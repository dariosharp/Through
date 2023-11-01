from idaapi import PluginForm
from PyQt5 import QtWidgets

class ResultClass(PluginForm):
    def OnCreate(self, form):
        self.parent = self.FormToPyQtWidget(form)
        self.items = []
        self.PopulateForm()

    def PopulateForm(self):
        layout = QtWidgets.QVBoxLayout()

        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Library Name", "Function Imported Affected", "Exploit address"])
        layout.addWidget(self.table)

        self.parent.setLayout(layout)

    def add_row(self, data):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        for col, item in enumerate(data):
            self.table.setItem(rowPosition, col, QtWidgets.QTableWidgetItem(item))

    def OnClose(self, form):
        pass



