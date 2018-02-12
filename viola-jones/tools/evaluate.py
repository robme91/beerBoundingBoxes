import os
import json
import math

# TODO: correct path from root
pred_path = '../data/beerBottles/pred/results_test2/'
eval_path = '../data/beerBottles/eval/'

eval_file = open('evaluation.txt', 'w')

threshold = 0.05

for filename in os.listdir(pred_path):
    if filename[-5:] != '.json':
        continue

    # eval and pred jsons have same naming?!
    pred_data = json.load(open(pred_path + filename))
    eval_data = json.load(open(eval_path + filename))

    for pred_beer in pred_data:
        for eval_beer in eval_data:

            w_threshold = eval_beer['w'] * threshold
            h_threshold = eval_beer['h'] * threshold

            if (pred_beer['w'] <= eval_beer['w'] - w_threshold or pred_beer['w'] >= eval_beer['w'] + w_threshold):
                continue
            if (pred_beer['h'] <= eval_beer['h'] - h_threshold or pred_beer['h'] >= eval_beer['h'] + h_threshold):
                continue
            if (pred_beer['x'] <= eval_beer['x'] - w_threshold or pred_beer['x'] >= eval_beer['x'] + w_threshold):
                continue
            if (pred_beer['y'] <= eval_beer['y'] - h_threshold or pred_beer['y'] >= eval_beer['y'] + h_threshold):
                continue

            if pred_beer['w'] == eval_beer['w']:
                w_accuracy = 1
            else:
                w_accuracy = math.sqrt((pred_beer['w'] - eval_beer['w']) ** 2) / w_threshold

            if pred_beer['h'] == eval_beer['h']:
                h_accuracy = 1
            else:
                h_accuracy = math.sqrt((pred_beer['h'] - eval_beer['h']) ** 2) / h_threshold

            if pred_beer['x'] == eval_beer['x']:
                x_accuracy = 1
            else:
                x_accuracy = math.sqrt((pred_beer['x'] - eval_beer['x']) ** 2) / w_threshold

            if pred_beer['y'] == eval_beer['y']:
                y_accuracy = 1
            else:
                y_accuracy = math.sqrt((pred_beer['y'] - eval_beer['y']) ** 2) / h_threshold

            data_accuracy = (w_accuracy + h_accuracy + x_accuracy + y_accuracy) / 4
            eval_file.write(filename[:-5] + ' - accuracy: ' + str(data_accuracy) + '\n')
