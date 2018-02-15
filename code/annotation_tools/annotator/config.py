# The annotator tool will read images from INCOMING folder and creates resized
# images and annotation files in the FINAL folder.
# After processing, the original image gets moved into the PROCESSED folder.

PATHS = {
    'incoming': '/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/INCOMING/',
    'processed': '/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/INCOMING/PROCESSED',
    'final': '/home/devfoo/Nextcloud@Beuth/ISY_BBB/images/FINAL'
}

IMAGE_DIMENSIONS = (1000, 750)  # SET TARGET DIMENSIONS HERE
