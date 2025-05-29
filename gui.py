import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QGraphicsDropShadowEffect, QFrame
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QObject, QTimer, QEasingCurve, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush
import speech_recognition as sr
from compiler import compile_rule
from rules import map_command_to_dsl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import pyqtProperty

class SpeechWorker(QObject):
    result_signal = pyqtSignal(str, str)
    finished = pyqtSignal()

    def run(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening... Please speak your command.")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"Recognized: {command}")
            mapped = map_command_to_dsl(command)
            compiled = compile_rule(mapped)
            self.result_signal.emit(command, compiled)
        except sr.UnknownValueError:
            self.result_signal.emit("Could not understand audio.", "")
        except sr.RequestError:
            self.result_signal.emit("API request failed.", "")
        self.finished.emit()

class GlowCircle(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setVisible(False)

        # Shadow effect for glow
        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(40)
        glow.setColor(QColor(100, 255, 100))
        glow.setOffset(0)
        self.setGraphicsEffect(glow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        green = QColor(100, 255, 100, 180)  # semi-transparent green
        painter.setBrush(QBrush(green))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())

class AudioVisualizer(QWidget):
    """ Pulsating circle for listening state,
        solid circle for recognized state.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(100)
        self.state = "idle"  # idle, listening, recognized
        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setStartValue(30)
        self.pulse_anim.setEndValue(45)
        self.pulse_anim.setDuration(1000)
        self.pulse_anim.setLoopCount(-1)
        self.pulse_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self._pulse_radius = 30

    def get_pulse_radius(self):
        return self._pulse_radius

    def set_pulse_radius(self, val):
        self._pulse_radius = val
        self.update()

    pulse_radius = property(get_pulse_radius, set_pulse_radius)

    def set_state(self, state):
        self.state = state
        if state == "listening":
            self.pulse_anim.start()
        else:
            self.pulse_anim.stop()
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center = self.rect().center()

        if self.state == "listening":
            color = QColor(100, 255, 100, 180)
            radius = self._pulse_radius
        elif self.state == "recognized":
            color = QColor(100, 255, 100, 255)
            radius = 40
        else:  # idle or other
            color = QColor(150, 150, 150, 100)
            radius = 30

        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, radius, radius)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IoT Voice Command Center")
        self.setStyleSheet("background-color: #2E3440; color: #D8DEE9;")
        self.initUI()
        self.showMaximized()

        # Thread setup
        self.thread = QThread()
        self.worker = SpeechWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.result_signal.connect(self.update_gui)
        self.worker.finished.connect(self.thread.quit)

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("IoT Voice Command Center")
        title_font = QFont("Segoe UI", 28, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #81A1C1; margin-bottom: 40px;")
        main_layout.addWidget(title)

        # Command display
        self.command_label = QLabel("Command: ")
        self.command_label.setWordWrap(True)
        self.command_label.setFont(QFont("Segoe UI", 18))
        self.command_label.setStyleSheet("border: 2px solid #4C566A; padding: 20px; border-radius: 10px;")
        main_layout.addWidget(self.command_label, stretch=0)

        # Compiled output display
        self.dsl_output_label = QLabel("Compiled Result: ")
        self.dsl_output_label.setWordWrap(True)
        self.dsl_output_label.setFont(QFont("Segoe UI", 18))
        self.dsl_output_label.setStyleSheet("border: 2px solid #4C566A; padding: 20px; border-radius: 10px;")
        main_layout.addWidget(self.dsl_output_label, stretch=0)

        # Spacer
        main_layout.addStretch()

        # Input area and buttons
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your automation rule here...")
        self.input_field.setFont(QFont("Segoe UI", 16))
        self.input_field.setStyleSheet(
            "padding: 15px; border-radius: 10px; border: 2px solid #4C566A; color: #ECEFF4;"
            "background-color: #3B4252;"
        )
        input_layout.addWidget(self.input_field)

        self.btn_compile = QPushButton("Compile Text")
        self.btn_compile.setCursor(Qt.PointingHandCursor)
        self.btn_compile.setStyleSheet(self.button_style())
        self.btn_compile.setFixedHeight(50)
        self.btn_compile.clicked.connect(self.handle_text_input)
        input_layout.addWidget(self.btn_compile)

        main_layout.addLayout(input_layout)

        self.btn_speak = QPushButton("Speak Command")
        self.btn_speak.setCursor(Qt.PointingHandCursor)
        self.btn_speak.setFixedHeight(50)
        self.btn_speak.setStyleSheet(self.button_style())
        self.btn_speak.clicked.connect(self.handle_voice_input)
        main_layout.addWidget(self.btn_speak)

        # Status label
        self.status_label = QLabel("Status: Waiting for input")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 14))
        self.status_label.setStyleSheet("color: #88C0D0; margin-top: 20px;")
        main_layout.addWidget(self.status_label)

        # Glow circle for light effect
        self.glow_circle = GlowCircle(self)
        self.glow_circle.move(self.width()//2 - 100, self.height()//2 - 100)
        self.glow_circle.hide()

        # Audio visualizer at bottom
        self.audio_visualizer = AudioVisualizer()
        main_layout.addWidget(self.audio_visualizer)

        self.setLayout(main_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Keep glow circle centered
        self.glow_circle.move(self.width()//2 - self.glow_circle.width()//2, self.height()//2 - self.glow_circle.height()//2)

    def button_style(self):
        return """
        QPushButton {
            background-color: #5E81AC;
            color: white;
            border-radius: 12px;
            font-size: 16px;
            padding: 12px 20px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #81A1C1;
        }
        QPushButton:pressed {
            background-color: #4C566A;
        }
        """

    def handle_text_input(self):
        rule = self.input_field.text()
        if rule.strip():
            self.command_label.setText(f"Command: {rule}")
            mapped = map_command_to_dsl(rule)
            result = compile_rule(mapped)
            self.dsl_output_label.setText(f"Compiled Result: {result}")
            self.status_label.setText("Text input compiled successfully")
            self.input_field.clear()
            self.update_light_status(rule)
            self.audio_visualizer.set_state("idle")
        else:
            self.status_label.setText("Please enter a valid automation rule.")

    def handle_voice_input(self):
        self.status_label.setText("Listening... Please speak now.")
        self.audio_visualizer.set_state("listening")
        self.btn_speak.setEnabled(False)
        self.thread.start()

    def update_gui(self, command, compiled):
        self.command_label.setText(f"Command: {command}")
        self.dsl_output_label.setText(f"Compiled Result: {compiled}")
        self.status_label.setText("Voice command compiled successfully")
        self.btn_speak.setEnabled(True)
        self.update_light_status(command)
        self.audio_visualizer.set_state("recognized")

    def update_light_status(self, command):
        command = command.lower()
        if "turn on" in command:
            self.glow_circle.setVisible(True)
        elif "turn off" in command:
            self.glow_circle.setVisible(False)
        else:
            self.glow_circle.setVisible(False)

            
class AudioVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.state = "idle"  # idle, listening, recognized
        self._pulse_radius = 30

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setStartValue(30)
        self.pulse_anim.setEndValue(45)
        self.pulse_anim.setDuration(1000)
        self.pulse_anim.setLoopCount(-1)
        self.pulse_anim.setEasingCurve(QEasingCurve.InOutQuad)

    def get_pulse_radius(self):
        return self._pulse_radius

    def set_pulse_radius(self, val):
        self._pulse_radius = val
        self.update()

    pulse_radius = pyqtProperty(int, get_pulse_radius, set_pulse_radius)

    def set_state(self, state):
        self.state = state
        if state == "listening":
            self.pulse_anim.start()
        else:
            self.pulse_anim.stop()
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center = self.rect().center()

        if self.state == "listening":
            color = QColor(100, 255, 100, 180)
            radius = self._pulse_radius
        elif self.state == "recognized":
            color = QColor(100, 255, 100, 255)
            radius = 40
        else:
            color = QColor(150, 150, 150, 100)
            radius = 30

        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, radius, radius)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.showMaximized()  # already called in MainWindow.__init__
    window.show()
    sys.exit(app.exec_())
