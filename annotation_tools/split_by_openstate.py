import glob
import json
import os

from PIL import Image

DSPATH = '/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/FINAL/'
OPENPATH = '/home/devfoo/Desktop/openclosed/open/'
CLOSEDPATH = '/home/devfoo/Desktop/openclosed/closed/'

for filename in glob.glob(DSPATH + '/*.json'):
    bb_array = json.load(open(filename, mode='r'))
    imagefilename = os.path.splitext(os.path.basename(filename))[0] + '.jpg'
    image = Image.open(DSPATH + imagefilename)
    for i, bb in enumerate(bb_array):
        x0 = bb['x']
        y0 = bb['y']
        x1 = x0 + bb['w']
        y1 = y0 + bb['h']
        single_beer_image = image.crop((x0,y0,x1,y1))
        # print(os.path.basename(filename), imagefilename, i, bb)
        if bb['isOpen'] == False:
            single_beer_image.save(CLOSEDPATH + str(i) + '_' + imagefilename)
        else:
            single_beer_image.save(OPENPATH + str(i) + '_' + imagefilename)
