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

overall_iou = []
overall_precision = []
overall_recall = []
file_count = 0
gold_annotations_count = 0
pred_annotations_count = 0

json_file = open(pred_path + '/results/' + 'evaluation.json', mode='w', encoding='utf-8')
eval_data = []

for filename in os.listdir(pred_path):
    if filename[-5:] != '.json':
        continue

    file_count += 1
    iou_arr = []
    no_match = []
    good_match = []
    bad_match = []

    # eval and pred jsons have same naming?!
    pred_data = json.load(open(pred_path + filename))
    gold_data = json.load(open(gold_path + filename))    
    
    # count gold and pred annotations for active images
    pred_annotations_count += len(pred_data)
    gold_annotations_count += len(gold_data)
    
    # if no pred annotation add 0.0 iou for each gold annotation
    if len(pred_data) == 0:
        for gold_beer in gold_data:
            iou_arr.append(0.0)
            no_match.append(0.0)
    for pred_beer in pred_data:
        # if no gold annotation given, add 0.0 iou
        if len(gold_data) == 0:
            iou_arr.append(0.0)
            no_match.append(0.0)
            continue
        else:
            pred_beer_values = (pred_beer['x'], pred_beer['y'], pred_beer['w'], pred_beer['h'])
            q = queue.PriorityQueue()

            # compute distance to each gold_beer
            for gold_beer in gold_data:
                gold_beer_values = (gold_beer['x'], gold_beer['y'], gold_beer['w'], gold_beer['h'])
                q.put((distance(pred_beer_values, gold_beer_values), gold_beer))
            
            # get shortest dist
            (_, gold_beer) = q.get()

            pred_beer_coords = (pred_beer['x'], pred_beer['y'], pred_beer['w']+pred_beer['x'], pred_beer['h']+pred_beer['y'])
            gold_beer_coords = (gold_beer['x'], gold_beer['y'], gold_beer['w']+gold_beer['x'], gold_beer['h']+gold_beer['y'])

            # compute intersection over union coefficient
            result = iou(pred_beer_coords, gold_beer_coords)

            # rank iou
            iou_arr.append(result)
            if result == 0.0:
                no_match.append(result)
            if result <= 0.5 and result != 0.0:
                bad_match.append(result)
            if result > 0.5:
                good_match.append(result)

    # iterate over annotations again to compute false negatives
    fn = 0
    for gold_beer in gold_data:
        gold_beer_coords = (gold_beer['x'], gold_beer['y'], gold_beer['w']+gold_beer['x'], gold_beer['h']+gold_beer['y'])
        false_negative_bool = True
        for pred_beer in pred_data:
            pred_beer_coords = (pred_beer['x'], pred_beer['y'], pred_beer['w']+pred_beer['x'], pred_beer['h']+pred_beer['y'])
            result = iou(pred_beer_coords, gold_beer_coords)
            if result > 0.5:
                false_negative_bool = False

        if false_negative_bool == True:
            fn += 1

    iou_coefficient = 0.0
    precision = 0.0
    recall = 0.0
    F1 = 0.0

    # compute precision, recall, f1 and iou for active image
    if len(iou_arr) != 0:
        iou_coefficient = sum(iou_arr) / len(iou_arr)
        tp = len(good_match)
        fp = len(bad_match) + len(no_match)

        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        if precision != 0.0 and recall != 0.0:
            F1 = 2 * ((precision * recall) / (precision + recall))

    # sum up precision, recall and iou over all documents
    overall_precision.append(precision)
    overall_recall.append(recall)
    overall_iou.append(iou_coefficient)

    # create json data
    eval_data.append({
        'filename': filename[:-5],
        'gold-annotations:': len(gold_data),
        'pred-annotations:': len(pred_data),
        'precision': precision,
        'recall': recall,
        'F1': F1,
        'iou-coefficient': iou_coefficient,
        'good-matches': len(good_match),
        'bad-matches': len(bad_match),
        'no-matches': len(no_match)
        })


if len(overall_precision) != 0:
    pr = sum(overall_precision) / len(overall_precision)
    re = sum(overall_recall) / len(overall_recall)
    evaluation = {
        'single-image-evaluation': eval_data,
        'image-count:': file_count,
        'gold-annotations': gold_annotations_count,
        'pred-annotations': pred_annotations_count,
        'precision': pr,
        'recall': re,
        'F1': 2 * ((pr * re) / (pr + re)),
        'iou-coefficient': sum(overall_iou) / len(overall_iou)
        }
    json.dump(evaluation, json_file)
json_file.close()
