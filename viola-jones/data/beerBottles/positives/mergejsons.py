import os
import json

merged_file = open('../info.dat', 'w')

for filename in os.listdir('./'):
    if filename[-5:] != '.json':
        continue
    data = json.load(open(filename))
    imgPath = 'positives/' + filename[:-4] + 'jpg'

    # relativ path
    merged_file.write(imgPath + '  ' + str(len(data)))
    # absolute path
    # merged_file.write(os.getcwd() + filename + '  ' + str(len(data)))
    
    for beer in data:
        merged_file.write('  ' + str(beer['x']) + ' ' + str(beer['y']) + ' ' + str(beer['w']) + ' ' + str(beer['h']))

    merged_file.write('\n')