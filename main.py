import sys
import traceback
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datavisualizer.widgets.custom_widgets.opening_window as ow
import datavisualizer.models.json_handler as jh
import datavisualizer.datavisualizer as dv


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Error catched!")
    print("Error message:\n", tb)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    # # you can use your own colors for different themes:
    # from PyQt5.QtGui import QPalette, QColor
    # palette = QPalette()
    # palette.setColor(QPalette.Window, QColor(25, 25, 25))  # (53, 53, 53))
    # palette.setColor(QPalette.WindowText, Qt.white)
    # palette.setColor(QPalette.Base, QColor(10, 10, 16))  # (25, 25, 25))
    # palette.setColor(QPalette.AlternateBase, QColor(25, 25, 25))  # (53, 53, 53))
    # palette.setColor(QPalette.ToolTipBase, Qt.white)
    # palette.setColor(QPalette.ToolTipText, Qt.white)
    # palette.setColor(QPalette.Text, Qt.white)
    # palette.setColor(QPalette.Button, QColor(53, 53, 53))
    # palette.setColor(QPalette.ButtonText, Qt.lightGray)
    # palette.setColor(QPalette.BrightText, Qt.red)
    # palette.setColor(QPalette.Link, QColor(42, 130, 218))
    # palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    # palette.setColor(QPalette.HighlightedText, Qt.white)
    # app.setPalette(palette)

    sys.excepthook = excepthook
    opening_window = ow.OpeningWindow()
    if opening_window.exec_() == QtWidgets.QDialog.Accepted:
        json_handler = jh.JsonHandler()
        json_handler.write_data_to_config_file(
            {'language': opening_window.language})
        data_visualizer = dv.DataVisualizer()
        data_visualizer.show()
        result = app.exec_()
        sys.exit(result)


if __name__ == "__main__":

    main()
