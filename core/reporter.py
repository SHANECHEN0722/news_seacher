"""
报告生成模块
"""
import os
from datetime import datetime
from templates.report_template import generate_html_content


class ReportGenerator:
    """HTML 报告生成器"""
    
    # 报告输出目录
    OUTPUT_DIR = "reports"
    
    @classmethod
    def _ensure_output_dir(cls):
        """确保输出目录存在"""
        if not os.path.exists(cls.OUTPUT_DIR):
            os.makedirs(cls.OUTPUT_DIR)
            print(f"📁 创建报告目录: {cls.OUTPUT_DIR}/")
    
    @classmethod
    def generate(cls, keyword, data):
        """生成 HTML 报告"""
        # 确保输出目录存在
        cls._ensure_output_dir()
        
        # 生成文件名（包含时间戳避免覆盖）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{keyword}_{timestamp}.html".replace(" ", "_")
        filepath = os.path.join(cls.OUTPUT_DIR, filename)
        
        # 生成 HTML 内容
        html_content = generate_html_content(keyword, data)
        
        # 写入文件
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ 报告已保存: {filepath}")
        return os.path.abspath(filepath)
