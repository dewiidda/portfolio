import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider, QLineEdit, QTextEdit, QFileDialog, QComboBox
)
from PyQt5.QtCore import QTimer, Qt
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import animation
from algorithms import bubble_sort, linear_search

class VisualizerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Algorithmic Logic Visualizer")
        self.algorithms = {"Bubble Sort": bubble_sort, "Linear Search": linear_search}
        self.current_algorithm = bubble_sort
        self.data = list(range(1, 21))
        random.shuffle(self.data)
        self.interval = 200 

        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout()
        central.setLayout(vbox)

        self.fig = Figure(figsize=(6,4))
        self.canvas = FigureCanvas(self.fig)
        vbox.addWidget(self.canvas)
        self.ax = self.fig.add_subplot(111)

        controls = QHBoxLayout()
        vbox.addLayout(controls)
        self.algo_select = QComboBox()
        self.algo_select.addItems(list(self.algorithms.keys()))
        self.algo_select.currentTextChanged.connect(self.change_algorithm)
        controls.addWidget(QLabel("Pilih Algoritma:"))
        controls.addWidget(self.algo_select)

        self.shuffle_btn = QPushButton("Acak Data")
        self.shuffle_btn.clicked.connect(self.shuffle_data)
        controls.addWidget(self.shuffle_btn)

        controls.addWidget(QLabel("Kecepatan:"))
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(50)
        self.speed_slider.setMaximum(1000)
        self.speed_slider.setValue(self.interval)
        self.speed_slider.valueChanged.connect(self.change_speed)
        controls.addWidget(self.speed_slider)

        self.start_btn = QPushButton("Mulai")
        self.start_btn.clicked.connect(self.animate)
        controls.addWidget(self.start_btn)

        self.draw_initial()

    def draw_initial(self):
        self.ax.clear()
        self.bar_rects = self.ax.bar(range(len(self.data)), self.data, align="edge", color='skyblue')
        self.ax.set_title(self.algo_select.currentText())
        self.ax.set_xlim(0, len(self.data))
        self.ax.set_ylim(0, max(self.data) + 5)
        self.canvas.draw()

    def change_algorithm(self, text):
        self.current_algorithm = self.algorithms[text]
        self.draw_initial()

    def shuffle_data(self):
        random.shuffle(self.data)
        self.draw_initial()

    def change_speed(self, value):
        self.interval = value

    def animate(self):
        self.iterator = self.current_algorithm(self.data.copy())
        self.ani = animation.FuncAnimation(
            self.fig, self.update_plot, fargs=(self.bar_rects,),
            frames=self.iterator, interval=self.interval, repeat=False
        )
        self.canvas.draw()
    
    def update_plot(self, arr, bar_rects):
        for rect, h in zip(bar_rects, arr):
            rect.set_height(h)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VisualizerWindow()
    window.show()
    sys.exit(app.exec_())