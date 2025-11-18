"""
动态网页爬取模块（支持JavaScript渲染）
使用 Selenium + Chrome 无头浏览器
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class DynamicCrawler:
    """动态网页爬虫（支持JavaScript）"""
    
    @staticmethod
    def setup_driver():
        """配置Chrome无头浏览器"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        
        try:
            # 尝试使用 webdriver-manager 自动管理驱动
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                print("✅ 使用 webdriver-manager 自动管理驱动")
            except ImportError:
                # 如果没安装 webdriver-manager，使用系统的 chromedriver
                driver = webdriver.Chrome(options=chrome_options)
                print("✅ 使用系统 chromedriver")
            
            return driver
        except Exception as e:
            print(f"⚠️ Chrome驱动初始化失败: {e}")
            print("💡 请运行: pip install selenium webdriver-manager")
            return None
    
    @classmethod
    def crawl_article(cls, url, wait_time=3):
        """
        爬取动态网页
        
        Args:
            url: 网页URL
            wait_time: 等待JavaScript加载的时间（秒）
        """
        driver = None
        try:
            print(f" [→] 正在爬取（动态）: {url}")
            
            driver = cls.setup_driver()
            if not driver:
                return None
            
            # 访问页面
            driver.get(url)
            
            # 等待页面加载
            time.sleep(wait_time)
            
            # 尝试等待主要内容加载（多种可能的标签）
            try:
                WebDriverWait(driver, 10).until(
                    lambda d: d.find_element(By.TAG_NAME, "article") or 
                             d.find_element(By.TAG_NAME, "main") or
                             d.find_elements(By.TAG_NAME, "p")
                )
            except:
                pass  # 继续
            
            # 额外等待，确保动态内容加载完成
            time.sleep(2)
            
            # 获取页面源码
            html = driver.page_source
            
            # 调试：保存HTML看看
            # with open('/tmp/debug_page.html', 'w', encoding='utf-8') as f:
            #     f.write(html)
            # print(f"     调试：HTML已保存到 /tmp/debug_page.html")
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # 提取标题
            title = ""
            title_tags = ['h1', 'h2', 'title']
            for tag in title_tags:
                title_elem = soup.find(tag)
                if title_elem and title_elem.get_text().strip():
                    title = title_elem.get_text().strip()
                    break
            
            # 提取正文 - 简单粗暴的方法
            text = ""
            
            # 方法1：获取所有段落
            paragraphs = soup.find_all('p')
            if paragraphs:
                para_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])
                if len(para_text) > 200:
                    text = para_text
            
            # 方法2：如果段落不够，直接获取body
            if len(text) < 200:
                body = soup.find('body')
                if body:
                    # 只移除script和style
                    for script in body(['script', 'style']):
                        script.decompose()
                    text = body.get_text(separator=' ', strip=True)
            
            # 简单清理：移除多余空格
            text = ' '.join(text.split())
            
            if len(text) > 200:
                print(f" [✓] 成功（动态）: {title[:50]}... ({len(text)} 字)")
                return {
                    "url": url,
                    "title": title or "无标题",
                    "text": text
                }
            else:
                print(f" [!] 内容太短 ({len(text)} 字): {url}")
                # 调试：显示抓到的内容前100字
                if text:
                    print(f"     抓到的内容: {text[:100]}...")
                return None
                
        except Exception as e:
            print(f" [!] 动态爬取失败: {url}")
            print(f"     错误: {str(e)[:100]}")
            return None
        finally:
            if driver:
                driver.quit()
    
    @classmethod
    def crawl_articles(cls, urls, wait_time=3):
        """批量爬取动态网页"""
        articles = []
        
        for url in urls:
            article = cls.crawl_article(url, wait_time)
            if article:
                articles.append(article)
        
        return articles
