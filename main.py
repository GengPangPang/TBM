from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtUiTools import QUiLoader
import pandas as pd
import pyqtgraph as pg
import sys
import pickle

main_win = None
plot_win = None
with open('models/scaler_slurry.pkl', 'rb') as file:
    scaler_slurry = pickle.load(file)

with open('models/scaler_earth.pkl', 'rb') as file:
    scaler_earth = pickle.load(file)

with open('models/svr_slurry_thrust.pkl', 'rb') as file:
    slurry_thrust_model = pickle.load(file)

with open('models/svr_slurry_torque.pkl', 'rb') as file:
    slurry_torque_model = pickle.load(file)

with open('models/rf_earth_thrust.pkl', 'rb') as file:
    earth_thrust_model = pickle.load(file)

with open('models/rf_earth_torque.pkl', 'rb') as file:
    earth_torque_model = pickle.load(file)

class WelcomeWin:
    def __init__(self):
        self.ui = QUiLoader().load('models/in.ui')
        self.ui.setFixedSize(self.ui.size())
        self.ui.setWindowFlags(self.ui.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.ui.enter_btn.clicked.connect(self.enter)

    def enter(self):
        global main_win
        main_win = MainWin()
        main_win.ui.show()
        self.ui.close()

class MainWin:
    def __init__(self):
        self.ui = QUiLoader().load('models/TBM_main.ui')
        self.ui.setFixedSize(self.ui.size())
        self.ui.setWindowFlags(self.ui.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.slurry_data = None
        self.slurry_result = None
        self.earth_data = None
        self.earth_result = None
        self.plot_win = None
        self.ui.slurry_btn.clicked.connect(self.slurry_show)
        self.ui.earth_btn.clicked.connect(self.earth_show)
        self.ui.importslurry_btn.clicked.connect(self.slurry_openfile)
        self.ui.importearth_btn.clicked.connect(self.earth_openfile)
        self.ui.addslurry_btn.clicked.connect(self.addslurry)
        self.ui.addearth_btn.clicked.connect(self.addearth)
        self.ui.delslurry_btn.clicked.connect(self.delslurry)
        self.ui.delearth_btn.clicked.connect(self.delearth)
        self.ui.calslurry_btn.clicked.connect(self.calslurry)
        self.ui.calearth_btn.clicked.connect(self.calearth)
        self.ui.clearslurry_btn.clicked.connect(self.clearslurrry)
        self.ui.clearearth_btn.clicked.connect(self.clearearth)
        self.ui.saveslurry_btn.clicked.connect(self.saveslurry)
        self.ui.saveearth_btn.clicked.connect(self.saveearth)
        self.ui.drawslurry_btn.clicked.connect(self.drawslurry)
        self.ui.drawearth_btn.clicked.connect(self.drawearth)

    def drawslurry(self):
        torque_data = []
        thrust_data = []
        for row in range(self.ui.slurry_table.rowCount()):
            torque_item = self.ui.slurry_table.item(row, self.ui.slurry_table.columnCount() - 1)
            thrust_item = self.ui.slurry_table.item(row, self.ui.slurry_table.columnCount() - 2)
            if torque_item and thrust_item:
                torque_data.append(float(torque_item.text()))
                thrust_data.append(float(thrust_item.text()))
        if torque_data and thrust_data:
            self.plot_win = pg.GraphicsLayoutWidget()
            self.plot_win.setBackground('w')
            self.plot_win.setFixedSize(1000, 400)
            plot1 = self.plot_win.addPlot(title="推力", titleColor='#008080', titleSize='12pt')
            plot1.plot(thrust_data, pen='r')
            plot2 = self.plot_win.addPlot(title="扭矩", titleColor='#008080', titleSize='12pt')
            plot2.plot(torque_data, pen='g')
            self.plot_win.show()

    def drawearth(self):
        torque_data = []
        thrust_data = []
        for row in range(self.ui.earth_table.rowCount()):
            torque_item = self.ui.earth_table.item(row, self.ui.earth_table.columnCount() - 1)
            thrust_item = self.ui.earth_table.item(row, self.ui.earth_table.columnCount() - 2)
            if torque_item and thrust_item:
                torque_data.append(float(torque_item.text()))
                thrust_data.append(float(thrust_item.text()))
        if torque_data and thrust_data:
            self.plot_win = pg.GraphicsLayoutWidget()
            self.plot_win.setBackground('w')
            self.plot_win.setFixedSize(1000, 400)
            plot1 = self.plot_win.addPlot(title="推力", titleColor='#008080', titleSize='12pt')
            plot1.plot(thrust_data, pen='r')
            plot2 = self.plot_win.addPlot(title="扭矩", titleColor='#008080', titleSize='12pt')
            plot2.plot(torque_data, pen='g')
            self.plot_win.show()

    def saveslurry(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self.ui, "保存Excel文件", "", "Excel Files (*.xlsx)", options=options)
        if file_name:
            df = pd.DataFrame(columns=[self.ui.slurry_table.horizontalHeaderItem(i).text() for i in
                                       range(self.ui.slurry_table.columnCount())])
            for row in range(self.ui.slurry_table.rowCount()):
                row_data = []
                for col in range(self.ui.slurry_table.columnCount()):
                    item = self.ui.slurry_table.item(row, col)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append(None)
                df.loc[len(df)] = row_data
            df.to_excel(file_name, index=False)

    def saveearth(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self.ui, "保存Excel文件", "", "Excel Files (*.xlsx)", options=options)
        if file_name:
            df = pd.DataFrame(columns=[self.ui.earth_table.horizontalHeaderItem(i).text() for i in
                                       range(self.ui.earth_table.columnCount())])
            for row in range(self.ui.earth_table.rowCount()):
                row_data = []
                for col in range(self.ui.earth_table.columnCount()):
                    item = self.ui.earth_table.item(row, col)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append(None)
                df.loc[len(df)] = row_data
            df.to_excel(file_name, index=False)

    def clearslurrry(self):
        self.ui.slurry_table.setRowCount(0)

    def clearearth(self):
        self.ui.earth_table.setRowCount(0)

    def addslurry(self):
        addRowNumber = self.ui.slurry_table.currentRow() + 1
        self.ui.slurry_table.insertRow(addRowNumber)

    def delslurry(self):
        self.ui.slurry_table.removeRow(self.ui.slurry_table.currentRow())

    def addearth(self):
        addRowNumber = self.ui.earth_table.currentRow() + 1
        self.ui.earth_table.insertRow(addRowNumber)

    def delearth(self):
        self.ui.earth_table.removeRow(self.ui.earth_table.currentRow())

    def slurry_show(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def earth_show(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def slurry_openfile(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "选择文件", "", "Excel Files (*.xls *.xlsx);;CSV Files (*.csv)")
        if file_path:
            df = pd.read_excel(file_path).iloc[:,:-2]
            for row in range(df.shape[0]):
                self.ui.slurry_table.insertRow(row)
                for col in range(df.shape[1]):
                    item = QtWidgets.QTableWidgetItem(str(df.iloc[row, col]))
                    self.ui.slurry_table.setItem(row, col, item)

    def earth_openfile(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "选择文件", "", "Excel Files (*.xls *.xlsx);;CSV Files (*.csv)")
        if file_path:
            df = pd.read_excel(file_path).iloc[:, :-2]
            for row in range(df.shape[0]):
                self.ui.earth_table.insertRow(row)
                for col in range(df.shape[1]):
                    item = QtWidgets.QTableWidgetItem(str(df.iloc[row, col]))
                    self.ui.earth_table.setItem(row, col, item)

    def slurry_to_df(self):
        rows = self.ui.slurry_table.rowCount()
        cols = self.ui.slurry_table.columnCount()
        data = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.ui.slurry_table.item(row, col)
                if item is not None:
                    row_data.append(float(item.text()))
            data.append(row_data)
        df = pd.DataFrame(data)
        result = df.iloc[:, 1] / df.iloc[:, 2]
        df.insert(loc=3, column='深跨比', value=result)
        df = df.drop(df.columns[[0, 1, 2]], axis=1)
        self.slurry_data = df

    def earth_to_df(self):
        rows = self.ui.earth_table.rowCount()
        cols = self.ui.earth_table.columnCount()
        data = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.ui.earth_table.item(row, col)
                if item is not None:
                    row_data.append(float(item.text()))
            data.append(row_data)
        df = pd.DataFrame(data)
        result = df.iloc[:, 1] / df.iloc[:, 2]
        df.insert(loc=3, column='深跨比', value=result)
        df = df.drop(df.columns[[0, 1, 2]], axis=1)
        self.earth_data = df

    def calslurry(self):
        cols = self.ui.slurry_table.columnCount()
        self.slurry_to_df()
        slurry_scale = scaler_slurry.transform(self.slurry_data)
        slurry_torque_pred = slurry_torque_model.predict(slurry_scale)
        slurry_thrust_pred = slurry_thrust_model.predict(slurry_scale)
        for row_num in range(len(slurry_torque_pred)):
            self.ui.slurry_table.setItem(row_num, cols - 1, QtWidgets.QTableWidgetItem('{:.2f}'.format(slurry_torque_pred[row_num])))
            self.ui.slurry_table.setItem(row_num, cols - 2, QtWidgets.QTableWidgetItem('{:.2f}'.format(slurry_thrust_pred[row_num])))

    def calearth(self):
        cols = self.ui.earth_table.columnCount()
        self.earth_to_df()
        earth_scale = scaler_earth.transform(self.earth_data)
        earth_torque_pred = earth_torque_model.predict(earth_scale)
        earth_thrust_pred = earth_thrust_model.predict(earth_scale)
        for row_num in range(len(earth_torque_pred)):
            self.ui.earth_table.setItem(row_num, cols-1, QtWidgets.QTableWidgetItem('{:.2f}'.format(earth_torque_pred[row_num])))
            self.ui.earth_table.setItem(row_num, cols-2, QtWidgets.QTableWidgetItem('{:.2f}'.format(earth_thrust_pred[row_num])))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = WelcomeWin()
    w.ui.show()
    sys.exit(app.exec_())