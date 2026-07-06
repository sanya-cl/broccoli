import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import numpy as np  # pip install numpy


class FunctionPlotter(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Визуализатор графиков функций")
        self.setGeometry(100, 100, 800, 600)

        # Центральный виджет
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        # Панель ввода
        input_layout = QtWidgets.QHBoxLayout()
        self.func_input = QtWidgets.QLineEdit()
        self.func_input.setPlaceholderText("Введите функцию: x**2, sin(x), 2*x+5, log(x), etc.")
        self.func_input.setText("x**2")  # пример по умолчанию
        self.plot_btn = QtWidgets.QPushButton("Построить график")
        input_layout.addWidget(QtWidgets.QLabel("f(x) ="))
        input_layout.addWidget(self.func_input)
        input_layout.addWidget(self.plot_btn)
        layout.addLayout(input_layout)

        # Виджет для графика
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)  # сглаживание
        layout.addWidget(self.chart_view)

        # Подключаем кнопку
        self.plot_btn.clicked.connect(self.plot_function)

        # Строим первый график
        self.plot_function()

    def plot_function(self):
        """Строит график функции, введённой пользователем"""
        try:
            # Получаем формулу из поля ввода
            formula = self.func_input.text()

            # Создаём безопасное пространство для eval
            safe_dict = {
                'x': 0, 'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                'log': np.log, 'log10': np.log10, 'exp': np.exp,
                'sqrt': np.sqrt, 'abs': np.abs, 'pi': np.pi, 'e': np.e
            }

            # Генерируем точки для графика (от -10 до 10)
            x_vals = np.linspace(-10, 10, 1000)
            y_vals = []

            for x in x_vals:
                safe_dict['x'] = x
                y = eval(formula, {"__builtins__": {}}, safe_dict)
                # Ограничиваем y, чтобы график не улетал в бесконечность
                if abs(y) > 100:
                    y = None  # пропускаем выбросы
                y_vals.append(y)

            # Создаём серию данных
            series = QLineSeries()
            series.setPen(QPen(Qt.blue, 2))  # синяя линия толщиной 2

            for x, y in zip(x_vals, y_vals):
                if y is not None and not np.isnan(y) and not np.isinf(y):
                    series.append(x, y)

            # Создаём график
            chart = QChart()
            chart.addSeries(series)
            chart.setTitle(f"f(x) = {formula}")
            chart.setAnimationOptions(QChart.SeriesAnimations)

            # Настраиваем оси
            axis_x = QValueAxis()
            axis_x.setTitleText("x")
            axis_x.setRange(-10, 10)
            axis_x.setLabelFormat("%.1f")

            axis_y = QValueAxis()
            axis_y.setTitleText("y")
            # Автоматический диапазон по y
            axis_y.setTitleText("y")

            chart.addAxis(axis_x, Qt.AlignBottom)
            chart.addAxis(axis_y, Qt.AlignLeft)
            series.attachAxis(axis_x)
            series.attachAxis(axis_y)

            # Настраиваем отображение
            chart.legend().hide()
            chart.setTheme(QChart.ChartThemeDark)

            self.chart_view.setChart(chart)

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось построить график:\n{str(e)}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = FunctionPlotter()
    window.show()
    sys.exit(app.exec_())
