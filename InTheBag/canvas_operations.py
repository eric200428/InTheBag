from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QRectF

class DiscCanvas(QWidget):
    """
    This class handles drawing discs and flipping them on a custom QWidget.
    """
    def __init__(self):
        super().__init__()
        self.results = []
        self.flipped_states = {}  # Track whether each disc is flipped

    def draw_discs(self, results):
        """
        Store results and trigger a repaint to draw discs.
        """
        self.results = results
        self.flipped_states = {index: True for index, _ in enumerate(results)}  # Initialize all discs as unflipped (showing names)
        self.update()

    def paintEvent(self, a0):  # Changed parameter name to "a0" to match PyQt5 expectations
        """
        Overriding the paint event to draw discs.
        """
        if not self.results:
            print("No results to draw")  # Debugging print
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        x_pos, y_pos = 75, 100  # Starting position for the first disc
        disc_radius = 75
        spacing = 50

        for index, row in enumerate(self.results):
            disc_name = row[1]  # Disc model name
            flight_details = f"Spd: {row[2]}\nGld: {row[3]}\nTrn: {row[4]}\nFde: {row[5]}"  # Flight details

            print(f"Drawing disc: {disc_name} at position ({x_pos}, {y_pos})")  # Debugging print for each disc

            # Draw disc (circle)
            rect = QRectF(x_pos, y_pos, disc_radius * 2, disc_radius * 2)
            painter.setBrush(QBrush(QColor("lightGray")))  # Using QColor for the light gray color
            painter.setPen(QPen(QColor("black"), 2))  # Using QColor for the black pen color
            painter.drawEllipse(rect)

            # Draw disc name or flight details based on the flip state
            if self.flipped_states.get(index, True):
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, disc_name)
            else:
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, flight_details)

            # Adjust position for the next disc
            x_pos += disc_radius * 2 + spacing

            if (index + 1) % 4 == 0:
                x_pos = 75
                y_pos += disc_radius * 2 + spacing

        # Adjust the widget size to fit all discs
        self.setMinimumSize(x_pos + disc_radius * 2, y_pos + disc_radius * 2)

    def mousePressEvent(self, a0):
        """
        Handle mouse click events to flip the discs.
        """
        x_pos, y_pos = 75, 100  # Starting position for the first disc
        disc_radius = 75
        spacing = 50

        # Check where the user clicked
        for index, _ in enumerate(self.results):
            rect = QRectF(x_pos, y_pos, disc_radius * 2, disc_radius * 2)

            if a0 is not None and rect.contains(a0.pos()):  # Use a0 instead of event to avoid the warning
                # Toggle the flipped state of the disc
                self.flipped_states[index] = not self.flipped_states.get(index, True)
                print(f"Flipping disc at index {index}. New state: {self.flipped_states[index]}")

                # Trigger a repaint to show the updated state
                self.update()

            # Adjust position for the next disc
            x_pos += disc_radius * 2 + spacing
            if (index + 1) % 4 == 0:
                x_pos = 75
                y_pos += disc_radius * 2 + spacing
