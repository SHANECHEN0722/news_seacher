# AI 新闻事件深度分析系统

基于 DeepSeek-V3 的智能新闻聚合与分析工具，采用 Map-Reduce 架构实现多源新闻的自动采集、去重、摘要与可视化报告生成。

**中文** | [English](README_EN.md)

## 功能特性

- 🔍 **多源搜索**：支持 Google + 百度新闻 + Bing 三引擎智能组合搜索（可配置 Google Cookie）
- 📄 **智能爬取**：使用 Newspaper3k 自动提取文章正文
- 🧹 **模糊去重**：基于 FuzzyWuzzy 的智能标题去重
- 🤖 **AI 分析**：DeepSeek-V3 驱动的 Map-Reduce 摘要生成
- 📊 **可视化报告**：生成精美的深色主题 HTML 报告
- 🖥️ **图形界面**：基于 PyQt6 的友好用户界面

## 项目结构

```
news_analyzer/
├── main.py                 # 程序入口
├── config.py              # 配置管理
├── requirements.txt       # 依赖列表
├── .env                   # 环境变量（需自行创建）
├── core/                  # 核心功能模块
│   ├── __init__.py
│   ├── searcher.py        # 新闻搜索
│   ├── crawler.py         # 文章爬取与去重
│   ├── analyzer.py        # AI 分析（Map-Reduce）
│   └── reporter.py        # HTML 报告生成
├── gui/                   # 图形界面模块
│   ├── __init__.py
│   ├── window.py          # 主窗口
│   └── worker.py          # 后台工作线程
├── templates/             # 模板文件
│   └── report_template.py # HTML 报告模板
└── reports/               # 生成的报告（自动创建）
    └── *.html             # HTML 报告文件
```

## 安装

1. 克隆项目
```bash
git clone https://github.com/SHANECHEN0722/news_seacher.git
cd news_analyzer
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置 API Key

创建 `.env` 文件并添加：
```
OPENAI_API_KEY="sk-your-deepseek-api-key"

# 可选：如果想使用 Google 搜索，添加 Google Cookie
# GOOGLE_COOKIE="your-google-cookie-here"
```

### 如何获取 Google Cookie（可选）

如果想使用 Google 搜索，需要配置 Cookie：

1. 打开浏览器，访问 https://www.google.com
2. 打开开发者工具（F12）
3. 切换到 Network 标签
4. 在 Google 搜索任意内容
5. 找到第一个请求，查看 Request Headers
6. 复制完整的 Cookie 值
7. 添加到 `.env` 文件中：
   ```
   GOOGLE_COOKIE="NID=xxx; 1P_JAR=xxx; ..."
   ```

**注意**：Cookie 会过期，如果 Google 搜索失败，可能需要更新 Cookie。

## 使用方法

运行主程序：
```bash
python main.py
```

或直接运行：
```bash
python3 main.py
```

## 关于搜索引擎

本项目支持三种搜索引擎：

### 🔍 搜索引擎优先级

1. **Google**（需要配置 Cookie）
   - ✅ 搜索质量最高
   - ✅ 国际新闻覆盖广
   - ⚠️ 需要配置 Cookie（见上方说明）
   - ⚠️ Cookie 会过期，需要定期更新

2. **百度新闻**（默认）
   - ✅ 稳定可靠，无需配置
   - ✅ 中文新闻质量好
   - ✅ 不需要 Cookie 或 API Key

3. **Bing**（备用）
   - ✅ 作为最后的备选方案
   - ⚠️ 可能被反爬虫限制

### 💡 推荐配置

- **日常使用**：不配置 GOOGLE_COOKIE，使用百度（稳定）
- **追求质量**：配置 GOOGLE_COOKIE，优先使用 Google
- **国际新闻**：配置 GOOGLE_COOKIE，Google 对国际新闻覆盖更好

## 技术栈

- **AI 模型**：DeepSeek-V3
- **GUI 框架**：PyQt6
- **爬虫库**：Newspaper3k, BeautifulSoup4
- **搜索引擎**：百度新闻, Bing Search
- **去重算法**：FuzzyWuzzy (Levenshtein Distance)
- **架构模式**：Map-Reduce

## 工作流程

1. **搜索阶段**：智能组合 Google、百度新闻、Bing 搜索相关新闻链接（自动去重）
2. **爬取阶段**：使用 Newspaper3k 提取文章标题和正文
3. **去重阶段**：基于模糊匹配算法去除重复文章
4. **Map 阶段**：对每篇文章生成独立摘要
5. **Reduce 阶段**：整合所有摘要，提取关键信息
6. **报告生成**：生成包含摘要、主题、实体、时间线的 HTML 报告，保存到 `reports/` 目录

## 输出说明

所有生成的 HTML 报告都会保存在 `reports/` 目录下，文件名格式为：
```
{关键词}_{时间戳}.html
```

例如：`CHINA_20251118_211030.html`

## 许可证

MIT License

## 作者

Shane
