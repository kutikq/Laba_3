from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1000, 1000)

        # Кнопка для вызова диалога
        button = QPushButton("Начать (выбора нет) ", self)
        button.setGeometry(100, 100, 200, 50)
        button.clicked.connect(self.start_drawing)

    def start_drawing(self):
        
 
