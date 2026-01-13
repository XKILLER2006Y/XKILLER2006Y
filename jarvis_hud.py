import sys
import random
import math
import platform
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QProgressBar, QListWidget, QListWidgetItem, QPushButton
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient, QPalette


class StatsWorker(QThread):
    stats_updated = Signal(float, float)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            cpu = random.uniform(10, 90)
            ram = random.uniform(20, 80)
            self.stats_updated.emit(cpu, ram)
            QThread.msleep(50)

    def stop(self):
        self.running = False
        self.wait()
    
    def update_stats_async(self):
        if self.running:
            cpu = random.uniform(10, 90)
            ram = random.uniform(20, 80)
            self.stats_updated.emit(cpu, ram)
            QTimer.singleShot(1000, self.update_stats_async)


class ParticleSphere(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.base_color = QColor(0, 150, 255, 200)
        self.setMinimumSize(300, 300)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rotation)
        self.timer.start(30)
        
        self.init_particles()

    def init_particles(self):
        self.particles = []
        num_particles = 100
        for _ in range(num_particles):
            theta = random.uniform(0, 2 * math.pi)
            phi = random.uniform(0, math.pi)
            r = 80
            x = r * math.sin(phi) * math.cos(theta)
            y = r * math.sin(phi) * math.sin(theta)
            z = r * math.cos(phi)
            self.particles.append([x, y, z])

    def update_rotation(self):
        self.angle_x += 0.01
        self.angle_y += 0.015
        self.update()

    def cleanup(self):
        self.timer.stop()
        self.particles.clear()
        self.angle_x = 0.0
        self.angle_y = 0.0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        cx = self.width() / 2
        cy = self.height() / 2
        
        projected = []
        for px, py, pz in self.particles:
            rx = px
            ry = py * math.cos(self.angle_x) - pz * math.sin(self.angle_x)
            rz = py * math.sin(self.angle_x) + pz * math.cos(self.angle_x)
            
            rx_final = rx * math.cos(self.angle_y) + rz * math.sin(self.angle_y)
            rz_final = -rx * math.sin(self.angle_y) + rz * math.cos(self.angle_y)
            ry_final = ry
            
            rz_clamped = max(-0.95, min(0.95, rz_final / 80))
            depth_factor = 1 / (1.8 - rz_clamped * 0.6)
            sx = cx + rx_final * depth_factor
            sy = cy + ry_final * depth_factor
            
            projected.append((sx, sy, rz_final))
        
        projected.sort(key=lambda p: p[2])
        
        for sx, sy, rz in projected:
            alpha = int(150 + (rz / 80) * 100)
            alpha = max(50, min(255, alpha))
            
            particle_color = QColor(self.base_color)
            particle_color.setAlpha(alpha)
            painter.setPen(Qt.NoPen)
            painter.setBrush(particle_color)
            painter.drawEllipse(int(sx - 3), int(sy - 3), 6, 6)


class ChatBubble(QWidget):
    def __init__(self, message, is_user=True, parent=None):
        super().__init__(parent)
        self.message = message
        self.is_user = is_user
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setMaximumWidth(300)
        
        if is_user:
            self.label.setAlignment(Qt.AlignRight)
            layout.addStretch()
            layout.addWidget(self.label)
            bg_color = "rgba(0, 120, 215, 180)"
            border_style = "border-bottom-left-radius: 3px;"
        else:
            self.label.setAlignment(Qt.AlignLeft)
            layout.addWidget(self.label)
            layout.addStretch()
            bg_color = "rgba(60, 60, 60, 180)"
            border_style = "border-bottom-right-radius: 3px;"
        
        self.label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: white;
                padding: 10px;
                border-radius: 15px;
                {border_style}
            }}
        """)


class JarvisHUD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dragging = False
        self.drag_position = QPoint()
        self.edge_margin = 10
        
        self.init_ui()
        self.init_stats_worker()
        
    def init_ui(self):
        self.setWindowTitle("JARVIS HUD")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("JARVIS HUD")
        header.setStyleSheet("""
            QLabel {
                color: #00BFFF;
                font-size: 24px;
                font-weight: bold;
                background: rgba(0, 0, 0, 150);
                padding: 10px;
                border-radius: 5px;
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        content_layout = QHBoxLayout()
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setStyleSheet("""
            QWidget {
                background: rgba(20, 20, 40, 200);
                border-radius: 10px;
            }
        """)
        
        stats_label = QLabel("System Stats")
        stats_label.setStyleSheet("color: #00BFFF; font-size: 16px; font-weight: bold;")
        left_layout.addWidget(stats_label)
        
        cpu_label = QLabel("CPU Usage:")
        cpu_label.setStyleSheet("color: white;")
        left_layout.addWidget(cpu_label)
        
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00BFFF;
                border-radius: 5px;
                background-color: rgba(0, 0, 0, 100);
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #00BFFF;
            }
        """)
        left_layout.addWidget(self.cpu_bar)
        
        ram_label = QLabel("RAM Usage:")
        ram_label.setStyleSheet("color: white;")
        left_layout.addWidget(ram_label)
        
        self.ram_bar = QProgressBar()
        self.ram_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00FF00;
                border-radius: 5px;
                background-color: rgba(0, 0, 0, 100);
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #00FF00;
            }
        """)
        left_layout.addWidget(self.ram_bar)
        
        self.particle_sphere = ParticleSphere()
        left_layout.addWidget(self.particle_sphere)
        
        left_layout.addStretch()
        
        content_layout.addWidget(left_panel)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_panel.setStyleSheet("""
            QWidget {
                background: rgba(20, 20, 40, 200);
                border-radius: 10px;
            }
        """)
        
        chat_label = QLabel("Communications")
        chat_label.setStyleSheet("color: #00BFFF; font-size: 16px; font-weight: bold;")
        right_layout.addWidget(chat_label)
        
        self.chat_list = QListWidget()
        self.chat_list.setStyleSheet("""
            QListWidget {
                background: rgba(20, 20, 40, 150);
                border: 2px solid #00BFFF;
                border-radius: 5px;
                color: white;
            }
            QListWidget::item {
                background: rgba(20, 20, 40, 100);
                border: none;
            }
        """)
        right_layout.addWidget(self.chat_list)
        
        self.add_chat_message("Hello, I am JARVIS", False)
        self.add_chat_message("Show me system status", True)
        self.add_chat_message("All systems operational", False)
        
        button_layout = QHBoxLayout()
        
        self.fullscreen_btn = QPushButton("Fullscreen")
        self.fullscreen_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 191, 255, 150);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 191, 255, 200);
            }
        """)
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        button_layout.addWidget(self.fullscreen_btn)
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 150);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 200);
            }
        """)
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        right_layout.addLayout(button_layout)
        
        content_layout.addWidget(right_panel)
        
        main_layout.addLayout(content_layout)
    
    def add_chat_message(self, message, is_user):
        bubble = ChatBubble(message, is_user)
        item = QListWidgetItem(self.chat_list)
        item.setSizeHint(bubble.sizeHint())
        self.chat_list.addItem(item)
        self.chat_list.setItemWidget(item, bubble)
    
    def init_stats_worker(self):
        self.stats_worker = StatsWorker()
        self.stats_worker.stats_updated.connect(self.update_stats)
        self.stats_worker.start()
    
    def update_stats(self, cpu, ram):
        if hasattr(self, 'cpu_bar') and self.cpu_bar is not None:
            self.cpu_bar.setValue(int(cpu))
        if hasattr(self, 'ram_bar') and self.ram_bar is not None:
            self.ram_bar.setValue(int(ram))
    
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.fullscreen_btn.setText("Fullscreen")
        else:
            self.showFullScreen()
            self.fullscreen_btn.setText("Exit Fullscreen")
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
    
    def nativeEvent(self, eventType, message):
        if platform.system() == "Windows" and eventType == "windows_generic_MSG":
            try:
                import ctypes
                import ctypes.wintypes
                msg = ctypes.wintypes.MSG.from_address(int(message))
                
                WM_NCHITTEST = 0x0084
                HTCLIENT = 1
                HTCAPTION = 2
                HTLEFT = 10
                HTRIGHT = 11
                HTTOP = 12
                HTTOPLEFT = 13
                HTTOPRIGHT = 14
                HTBOTTOM = 15
                HTBOTTOMLEFT = 16
                HTBOTTOMRIGHT = 17
                
                if msg.message == WM_NCHITTEST:
                    x = msg.lParam & 0xFFFF
                    y = (msg.lParam >> 16) & 0xFFFF
                    
                    rect = self.geometry()
                    
                    if x < self.edge_margin:
                        if y < self.edge_margin:
                            return (True, HTTOPLEFT)
                        elif y > rect.height() - self.edge_margin:
                            return (True, HTBOTTOMLEFT)
                        else:
                            return (True, HTLEFT)
                    elif x > rect.width() - self.edge_margin:
                        if y < self.edge_margin:
                            return (True, HTTOPRIGHT)
                        elif y > rect.height() - self.edge_margin:
                            return (True, HTBOTTOMRIGHT)
                        else:
                            return (True, HTRIGHT)
                    elif y < self.edge_margin:
                        return (True, HTTOP)
                    elif y > rect.height() - self.edge_margin:
                        return (True, HTBOTTOM)
            except Exception:
                pass
        
        return super().nativeEvent(eventType, message)
    
    def closeEvent(self, event):
        self.stats_worker.stop()
        self.particle_sphere.cleanup()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(15, 15, 30))
    palette.setColor(QPalette.WindowText, Qt.white)
    app.setPalette(palette)
    
    window = JarvisHUD()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
