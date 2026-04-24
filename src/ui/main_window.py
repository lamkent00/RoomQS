import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from shapely.geometry import Polygon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RoomQS")
        self.resize(400, 300)

        central_widget = QWidget()
        layout = QVBoxLayout()

        # Test PySide6 label
        label_ui = QLabel("PySide6 Window Loaded Successfully!")
        layout.addWidget(label_ui)

        # Test Shapely import and geometry
        try:
            poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
            area = poly.area
            label_shapely = QLabel(f"Shapely Loaded! Polygon area: {area}")
            label_shapely.setStyleSheet("color: green;")
        except Exception as e:
            label_shapely = QLabel(f"Shapely Error: {str(e)}")
            label_shapely.setStyleSheet("color: red;")

        layout.addWidget(label_shapely)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


def run_ui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
