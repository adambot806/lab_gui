import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction




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



def create_action(parent, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
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



