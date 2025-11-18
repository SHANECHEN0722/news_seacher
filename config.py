"""
配置管理模块
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# API 配置
API_KEY = os.getenv("OPENAI_API_KEY")
API_BASE_URL = "https://api.deepseek.com"

# DeepSeek 客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE_URL
)

# 搜索配置
SEARCH_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.baidu.com'
}

# Google 搜索配置（可选）
# 如果需要使用 Google 搜索，请在 .env 文件中添加 GOOGLE_COOKIE
GOOGLE_COOKIE = os.getenv("GOOGLE_COOKIE", "").strip().replace('\n', '').replace('\r', '')

# 去重配置
SIMILARITY_THRESHOLD = 85  # 文章标题相似度阈值

# AI 配置
AI_MODEL = "deepseek-chat"
AI_TEMPERATURE = 0.3
