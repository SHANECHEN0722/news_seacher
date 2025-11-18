"""
GUI 主窗口
"""
import sys
import subprocess
import webbrowser
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit, QLabel, QSpinBox, QComboBox
)
from PyQt6.QtCore import Qt
from .worker import AnalysisWorker


class NewsAnalyzerWindow(QMainWindow):
    """新闻分析器主窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("AI News Event Analysis System")
        self.setFixedSize(600, 550)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel("🤖 AI News Event Analysis System")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #1e3a8a; margin-bottom: 5px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Search: Baidu + Google + Bing | AI Model: DeepSeek-V3 | Architecture: Map-Reduce")
        subtitle_label.setStyleSheet("font-size: 11px; color: #666; margin-bottom: 10px;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        # Input
        input_layout = QHBoxLayout()
        input_label = QLabel("Event Keyword:")
        self.event_input = QLineEdit()
        self.event_input.setPlaceholderText("e.g., AI breakthrough 2025")
        self.event_input.setStyleSheet("padding: 8px;")
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.event_input)
        main_layout.addLayout(input_layout)
        
        # Options
        options_layout = QHBoxLayout()
        num_label = QLabel("Articles:")
        self.num_spin = QSpinBox()
        self.num_spin.setRange(3, 15)
        self.num_spin.setValue(5)
        
        time_label = QLabel("Time Range:")
        self.timelimit_combo = QComboBox()
        self.timelimit_combo.addItems(["Any Time", "Past Week", "Past Month"])
        
        options_layout.addWidget(num_label)
        options_layout.addWidget(self.num_spin)
        options_layout.addSpacing(20)
        options_layout.addWidget(time_label)
        options_layout.addWidget(self.timelimit_combo)
        main_layout.addLayout(options_layout)
        
        # Button
        self.generate_btn = QPushButton("🚀 Start Analysis")
        self.generate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #8b5cf6);
                color: white; border: none;
                padding: 14px; font-size: 15px; border-radius: 8px; font-weight: bold;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #7c3aed); 
            }
            QPushButton:disabled { background-color: #6c757d; }
        """)
        self.generate_btn.clicked.connect(self.start_analysis)
        main_layout.addWidget(self.generate_btn)
        
        # Log
        log_label = QLabel("System Log:")
        main_layout.addWidget(log_label)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            background-color: #f8f9fa; border: 1px solid #dee2e6;
            padding: 8px; font-family: 'Menlo', 'Consolas', monospace; font-size: 12px;
        """)
        main_layout.addWidget(self.log_text)
    
    def start_analysis(self):
        """Start analysis"""
        keyword = self.event_input.text().strip()
        if not keyword:
            self.log_text.append("❌ Error: Please enter an event keyword!")
            return
        
        self.generate_btn.setEnabled(False)
        self.generate_btn.setText("⏳ Analyzing...")
        self.log_text.clear()
        self.log_text.append("=" * 50)
        self.log_text.append(f"🎯 Target: {keyword}")
        self.log_text.append("=" * 50)
        
        # 启动工作线程
        self.worker = AnalysisWorker(
            keyword, 
            self.num_spin.value(), 
            'a'
        )
        self.worker.log_signal.connect(self.update_log)
        self.worker.success_signal.connect(self.on_success)
        self.worker.fail_signal.connect(self.on_fail)
        self.worker.start()
    
    def update_log(self, message):
        """更新日志"""
        self.log_text.append(message)
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def on_success(self, report_path):
        """Analysis successful"""
        self.log_text.append("-" * 30)
        self.log_text.append(f"🎉 Task completed! Report generated:\n{report_path}")
        self.log_text.append("Opening browser...")
        
        try:
            if sys.platform == 'darwin':
                subprocess.run(['open', report_path], check=True)
            else:
                webbrowser.open(f"file://{report_path}")
        except Exception as e:
            self.log_text.append(f" [!] Cannot open browser: {e}")
        
        self.reset_ui()
    
    def on_fail(self, error):
        """Analysis failed"""
        self.log_text.append("-" * 30)
        self.log_text.append(f"❌ Task failed: {error}")
        self.reset_ui()
    
    def reset_ui(self):
        """Reset UI"""
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("🚀 Start Analysis")
