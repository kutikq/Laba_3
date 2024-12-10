from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QColorDialog, QWidget, QVBoxLayout, QToolBar, QColor, QLayout, QSpinBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen #для пера
import sys

# Класс для холста (для рисования)
class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StaticContents)
        self.setFixedSize(1000, 1000)

  # инициализация переменных
        self.image = self.grab().toImage()
        self.last_point = None
        self.pen_color = Qt.black
        self.pen_width = 5

    # иннициализируум мышь
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()

    # Метод для работы пера
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton: #если зажата ЛКМ
            painter = QPainter(self.image) #Рисовать не на самом виджете, а на изображении
            # Параметры мыши: цвет, размер, тип линии, вид концов
            pen = QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap) 
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()
    
    def paintEvent(self, event):
        """Перерисовываем холст"""
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)


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

    # Добавляем кнопку в макет
        layout.addWidget(self.button)

    # Создаем панель инструментов
        self.create_toolbar()

    #определяем нашу панель
    def create_toolbar(self):
        toolbar = QToolBar(self)

        # Создаем действия для панели инструментов
        color_button = QPushButton("Выбрать цвет", self)
        color_button.clicked.connect(self.choose_color)  # Подключаем к методу выбора цвета
        width_button = QPushButton("Выбрать размер", self)
        width_button.clicked.connect(self.chose_width)

        # Добавляем кнопки на панель инструментов
        toolbar.addWidget(color_button)
        toolbar.addWidget(width_button)

        # Добавляем панель инструментов в главное окно
        self.addToolBar(toolbar)

    #выбор цвета на пере
    def choose_color(self):
        color = QColorDialog.getColor(self.pen_color, self)
        if color.isValid():
            self.pen_color = color  # Обновляем цвет пер
    
    #выбор разсера пера
    def chose_width(self):
        """Метод для создания и отображения QSpinBox для выбора размера пера"""
        # Создаем QSpinBox для выбора размера пера
        self.size_spinbox = QSpinBox(self)
        self.size_spinbox.setRange(1, 50)  # Устанавливаем диапазон от 1 до 50
        self.size_spinbox.setValue(self.pen_width)  # Устанавливаем начальное значение (по умолчанию размер пера 5)
        
        # Подключаем событие изменения значения к методу, который обновляет размер пера
        self.size_spinbox.valueChanged.connect(self.set_pen_size)

        # Показываем QSpinBox на экране
        self.size_spinbox.show()
    
    def set_pen_size(self, value):
        """Метод для обновления размера пера"""
        self.pen_width = value  # Обновляем размер пера на основе значения из QSpinBox
        print(f"Размер пера: {self.pen_width}")



    # Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())




 
