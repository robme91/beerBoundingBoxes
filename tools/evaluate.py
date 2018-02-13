import os
import json
import math

def union(au, bu, i):
    aA = (max(au[0], au[2]) - min(au[0], au[2])) * (max(au[1], au[3]) - min(au[1], au[3]))
    bA = (max(bu[0], bu[2]) - min(bu[0], bu[2])) * (max(bu[1], bu[3]) - min(bu[1], bu[3]))
    # x = min(au[0], bu[0])
    # y = min(au[1], bu[1])
    # w = max(au[2], bu[2]) - x
    # h = max(au[3], bu[3]) - y
    return aA + bA - i

# from keras: https://github.com/broadinstitute/keras-rcnn/blob/78313b6e9adf918b92ee1842adc199cb8fbe8df0/keras_rcnn/preprocessing/_object_detection.py#L19-L24
def intersection(ai, bi):
    x = max(ai[0], bi[0])
    y = max(ai[1], bi[1])
    w = min(ai[2], bi[2]) - x
    h = min(ai[3], bi[3]) - y
    if w < 0 or h < 0:
        return 0.0
    return w*h

def iou(a, b):
    # a and b should be (x1,y1,x2,y2)
    if a[0] >= a[2] or a[1] >= a[3] or b[0] >= b[2] or b[1] >= b[3]:
        return 0.0

    i = intersection(a, b)
    u = union(a, b, i)

    return float(i) / float(u)

pred_path = './viola-jones/data/beerBottles/pred/'
gold_path = './viola-jones/data/beerBottles/eval/'

eval_file = open('evaluation.txt', 'w')
overall_precision = []

for filename in os.listdir(pred_path):
    if filename[-5:] != '.json':
        continue

    scores = []
    no_match = []
    good_match = []
    bad_match = []

    # eval and pred jsons have same naming?!
    pred_data = json.load(open(pred_path + filename))
    gold_data = json.load(open(gold_path + filename))

    eval_file.write('eval - ' + filename[:-5] + '\n')
    eval_file.write('gold-annotations: ' + str(len(gold_data)) + ' - pred-annotations: ' + str(len(pred_data)) + '\n')

    for gold_beer in gold_data:
        gold_beer_coords = (gold_beer['x'], gold_beer['y'], gold_beer['w']+gold_beer['x'], gold_beer['h']+gold_beer['y'])
        
        # if no pred annotation add 0% precision
        if len(pred_data) == 0:
            scores.append(0.0)

        for pred_beer in pred_data:
            pred_beer_coords = (pred_beer['x'], pred_beer['y'], pred_beer['w']+pred_beer['x'], pred_beer['h']+pred_beer['y'])

            # compute intersection over union score
            result = iou(pred_beer_coords, gold_beer_coords)

            scores.append(result)

            if result == 0.0:
                no_match.append(result)
            if result <= 0.5 and result != 0.0:
                bad_match.append(result)
            if result > 0.5:
                good_match.append(result)


    if len(good_match) != 0:
        eval_file.write('good match:    found - ' + str(len(good_match)) + '    precision - ' +  str(sum(good_match)/len(good_match)) + '\n')

    if len(bad_match) != 0:
        eval_file.write('bad match:     found - ' + str(len(bad_match)) + '     precision - ' + str(sum(bad_match)/len(bad_match)) + '\n')

    if len(no_match) != 0:
        eval_file.write('no match:      found - ' + str(len(no_match)) + '\n')

    if len(scores) != 0:
        eval_file.write('precision on image - ' + str(sum(scores)/len(scores)) + '\n')
        overall_precision.append(sum(scores)/len(scores))

    eval_file.write('\n')

if len(overall_precision) != 0:
    print('model-precision: ' + str(sum(overall_precision) / len(overall_precision)))
    eval_file.write('\n')    
    eval_file.write('model-precision: ' + str(sum(overall_precision) / len(overall_precision)) + '\n')
    eval_file.write('\n')
