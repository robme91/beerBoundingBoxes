#!/usr/bin/env python3

import glob
from enum import Enum
from random import randint
from tkinter import *
from PIL import Image, ImageTk
import img_rotate
import os
import json
from AutocompleteEntry import AutocompleteEntry
from config import PATHS, IMAGE_DIMENSIONS

def getRandomPicturePathFromPath(path):
    image_paths = list(glob.glob(path + '/*.jpg'))
    if len(image_paths) != 0:
        return image_paths[randint(0, len(image_paths) - 1)]
    else:
        print("No images to process, quitting.")
        exit(1)


def getNextFreeFileID():
    images = list(glob.glob(PATHS['final'] + '/*.jpg'))
    return str(len(images)).zfill(4)


class OperationMode(Enum):  # ENUM FOR APPSTATE
    SETPOINT1 = 1
    SETPOINT2 = 2


class App:
    BEER_BRANDS = set()

    def resetState(self):
        self.resetAfterBoundingBoxFinalization()
        self.CURRENT_BB_OBJECTS = []
        self.CURRENT_IMAGE = None
        self.CURRENT_IMAGE_PATH = None

    def resetAfterBoundingBoxFinalization(self):
        self.CURRENT_EDITMODE = OperationMode.SETPOINT1
        self.CURRENT_CROSSHAIR_COLOR = 'red'
        self.CURRENT_POINT0 = None
        self.CURRENT_POINT1 = None
        self.CURRENT_LASTPOINT = None
        self.CURRENT_DETAILPOPUP = {
            'brand': None,
            'isOpen': None
        }
        self.CURRENT_DETAILPOPUP['isOpen'] = IntVar()

    def __init__(self, master):
        self.resetState()
        self.master = master
        frame = Frame(master)
        frame.pack()
        self.imgViewCanvas = Canvas(frame, cnf={"width": IMAGE_DIMENSIONS[0], "height": IMAGE_DIMENSIONS[1]})
        self.imgViewCanvas.pack(side=LEFT)
        self.imgViewCanvas.bind('<Motion>', self.imgViewCanvasMouseMove)
        self.imgViewCanvas.bind('<ButtonRelease-1>', self.imgViewCanvasMouseClick)
        master.bind('<KeyPress-n>', self.next)
        master.bind('<KeyPress-N>', self.next)
        self.loadPicture(getRandomPicturePathFromPath(PATHS['incoming']))

    def imgViewCanvasMouseMove(self, event):
        self.redrawCrosshair(event.x, event.y)
        if self.CURRENT_EDITMODE is OperationMode.SETPOINT2:
            self.imgViewCanvas.delete('bb_preview')
            self.imgViewCanvas.create_rectangle(self.CURRENT_LASTPOINT[0], self.CURRENT_LASTPOINT[1], event.x, event.y,
                                                outline='green yellow', width=1, tag='bb_preview')

    def imgViewCanvasMouseClick(self, event):
        if self.CURRENT_EDITMODE is OperationMode.SETPOINT1:
            self.CURRENT_CROSSHAIR_COLOR = 'green yellow'
            self.CURRENT_POINT0 = (event.x, event.y)
            self.addNewPoint(event.x, event.y)
            self.redrawCrosshair(event.x, event.y)
            self.CURRENT_EDITMODE = OperationMode.SETPOINT2
            return
        if self.CURRENT_EDITMODE is OperationMode.SETPOINT2:
            self.CURRENT_CROSSHAIR_COLOR = 'red'
            self.CURRENT_POINT1 = (event.x, event.y)
            self.addNewPoint(event.x, event.y)
            self.redrawCrosshair(event.x, event.y)
            self.showDetailsInput()
            self.CURRENT_EDITMODE = OperationMode.SETPOINT1
            return

    def redrawCrosshair(self, x, y):
        self.imgViewCanvas.delete('crosshair')
        self.imgViewCanvas.create_line(x, 0, x, self.imgViewCanvas.winfo_height(), fill=self.CURRENT_CROSSHAIR_COLOR,
                                       width=1, tag='crosshair')
        self.imgViewCanvas.create_line(0, y, self.imgViewCanvas.winfo_width(), y, fill=self.CURRENT_CROSSHAIR_COLOR,
                                       width=1, tag='crosshair')

    def addNewPoint(self, x, y):
        self.CURRENT_LASTPOINT = (x, y)
        self.imgViewCanvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='green yellow', width=0)

    def loadPicture(self, path):
        self.CURRENT_IMAGE_PATH = path
        self.CURRENT_IMAGE = Image.open(self.CURRENT_IMAGE_PATH)
        try:
            self.CURRENT_IMAGE, _ = img_rotate.fix_orientation(self.CURRENT_IMAGE)
        except ValueError as e:
            print('Could not rotate', os.path.basename(path), '-', e)
        self.CURRENT_IMAGE = self.CURRENT_IMAGE.resize(IMAGE_DIMENSIONS, resample=Image.LANCZOS)
        self.imgViewCanvas.image = ImageTk.PhotoImage(self.CURRENT_IMAGE)
        self.imgViewCanvas.create_image(0, 0, anchor='nw', image=self.imgViewCanvas.image)
        self.master.title(os.path.basename(self.CURRENT_IMAGE_PATH))

    def showDetailsInput(self):
        detailsPopup = Toplevel(takefocus=True)
        self.detailsPopup = detailsPopup
        detailsPopup.grab_set()
        detailsPopup.geometry('200x200+50+50')
        self.detailsPopupBrandEntry = AutocompleteEntry(list(self.BEER_BRANDS), detailsPopup)
        self.detailsPopupBrandEntry.focus_set()
        detailsPopupOpenCheckbox = Checkbutton(detailsPopup, text='is open?',
                                               variable=self.CURRENT_DETAILPOPUP['isOpen'])
        detailsPopupOpenCheckbox.select()
        detailsPopupOKBtn = Button(detailsPopup, text="OK", command=self.detailsInputOKClick)
        detailsPopupCancelBtn = Button(detailsPopup, text="CANCEL", command=self.detailsInputCancelClick)
        Label(detailsPopup, text='Brand:').pack()
        self.detailsPopupBrandEntry.pack()
        detailsPopupOpenCheckbox.pack()
        detailsPopupOKBtn.pack()
        detailsPopupCancelBtn.pack()

    def detailsInputOKClick(self):
        brand = self.detailsPopupBrandEntry.get()
        isOpen = self.CURRENT_DETAILPOPUP['isOpen'].get()
        self.finalizeCurrentBBEntry(brand, isOpen)
        self.resetAfterBoundingBoxFinalization()
        self.detailsPopup.destroy()

    def detailsInputCancelClick(self):
        self.resetAfterBoundingBoxFinalization()
        self.detailsPopup.destroy()

    def finalizeCurrentBBEntry(self, brand, isOpen):
        (p0x, p0y) = self.CURRENT_POINT0
        (p1x, p1y) = self.CURRENT_POINT1
        isOpen = (bool(isOpen))
        x = min(p0x, p1x)
        y = min(p0y, p1y)
        w = max(p0x, p1x) - x
        h = max(p0y, p1y) - y
        self.CURRENT_BB_OBJECTS.append({
            'brand': brand,
            'isOpen': isOpen,
            'x': x,
            'y': y,
            'w': w,
            'h': h
        })
        self.BEER_BRANDS.add(brand)

    def next(self, event):
        # finalize current progress and load next pic
        if len(self.CURRENT_BB_OBJECTS) > 0:
            newFileId = getNextFreeFileID()
            self.moveProcessedPictureToProcessedPath()
            self.copyResizedPictureToFinalPath(newFileId)
            self.storeBBJSON(newFileId)
        self.resetState()
        self.loadPicture(getRandomPicturePathFromPath(PATHS['incoming']))
        return

    def moveProcessedPictureToProcessedPath(self):
        filename = os.path.basename(self.CURRENT_IMAGE_PATH)
        os.rename(self.CURRENT_IMAGE_PATH, PATHS['processed'] + os.sep + filename)

    def copyResizedPictureToFinalPath(self, newFileID):
        self.CURRENT_IMAGE.save(PATHS['final'] + os.sep + newFileID + '.jpg')

    def storeBBJSON(self, newFileID):
        # store all bb points in json
        file = open(PATHS['final'] + os.sep + newFileID + '.json', mode='w', encoding='utf-8')
        json.dump(self.CURRENT_BB_OBJECTS, file, sort_keys=True)
        file.close()


root = Tk()
app = App(root)
root.mainloop()
root.destroy()
