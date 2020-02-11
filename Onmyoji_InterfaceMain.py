from PyQt5 import QtWidgets
import sys
from Onmyoji_Logic import MainWindow
import qdarkstyle

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    # 暗黑风格渲染
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow.show()
    sys.exit(app.exec_())
