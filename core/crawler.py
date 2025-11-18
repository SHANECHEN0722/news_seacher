"""
新闻爬取模块
"""
from newspaper import Article
from fuzzywuzzy import fuzz
from config import SIMILARITY_THRESHOLD


class NewsCrawler:
    """新闻爬虫"""
    
    @staticmethod
    def crawl_article(url):
        """爬取单篇文章"""
        try:
            article = Article(url, language='zh')
            article.download()
            article.parse()
            
            if len(article.text) > 200:
                return {
                    "url": url,
                    "title": article.title,
                    "text": article.text
                }
        except Exception as e:
            print(f" [!] 爬取失败: {url} - {e}")
        
        return None
    
    @classmethod
    def crawl_articles(cls, urls):
        """批量爬取文章"""
        articles = []
        
        for url in urls:
            article = cls.crawl_article(url)
            if article:
                articles.append(article)
        
        return articles
    
    @staticmethod
    def deduplicate(articles):
        """使用模糊匹配去重"""
        unique_articles = []
        seen_titles = []
        
        print(f"🔍 [Cleaning] 正在去重处理 {len(articles)} 篇文章...")
        
        for article in articles:
            is_duplicate = False
            
            for seen_title in seen_titles:
                similarity = fuzz.token_sort_ratio(article['title'], seen_title)
                if similarity > SIMILARITY_THRESHOLD:
                    is_duplicate = True
                    print(f" [!] 剔除重复内容 (相似度 {similarity}%): {article['title']}")
                    break
            
            if not is_duplicate:
                unique_articles.append(article)
                seen_titles.append(article['title'])
        
        print(f"✅ [Cleaning] 去重完成. 剩余 {len(unique_articles)} 篇独立文章.")
        return unique_articles
