import os
import json
import math
import queue

def distance(aB, bB):
    # center points
    aX = aB[0] + (aB[2] / 2)
    aY = aB[1] + (aB[3] / 2)
    bX = bB[0] + (bB[2] / 2)
    bY = bB[1] + (bB[3] / 2)
    return math.sqrt((bX - aX)**2 + (bY - aY)**2)

# from keras: https://github.com/broadinstitute/keras-rcnn/blob/78313b6e9adf918b92ee1842adc199cb8fbe8df0/keras_rcnn/preprocessing/_object_detection.py#L19-L24
def union(au, bu, i):
    aA = (max(au[0], au[2]) - min(au[0], au[2])) * (max(au[1], au[3]) - min(au[1], au[3]))
    bA = (max(bu[0], bu[2]) - min(bu[0], bu[2])) * (max(bu[1], bu[3]) - min(bu[1], bu[3]))
    # x = min(au[0], bu[0])
    # y = min(au[1], bu[1])
    # w = max(au[2], bu[2]) - x
    # h = max(au[3], bu[3]) - y
    return aA + bA - i

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

overall_precision = []
gold_annotations_count = 0
pred_annotations_count = 0

json_file = open(pred_path + '/results/' + 'evaluation.json', mode='w', encoding='utf-8')
eval_data = []

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
    
    
    # if no pred annotation add 0% precision
    if len(pred_data) == 0:
        scores.append(0.0)
    for pred_beer in pred_data:
        pred_beer_values = (pred_beer['x'], pred_beer['y'], pred_beer['w'], pred_beer['h'])
        pred_annotations_count += 1
        q = queue.PriorityQueue()

        if len(gold_data) != 0:
            # compute distance to each gold_beer
            for gold_beer in gold_data:
                gold_beer_values = (gold_beer['x'], gold_beer['y'], gold_beer['w'], gold_beer['h'])
                gold_annotations_count += 1
                q.put((distance(pred_beer_values, gold_beer_values), gold_beer))
            
            # get shortest dist
            (_, gold_beer) = q.get()

            pred_beer_coords = (pred_beer['x'], pred_beer['y'], pred_beer['w']+pred_beer['x'], pred_beer['h']+pred_beer['y'])
            gold_beer_coords = (gold_beer['x'], gold_beer['y'], gold_beer['w']+gold_beer['x'], gold_beer['h']+gold_beer['y'])

            # compute intersection over union score
            result = iou(pred_beer_coords, gold_beer_coords)

            # rank scores
            scores.append(result)
            if result == 0.0:
                no_match.append(result)
            if result <= 0.5 and result != 0.0:
                bad_match.append(result)
            if result > 0.5:
                good_match.append(result)

    good_match_prec = 0.0
    bad_match_prec = 0.0
    score_prec = 0.0

    # compute average precisions
    if len(good_match) != 0:
        good_match_prec = sum(good_match)/len(good_match)
    if len(bad_match) != 0:
        bad_match_prec = sum(bad_match)/len(bad_match)
    if len(scores) != 0:
        score_prec = sum(scores)/len(scores)

    # sum up precision over all documents
    overall_precision.append(score_prec)
    eval_data.append({
        'filename': filename[:-5],
        'gold-annotations-count:': len(gold_data),
        'pred-annotations-count:': len(pred_data),
        'image-precision': score_prec,
        'good-match-count': len(good_match),
        'good-match-precision': good_match_prec,
        'bad-match-count': len(bad_match),
        'bad-match-precision': bad_match_prec,
        'no-match-count': len(no_match)
        })

if len(overall_precision) != 0:
    print('model-precision: ' + str(sum(overall_precision) / len(overall_precision)))    
    evaluation = {
        'image-evaluation': eval_data,
        'image-count:': len(os.listdir(pred_path)),
        'gold-annotations': gold_annotations_count,
        'pred-annotations': pred_annotations_count,
        'model-precision': sum(overall_precision) / len(overall_precision)
        }
    json.dump(evaluation, json_file)
json_file.close()
