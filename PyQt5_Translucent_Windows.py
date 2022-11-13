import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QEvent, QObject


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()

        # To save mouse relative position.
        self.mouse_relative_position_x = 0
        self.mouse_relative_position_y = 0

        # Create the stylesheet to apply to the button.
        button_style = "color: rgb(255, 255, 255);" \
                       "background-color: rgba(6, 104, 249, 255);" \
                       "border-color: rgba(151, 222, 247, 50);" \
                       "border-width: 1px;" \
                       "border-radius: 5px;"

        # Create the stylesheet to apply to the window.
        # To make the window transparent, set the background-color
        # alpha channel to 2. Notice, that the minimum value for the
        # alpha channel is 2, lower than this value doesn't work.
        widget_stylesheet = "border-color: rgba(255, 0, 0, 255);" \
                            "border-style: solid;" \
                            "border-width: 2px;" \
                            "border-radius: 2px;" \
                            "background-color: rgba(255, 255, 255, 2);"

        # Create an instance of a QPushButton.
        button = QPushButton("Close")
        button.setFixedSize(85, 30)
        button.setStyleSheet(button_style)

        # When button is clicked, then close the window.
        button.clicked.connect(self.close)

        # Create an instance of a QHBoxLayout.
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch(1)
        horizontal_layout.addWidget(button)
        horizontal_layout.addStretch(1)

        # Create an instance of a QVBoxLayout.
        vert_layout = QVBoxLayout()
        vert_layout.addStretch(1)
        vert_layout.addLayout(horizontal_layout)

        # Create the central widget.
        central_widget = QWidget(self)
        central_widget.setLayout(vert_layout)
        central_widget.setStyleSheet(widget_stylesheet)
        central_widget.setMouseTracking(True)
        central_widget.installEventFilter(self)
        central_widget.setFixedSize(300, 200)
        # Sets the given widget to be the main window's central widget.
        self.setCentralWidget(central_widget)

    # Override method mouseReleaseEvent for class MainWindow.
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Change the mouse cursor to be the standard arrow cursor.
            QApplication.setOverrideCursor(Qt.ArrowCursor)

    # Override method mousePressEvent for class MainWindow.
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Get the cursor position relative to the widget that
            # receives the mouse event.
            self.mouse_relative_position_x = event.pos().x()
            self.mouse_relative_position_y = event.pos().y()

    # Override method eventFilter for class MainWindow.
    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        # If the mouse moved.
        if event.type() == QEvent.MouseMove:
            # If the mouse left button was pressed.
            if event.buttons() & Qt.LeftButton:
                # Change the mouse cursor to cursor used for elements that are used to
                # resize top-level windows in any direction.
                QApplication.setOverrideCursor(Qt.SizeAllCursor)
                # Move the widget when the mouse is dragged.
                self.move(event.globalPos().x() - self.mouse_relative_position_x,
                          event.globalPos().y() - self.mouse_relative_position_y)
            else:
                return False
        else:
            return False
        return True


def main():
    # Create a QApplication object. It manages the GUI application's
    # control flow and main settings. It handles widget specific initialization,
    # finalization. For any GUI application using Qt, there is precisely
    # one QApplication object
    app = QApplication(sys.argv)
    # Create an instance of the class MainWindow.
    window = MainWindow()
    # Flag to produce a borderless window.
    # The user cannot move or resize a borderless window via the window system.
    window.setWindowFlags(Qt.FramelessWindowHint)
    # Indicates that the widget should have a translucent background, i.e.,
    # any non-opaque regions of the widgets will be translucent because the widget
    # will have an alpha channel. Setting this flag causes WA_NoSystemBackground
    # to be set.
    window.setAttribute(Qt.WA_TranslucentBackground)
    # Show the window.
    window.show()
    # Start Qt event loop.
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
