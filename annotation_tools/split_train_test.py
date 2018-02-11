import random
import shutil

DSPATH = '/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/FINAL/'
TRAINPATH = '/home/devfoo/Desktop/split8020/train/'
TESTPATH = '/home/devfoo/Desktop/split8020/test/'

ids = list(range(0,1000))
random.shuffle(ids)

train_ids = ids[0:800]
test_ids = ids[800:1000]

for id in train_ids:
    id = str(id).zfill(4)
    shutil.copy2(DSPATH + id + '.jpg', TRAINPATH)
    shutil.copy2(DSPATH + id + '.json', TRAINPATH)

for id in test_ids:
    id = str(id).zfill(4)
    shutil.copy2(DSPATH + id + '.jpg', TESTPATH)
    shutil.copy2(DSPATH + id + '.json', TESTPATH)