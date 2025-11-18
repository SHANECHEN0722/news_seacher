"""
AI 新闻事件摘要生成器
主程序入口
"""
import sys
from PyQt6.QtWidgets import QApplication, QTextEdit
from config import client
from gui import NewsAnalyzerWindow


def check_api_key():
    """Check API Key configuration"""
    if not client.api_key:
        app = QApplication.instance() or QApplication(sys.argv)
        error_box = QTextEdit()
        error_box.setReadOnly(True)
        error_text = (
            "❌ Fatal Error: API Key not found.\n\n"
            "Please create a .env file in the project directory and add your DeepSeek API Key:\n"
            "OPENAI_API_KEY=\"sk-xxxx...\"\n\n"
            "(Note: This program uses OpenAI SDK to call DeepSeek, so the variable name must be OPENAI_API_KEY)"
        )
        error_box.setText(error_text)
        error_box.setWindowTitle("Configuration Missing")
        error_box.setFixedSize(500, 250)
        error_box.show()
        sys.exit(app.exec())


def main():
    """主函数"""
    check_api_key()
    
    app = QApplication(sys.argv)
    window = NewsAnalyzerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
