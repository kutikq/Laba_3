from PySide6.QtWidgets import QApplication, QWidget
import sys

# Точка входа
if __name__ in '__main__':
    # Создание класса приложения
    app = QApplication(sys.argv)
    app.setApplicationName('ЙоУ')

    # Видимый виджет приложения (пока пустой)
    w = QWidget()
    w.show()

    # Запуск цикла обработки сообщений
    app.exec()