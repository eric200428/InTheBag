from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea)
from PyQt5.QtCore import Qt
from .canvas_operations import DiscCanvas  # Import DiscCanvas to draw discs
from .database import execute_query  # Import the database query

class DiscLookupApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Disc Lookup')
        self.setGeometry(100, 100, 1200, 900)
        
        # Create UI components
        self.init_ui()

    def init_ui(self):
        # Manufacturer input
        manufacturer_label = QLabel('Enter Manufacturer:')
        self.manufacturer_input = QLineEdit()

        # Model input
        model_label = QLabel('Enter Model:')
        self.model_input = QLineEdit()

        # Execute query button
        self.execute_button = QPushButton('Execute Query')
        self.execute_button.clicked.connect(self.on_execute_query)

        # Disc display canvas (custom widget)
        self.canvas = DiscCanvas()

        # Scroll area to make the canvas scrollable
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.canvas)

        # Layout for the input fields and button
        input_layout = QHBoxLayout()
        input_layout.addWidget(manufacturer_label)
        input_layout.addWidget(self.manufacturer_input)
        input_layout.addWidget(model_label)
        input_layout.addWidget(self.model_input)
        input_layout.addWidget(self.execute_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def on_execute_query(self):
        manufacturer = self.manufacturer_input.text().strip()
        model = self.model_input.text().strip()

        # Query database for disc results
        results = execute_query(manufacturer, model)

        if results:
            # Pass results to canvas to draw discs
            self.canvas.draw_discs(results)
        else:
            print("No results found.")
