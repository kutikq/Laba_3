from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QColorDialog, QWidget, QVBoxLayout, QToolBar, QHBoxLayout, QSpinBox, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor, QImage
import sys

# Класс для холста (для рисования)
class Canvas(QWidget):
    def __init__(self, parent=None, pen_color=Qt.black, pen_width=5, is_eraser=False):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StaticContents)
        self.setFixedSize(1000, 1000)

        # Инициализация переменных
        self.image = QImage(self.size(), QImage.Format_RGB32)  # Инициализация пустого изображения
        self.image.fill(Qt.white)  # Заполнение холста белым цветом
        self.last_point = None
        self.pen_color = pen_color  # Цвет пера
        self.pen_width = pen_width  # Размер пера
        self.is_eraser = is_eraser  # Инструмент (рисование или ластик)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            painter = QPainter(self.image)  # Рисовать не на самом виджете, а на изображении

            # Параметры мыши: цвет, размер, тип линии, вид концов
            if self.is_eraser:
                pen = QPen(Qt.white, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)  # Белый цвет для ластика
            else:
                pen = QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)  # Обычное рисование

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

        # Инициализация переменных для рисования
        self.pen_color = Qt.black  # Начальный цвет пера
        self.pen_width = 5  # Начальный размер пера
        self.is_eraser = False  # Начально инструмент не ластик

        # Создаем основной виджет
        self.central_widget = QWidget(self)
        # Создаем макет для виджета
        layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Создаем кнопку "Начать" с текстом
        self.button = QPushButton("Начать (выбора нет)", self)
        self.button.setGeometry(100, 100, 200, 50)  # Размеры и позиция кнопки
        self.button.clicked.connect(self.start_drawing)

    def start_drawing(self):
        # Метод для переключения на холст для рисования
        self.canvas = Canvas(self, self.pen_color, self.pen_width, self.is_eraser)  # Передаем параметры в Canvas
        self.setCentralWidget(self.canvas)  # Заменяем текущий виджет на холст
        self.button.setVisible(False)  # Скрываем кнопку после старта рисования

        # Добавляем панель инструментов
        self.create_toolbar()

    def create_toolbar(self):
        # Создаём панель инструментов
        toolbar = QToolBar(self)
        toolbar.setMovable(False)  # Фиксируем панель, чтобы она не перемещалась
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # Задаём стиль кнопок

        # Создаём контейнер для горизонтального размещения кнопок
        container_widget = QWidget(self)
        container_layout = QHBoxLayout(container_widget)
        container_widget.setLayout(container_layout)

        # Создаём кнопки
        color_button = QPushButton("Выбрать цвет", self)
        color_button.clicked.connect(self.choose_color)
        width_button = QPushButton("Выбрать размер", self)
        width_button.clicked.connect(self.choose_width)
        eraser_button = QPushButton("Выбрать ластик", self)
        eraser_button.clicked.connect(self.chose_eraser)

        # Добавляем кнопки в контейнер
        container_layout.addWidget(color_button)
        container_layout.addWidget(width_button)
        container_layout.addWidget(eraser_button)

        # Добавляем контейнер в панель инструментов
        toolbar.addWidget(container_widget)

        # Добавляем панель инструментов в главное окно
        self.addToolBar(Qt.TopToolBarArea, toolbar)

    def choose_color(self):
        color = QColorDialog.getColor(self.pen_color, self)
        if color.isValid():
            self.pen_color = color  # Обновляем цвет пера
            self.canvas.pen_color = self.pen_color  # Обновляем цвет на холсте

    def choose_width(self):
        dialog = QDialog(self)  # Диалоговое окно
        dialog.setWindowTitle("Выберите размер пера")

        layout = QVBoxLayout(dialog)  # Макет для диалога
        size_spinbox = QSpinBox(dialog)
        size_spinbox.setRange(1, 50)
        size_spinbox.setValue(self.pen_width)
        layout.addWidget(size_spinbox)

        ok_button = QPushButton("OK", dialog)
        layout.addWidget(ok_button)

        # Обработчик кнопки OK
        ok_button.clicked.connect(lambda: (self.set_pen_size(size_spinbox.value()), dialog.close()))

        dialog.exec_()

    def set_pen_size(self, value):
        """Метод для обновления размера пера"""
        self.pen_width = value  # Обновляем размер пера на основе значения из QSpinBox
        print(f"Размер пера: {self.pen_width}")
        self.canvas.pen_width = self.pen_width  # Обновляем размер на холсте

    def chose_eraser(self):
        """Метод для переключения между рисованием и ластиком"""
        self.is_eraser = not self.is_eraser  # Переключаем состояние (рисование или ластик)
        self.canvas.is_eraser = self.is_eraser  # Обновляем состояние ластика на холсте


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
