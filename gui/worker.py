"""
后台工作线程
"""
from PyQt6.QtCore import QThread, pyqtSignal
from core import NewsSearcher, NewsCrawler, NewsAnalyzer, ReportGenerator


class AnalysisWorker(QThread):
    """分析工作线程"""
    
    log_signal = pyqtSignal(str)
    success_signal = pyqtSignal(str)
    fail_signal = pyqtSignal(str)
    
    def __init__(self, keyword, max_links, timelimit):
        super().__init__()
        self.keyword = keyword
        self.max_links = max_links
        self.timelimit = timelimit
    
    def run(self):
        """Execute analysis workflow"""
        try:
            # 1. Search news
            self.log_signal.emit(f"🔍 Searching for '{self.keyword}'...")
            links = NewsSearcher.search(self.keyword, self.max_links, self.timelimit)
            
            if not links:
                self.fail_signal.emit("No news links found")
                return
            
            self.log_signal.emit(f"✅ Found {len(links)} links")
            
            # 2. Crawl articles
            self.log_signal.emit("📄 Crawling articles...")
            articles = NewsCrawler.crawl_articles(links)
            
            if not articles:
                self.fail_signal.emit("Failed to crawl articles")
                return
            
            self.log_signal.emit(f"✅ Crawled {len(articles)} articles")
            
            # 3. Deduplication
            self.log_signal.emit("🔄 Deduplicating...")
            unique_articles = NewsCrawler.deduplicate(articles)
            
            if not unique_articles:
                self.fail_signal.emit("No articles after deduplication")
                return
            
            self.log_signal.emit(f"✅ Deduplication complete, {len(unique_articles)} articles remaining")
            
            # 4. AI Analysis
            self.log_signal.emit("✨ Running AI analysis...")
            data = NewsAnalyzer.analyze(unique_articles, self.keyword)
            
            if isinstance(data, str):
                self.fail_signal.emit(f"AI analysis failed: {data}")
                return
            
            self.log_signal.emit("✅ AI analysis complete")
            
            # 5. Generate report
            self.log_signal.emit("📝 Generating HTML report...")
            report_path = ReportGenerator.generate(self.keyword, data)
            
            self.success_signal.emit(report_path)
            
        except Exception as e:
            self.fail_signal.emit(f"Exception: {str(e)}")
