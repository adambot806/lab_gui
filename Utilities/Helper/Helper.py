import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import threading
import numpy as np


class print_redirect(QObject):
    """
    replace stdout that both prints and emits the text as a signal

    """
    print_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.old_stdout = sys.stdout

    def write(self, stri):
        self.old_stdout.write(stri)
        # emit the stdout statements
        self.print_signal.emit(stri)

    def flush(self):
        self.old_stdout.flush()


class thread_with_trace(threading.Thread):

    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


def create_action(parent, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False):
    action = QAction(text, parent)
    if icon is not None:
        action.setIcon(QIcon("./images/%s.png" % icon))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot is not None:
        action.triggered.connect(slot)
    if checkable:
        action.setCheckable(True)
    return action


def split_list(image):
    """
    design for Chameleon camera, take the  image to array
    :param image: list
    :return:
    """
    alist = []
    img_rows = image.getRows()
    img_cols = image.getCols()
    img_data = image.getData()
    for i in range(img_rows):
        alist.append(img_data[i*img_cols:(i+1)*img_cols])
    return np.array(alist)

