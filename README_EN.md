# AI News Event Analysis System

An intelligent news aggregation and analysis tool powered by DeepSeek-V3, implementing Map-Reduce architecture for automated multi-source news collection, deduplication, summarization, and visualization report generation.

[中文文档](README.md) | **English**

## Features

- 🔍 **Multi-Source Search**: Supports Google + Baidu News + Bing triple-engine intelligent search (Google Cookie configurable)
- 📄 **Smart Crawling**: Dual-mode crawling with static (Newspaper3k) and dynamic (Selenium) crawlers
- 🧹 **Fuzzy Deduplication**: Intelligent title deduplication based on FuzzyWuzzy (85% threshold)
- 🤖 **AI Analysis**: DeepSeek-V3 powered Map-Reduce summarization
- 📊 **Visual Reports**: Generates beautiful dark-themed HTML reports
- 🖥️ **GUI Interface**: User-friendly interface based on PyQt6
- 🚀 **Auto Fallback**: Automatically switches to dynamic crawler when static crawler fails

## Project Structure

```
news_analyzer/
├── main.py                 # Program entry
├── config.py              # Configuration management
├── requirements.txt       # Dependencies
├── .env                   # Environment variables (create manually)
├── core/                  # Core modules
│   ├── __init__.py
│   ├── searcher.py        # News search
│   ├── crawler.py         # Article crawling & deduplication
│   ├── analyzer.py        # AI analysis (Map-Reduce)
│   └── reporter.py        # HTML report generation
├── gui/                   # GUI modules
│   ├── __init__.py
│   ├── window.py          # Main window
│   └── worker.py          # Background worker thread
├── templates/             # Template files
│   └── report_template.py # HTML report template
└── reports/               # Generated reports (auto-created)
    └── *.html             # HTML report files
```

## Installation

1. Clone the project
```bash
git clone https://github.com/SHANECHEN0722/news_seacher.git
cd news_analyzer
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure API Key

Create a `.env` file and add:
```
OPENAI_API_KEY="sk-your-deepseek-api-key"

# Optional: Add Google Cookie for Google search
# GOOGLE_COOKIE="your-google-cookie-here"
```

### How to Get Google Cookie (Optional)

If you want to use Google search, you need to configure Cookie:

1. Open your browser and visit https://www.google.com
2. Open Developer Tools (F12)
3. Switch to the Network tab
4. Search for anything on Google
5. Find the first request and check Request Headers
6. Copy the complete Cookie value
7. Add to `.env` file:
   ```
   GOOGLE_COOKIE="NID=xxx; 1P_JAR=xxx; ..."
   ```

**Note**: Cookies expire. If Google search fails, you may need to update the Cookie.

## Usage

Run the main program:
```bash
python main.py
```

Or:
```bash
python3 main.py
```

## About Search Engines

This project supports three search engines:

### 🔍 Search Engine Priority

1. **Google** (requires Cookie configuration)
   - ✅ Highest search quality
   - ✅ Wide international news coverage
   - ⚠️ Requires Cookie configuration (see above)
   - ⚠️ Cookie expires, needs periodic updates

2. **Baidu News** (default)
   - ✅ Stable and reliable, no configuration needed
   - ✅ Good Chinese news quality
   - ✅ No Cookie or API Key required

3. **Bing** (backup)
   - ✅ Last resort option
   - ⚠️ May be limited by anti-crawling

### 💡 Recommended Configuration

- **Daily Use**: Don't configure GOOGLE_COOKIE, use Baidu (stable)
- **Quality Priority**: Configure GOOGLE_COOKIE, prioritize Google
- **International News**: Configure GOOGLE_COOKIE, Google has better international coverage

## Workflow

1. **Search Phase**: Intelligently combine Google, Baidu News, and Bing to search for relevant news links (auto-deduplication)
2. **Crawl Phase**: Extract article titles and content using Newspaper3k
3. **Deduplication Phase**: Remove duplicate articles using fuzzy matching algorithm
4. **Map Phase**: Generate independent summaries for each article
5. **Reduce Phase**: Consolidate all summaries and extract key information
6. **Report Generation**: Generate HTML report with summary, themes, entities, and timeline, saved to `reports/` directory

## Output

All generated HTML reports are saved in the `reports/` directory with the filename format:
```
{keyword}_{timestamp}.html
```

Example: `CHINA_20251118_211030.html`

## Tech Stack

- **AI Model**: DeepSeek-V3
- **GUI Framework**: PyQt6
- **Crawler Libraries**: Newspaper3k (Static), Selenium (Dynamic), BeautifulSoup4
- **Search Engines**: Google Search, Baidu News, Bing Search
- **Deduplication Algorithm**: FuzzyWuzzy (Levenshtein Distance)
- **Architecture Pattern**: Map-Reduce

## License

MIT License

## Author

Shane
