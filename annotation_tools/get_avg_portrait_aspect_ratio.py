import glob
import json

DSPATH = '/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/FINAL/'
ratios = []

for filename in glob.glob(DSPATH + '/*.json'):
    bb_array = json.load(open(filename, mode='r'))
    for bb in bb_array:
        w = bb['w']
        h = bb['h']
        if h > w:
            ratios.append(h/w)
            print(h/w)

print('===')
print('min:', min(ratios), 'max:', max(ratios), 'avg:', sum(ratios) / len(ratios))