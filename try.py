from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QColorDialog, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen #для пера
import sys

# Класс для холста (для рисования)
class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StaticContents)
        self.setFixedSize(1000, 1000)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1000, 800)

 # Создаем основной виджет
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Создаем макет для виджета
        layout = QVBoxLayout(self.central_widget)
    
         # Создаем кнопку "Начать" с текстом
        self.button = QPushButton("Начать (выбора нет)", self)
        self.button.setGeometry(100, 100, 200, 50)  # Размеры и позиция кнопки
        self.button.clicked.connect(self.start_drawing)

    def start_drawing(self):
        #Метод для переключения на холст для рисования
        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)  # Заменяем текущий виджет на холст
        self.button.setVisible(False)  # Скрываем кнопку после старта рисования

    # Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())




 
