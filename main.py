import sys
import math
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QFont, QColor

class ClockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 200)
        self.hour = 12
        self.minute = 0
        self.selected_hand = None  # Хранит, какая стрелка выбрана

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Рисуем фон с градиентом
        gradient = QColor(240, 240, 240)
        painter.fillRect(self.rect(), gradient)

        # Рисуем циферблат
        side = min(self.width(), self.height())
        painter.setViewport((self.width() - side) // 2, (self.height() - side) // 2, side, side)
        painter.setWindow(0, 0, 200, 200)

        # Рисуем круг
        painter.setPen(Qt.black)
        painter.setBrush(Qt.white)
        painter.drawEllipse(0, 0, 200, 200)

        # Рисуем деления
        for i in range(0, 60):
            angle = 6 * i  # 6 градусов между делениями
            length = 10 if i % 5 else 15  # Длинные деления для часов
            painter.drawLine(100 + (90 - length) * math.sin(math.radians(angle)),
                             100 - (90 - length) * math.cos(math.radians(angle)),
                             100 + 90 * math.sin(math.radians(angle)),
                             100 - 90 * math.cos(math.radians(angle)))

        # Рисуем цифры
        painter.setFont(QFont("Arial", 10))
        for i in range(1, 13):
            angle = 30 * i  # 30 градусов между цифрами
            x = 100 + 70 * math.sin(math.radians(angle))
            y = 100 - 70 * math.cos(math.radians(angle))
            painter.drawText(int(x) - 10, int(y) + 10, str(i))

        # Рисуем стрелки
        self.draw_hand(painter, self.hour % 12 * 30 + self.minute * 0.5, 50, Qt.black, 'hour')  # Часовая стрелка
        self.draw_hand(painter, self.minute * 6, 70, Qt.blue, 'minute')  # Минутная стрелка

    def draw_hand(self, painter, angle, length, color, hand_type):
        painter.setPen(color)
        painter.save()
        painter.translate(100, 100)
        painter.rotate(angle)

        # Устанавливаем стиль стрелки
        if hand_type == 'hour':
            painter.setBrush(Qt.black)
            painter.setPen(Qt.black)
            painter.drawLine(0, 0, 0, -length)  # Часовая стрелка
        else:
            painter.setBrush(Qt.blue)
            painter.setPen(Qt.blue)
            painter.drawLine(0, 0, 0, -length)  # Минутная стрелка

        painter.restore()

        # Проверка на выбор стрелки
        if self.selected_hand == hand_type:
            painter.setBrush(Qt.red)
            painter.drawEllipse(100 + length * math.sin(math.radians(angle)), 
                                100 - length * math.cos(math.radians(angle)), 8, 8)

    def mousePressEvent(self, event):
        # Преобразуем координаты мыши в координаты циферблата
        side = min(self.width(), self.height())
        x = event.position().x() - (self.width() - side) // 2
        y = event.position().y() - (self.height() - side) // 2
        x -= 100
        y -= 100

        # Вычисляем угол
        angle = math.degrees(math.atan2(y, x)) + 90
        if angle < 0:
            angle += 360

        # Проверяем, какая стрелка выбрана
        if abs(angle - (self.hour % 12 * 30 + self.minute * 0.5)) < 15:
            self.selected_hand = 'hour'
        elif abs(angle - (self.minute * 6)) < 15:
            self.selected_hand = 'minute'
        else:
            self.selected_hand = None

    def mouseMoveEvent(self, event):
        if self.selected_hand:
            # Преобразуем координаты мыши в координаты циферблата
            side = min(self.width(), self.height())
            x = event.position().x() - (self.width() - side) // 2
            y = event.position().y() - (self.height() - side) // 2
            x -= 100
            y -= 100

            # Вычисляем угол
            angle = math.degrees(math.atan2(y, x)) + 90
            if angle < 0:
                angle += 360

            # Обновляем время в зависимости от выбранной стрелки
            if self.selected_hand == 'hour':
                self.hour = int(angle / 30) % 12
                if self.hour == 0:
                    self.hour = 12
            elif self.selected_hand == 'minute':
                self.minute = int(angle / 6) % 60

            self.update()

    def mouseReleaseEvent(self, event):
        self.selected_hand = None  # Сбрасываем выбор стрелки

class TimeInputApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Циферблат для ввода времени")

        layout = QVBoxLayout()

        self.clock = ClockWidget()
        self.label = QLabel("Выбранное время: 12:00")
        self.button = QPushButton("Сбросить время")

        layout.addWidget(self.clock)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

        # Таймер для обновления времени
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(100)

        # Подключение кнопки
        self.button.clicked.connect(self.reset_time)

    def update_time(self):
        self.label.setText(f"Выбранное время: {self.clock.hour:02d}:{self.clock.minute:02d}")

    def reset_time(self):
        self.clock.hour = 12
        self.clock.minute = 0
        self.update_time()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeInputApp()
    window.show()
    sys.exit(app.exec())
