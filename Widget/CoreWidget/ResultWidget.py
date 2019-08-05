import PyQt5.QtWidgets as QtWidgets


class ResultWidget(QtWidgets.QWidget):

    """
    This class is a TextEdit with a few extra features,
    can be integrated into LabGui as a message box,which
    can be use for warning and display calculate result
    """

    def __init__(self, parent=None):
        super(ResultWidget, self).__init__(parent)
        self.atom_num_label = QtWidgets.QLabel('Atom number: ')
        self.atom_num = QtWidgets.QLabel(str(0))
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.addWidget(self.atom_num_label)
        self.hLayout.addWidget(self.atom_num)
        self.setLayout(self.hLayout)

    def change_atom_num(self, atom_num):

        self.atom_num.setText(str(atom_num))


