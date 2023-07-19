import os, idaapi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QListWidget

class SetPaths(QDialog):
    def __init__(self):
        super(SetPaths, self).__init__()
        self.setWindowTitle("Set Paths")
        layout = QVBoxLayout()
        self.input_fields = []
        label = QLabel("Insert the function are you looking for: (e.g. system)")
        layout.addWidget(label)
        line_edit = QLineEdit()
        line_edit.setText("system")
        layout.addWidget(line_edit)
        self.input_fields.append(line_edit)
        label = QLabel("Insert the path to the libs: (e.g. C:\\Program File\\MyProgram\\Libs)")
        layout.addWidget(label)
        line_edit = QLineEdit()
        layout.addWidget(line_edit)
        self.input_fields.append(line_edit)
        button = QPushButton("OK")
        button.clicked.connect(self.on_button_clicked)
        layout.addWidget(button)
        self.setLayout(layout)
    
    def on_button_clicked(self):
        self.input_values = [field.text() for field in self.input_fields]
        self.accept()

    def getValues(self):
        return self.input_values[0],self.input_values[1]
    
class PathIDA:
    def __init__(self):
        dialog = SetPaths()
        dialog.exec_()
        self.function, self.libs, self.idapath = dialog.getValues()
    def getValues(self):
        return os.path.basename((idaapi.get_input_file_path())), self.function, self.libs, self.idapath


class SelectorIDA(QDialog):
    def __init__(self, listLibs):
        super(SelectorIDA, self).__init__()
        self.listLibs = listLibs
        self.over_layout()

    def over_layout(self):
        self.setup_layout()
        self.addAvailableItems(self.listLibs)
        
    def setup_layout(self):
        overlay = QVBoxLayout(self)
        lay = QHBoxLayout()

        self.mInput = QListWidget()
        self.mOuput = QListWidget()
        self.mButtonToSelected = QPushButton(">>")
        self.mBtnMoveToAvailable= QPushButton(">")
        self.mBtnMoveToSelected= QPushButton("<")
        self.mButtonToAvailable = QPushButton("<<")

        vlay = QVBoxLayout()

        vlay.addStretch()
        vlay.addWidget(self.mButtonToSelected)
        vlay.addWidget(self.mBtnMoveToAvailable)
        vlay.addWidget(self.mBtnMoveToSelected)
        vlay.addWidget(self.mButtonToAvailable)
        vlay.addStretch()

        vlay2 = QVBoxLayout()
        vlay2.addStretch()

        lay.addWidget(self.mInput)
        lay.addLayout(vlay)
        lay.addWidget(self.mOuput)
        lay.addLayout(vlay2)

        label = QLabel("In the following libs is available the function that you are lookin for.\nPls select in which of them discover if the function is reachable: (this includes ida anaysis for each lib)")
        overlay.addWidget(label)
        overlay.addLayout(lay)
        done_button = QPushButton(text="Done", clicked=self.get_right_elements)
        overlay.addWidget(done_button)

        self.update_buttons_status()
        self.connections()

    @pyqtSlot()
    def update_buttons_status(self):
        self.mBtnMoveToAvailable.setDisabled(not bool(self.mInput.selectedItems()) or self.mOuput.currentRow() == 0)
        self.mBtnMoveToSelected.setDisabled(not bool(self.mOuput.selectedItems()))

    def connections(self):
        self.mInput.itemSelectionChanged.connect(self.update_buttons_status)
        self.mOuput.itemSelectionChanged.connect(self.update_buttons_status)
        self.mBtnMoveToAvailable.clicked.connect(self.on_mBtnMoveToAvailable_clicked)
        self.mBtnMoveToSelected.clicked.connect(self.on_mBtnMoveToSelected_clicked)
        self.mButtonToAvailable.clicked.connect(self.on_mButtonToAvailable_clicked)
        self.mButtonToSelected.clicked.connect(self.on_mButtonToSelected_clicked)

    @pyqtSlot()
    def on_mBtnMoveToAvailable_clicked(self):
        self.mOuput.addItem(self.mInput.takeItem(self.mInput.currentRow()))

    @pyqtSlot()
    def on_mBtnMoveToSelected_clicked(self):
        self.mInput.addItem(self.mOuput.takeItem(self.mOuput.currentRow()))

    @pyqtSlot()
    def on_mButtonToAvailable_clicked(self):
        while self.mOuput.count() > 0:
            self.mInput.addItem(self.mOuput.takeItem(0))

    @pyqtSlot()
    def on_mButtonToSelected_clicked(self):
        while self.mInput.count() > 0:
            self.mOuput.addItem(self.mInput.takeItem(0))        

    def addAvailableItems(self, items):
        self.mInput.addItems(items)

    def get_right_elements(self):
        self.accept()
    
    def get_selected_elements(self):
        r = []
        for i in range(self.mOuput.count()):
            it = self.mOuput.item(i)
            r.append(it.text())
        return r
    

class SelectLibsIDA:
    def __init__(self, libs):
        self.list_selection = SelectorIDA(libs)
        self.list_selection.exec_()
    def getList(self):
        return self.list_selection.get_selected_elements()


















