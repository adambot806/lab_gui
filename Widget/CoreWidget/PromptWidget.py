import sys
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from Utilities.Helper import Helper


class PromptWidget(QtWidgets.QWidget):

    """
    This class is a TextEdit with a few extra features,
    can be integrated into LabGui as a message box,which
    can be use for warning and display calculate result
    """

    def __init__(self, parent=None):
        super(PromptWidget, self).__init__(parent)
        self.consoleTextEdit = QtWidgets.QTextEdit()
        self.consoleTextEdit.setReadOnly(True)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.addWidget(self.consoleTextEdit)
        self.setLayout(self.verticalLayout)

    def console_text(self, new_text=None):

        """get/set method for the text in the console"""

        if new_text == None:

            return str((self.consoleTextEdit.toPlainText())).rstrip()

        else:

            self.consoleTextEdit.setPlainText(new_text)

    def automatic_scroll(self):
        """
        performs an automatic scroll up
        the latest text shall always be in view
        """
        sb = self.consoleTextEdit.verticalScrollBar()
        sb.setValue(sb.maximum())
