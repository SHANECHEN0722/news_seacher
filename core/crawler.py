"""
新闻爬取模块
"""
from newspaper import Article
from fuzzywuzzy import fuzz
from config import SIMILARITY_THRESHOLD


class NewsCrawler:
    """新闻爬虫"""
    
    # 难以爬取的网站黑名单
    BLOCKED_DOMAINS = [
        # 'zhihu.com',
        # 'weibo.com',
        # 'twitter.com',
        # 'facebook.com',
        # 'instagram.com',
        # 'youtube.com',
        # 'bilibili.com',
        # 'douyin.com'
    ]
    
    @classmethod
    def is_blocked_domain(cls, url):
        """检查URL是否在黑名单中"""
        return any(domain in url for domain in cls.BLOCKED_DOMAINS)
    
    @classmethod
    def crawl_article(cls, url):
        """爬取单篇文章"""
        # 过滤黑名单网站
        if cls.is_blocked_domain(url):
            print(f" [!] 跳过黑名单网站: {url}")
            return None
        
        try:
            print(f" [→] 正在爬取: {url}")
            article = Article(url)  # 不指定语言，让 newspaper 自动检测
            article.download()
            article.parse()
            
            if len(article.text) > 200:
                print(f" [✓] 成功: {article.title[:50]}... ({len(article.text)} 字)")
                return {
                    "url": url,
                    "title": article.title,
                    "text": article.text
                }
            else:
                print(f" [!] 内容太短 ({len(article.text)} 字): {url}")
        except Exception as e:
            print(f" [!] 爬取失败: {url}")
            print(f"     错误: {str(e)[:100]}")
        
        return None
    
    @classmethod
    def crawl_articles(cls, urls, use_dynamic=False):
        """
        批量爬取文章
        
        Args:
            urls: URL列表
            use_dynamic: 是否使用动态爬虫（Selenium）
        """
        articles = []
        failed_urls = []
        
        # 第一轮：使用静态爬虫
        for url in urls:
            article = cls.crawl_article(url)
            if article:
                articles.append(article)
            else:
                failed_urls.append(url)
        
        # 第二轮：如果启用动态爬虫且有失败的URL，尝试用Selenium
        if use_dynamic and failed_urls:
            print(f"\n🔄 [Dynamic] 尝试用动态爬虫重新爬取 {len(failed_urls)} 个失败的链接...")
            try:
                from core.dynamic_crawler import DynamicCrawler
                
                for url in failed_urls:
                    article = DynamicCrawler.crawl_article(url)
                    if article:
                        articles.append(article)
            except ImportError:
                print("⚠️ 动态爬虫未安装，跳过。运行: pip install selenium")
            except Exception as e:
                print(f"⚠️ 动态爬虫失败: {e}")
        
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
