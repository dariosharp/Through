import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit
import idaapi

class MyDialog(QDialog):
    input_signal = pyqtSignal(list)
    
    def __init__(self):
        super(MyDialog, self).__init__()
        self.setWindowTitle("My Dialog")
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
        label = QLabel("Insert the IDApro PATH: (e.g. C:\\Program Files\\IDAPro\\ida.exe)")
        layout.addWidget(label)
        line_edit = QLineEdit()
        line_edit.setText("C:\\Program Files\\IDAPro\\ida.exe")
        layout.addWidget(line_edit)
        self.input_fields.append(line_edit) 
        button = QPushButton("OK")
        button.clicked.connect(self.on_button_clicked)
        layout.addWidget(button)
        self.setLayout(layout)
    
    def on_button_clicked(self):
        input_values = [field.text() for field in self.input_fields]
        self.input_signal.emit(input_values)
        self.accept()

class windowIDA:
    def __init__(self):
        dialog = MyDialog()
        dialog.input_signal.connect(lambda values: setattr(MyDialog, 'function', values[0]))
        dialog.input_signal.connect(lambda values: setattr(MyDialog, 'libs', values[1]))
        dialog.input_signal.connect(lambda values: setattr(MyDialog, 'idapath', values[2]))
        dialog.exec_()
        self.function = MyDialog.function
        self.libs = MyDialog.libs
        self.idapath = MyDialog.idapath
    def getValues(self):
        return os.path.basename((idaapi.get_input_file_path())), self.function, self.libs, self.idapath


