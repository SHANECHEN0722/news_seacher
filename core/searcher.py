"""
新闻搜索模块
"""
import requests
import time
from bs4 import BeautifulSoup
from config import SEARCH_HEADERS, GOOGLE_COOKIE


class NewsSearcher:
    """新闻搜索器"""
    
    @staticmethod
    def search_baidu(keyword, max_results=10):
        """使用百度新闻搜索"""
        news_links = []
        
        try:
            print(f"🔍 [Baidu] 正在搜索: {keyword}")
            
            search_url = f"https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd={keyword}"
            response = requests.get(search_url, headers=SEARCH_HEADERS, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='result')
            
            if not results:
                results = soup.find_all('div', class_='c-container')
            
            count = 0
            for result in results:
                if count >= max_results:
                    break
                
                link_tag = result.find('a')
                if link_tag and link_tag.get('href'):
                    url = link_tag.get('href')
                    if 'baidu.com' not in url or 'baijiahao.baidu.com' in url:
                        news_links.append(url)
                        print(f"✅ 找到链接 {count + 1}: {url[:80]}...")
                        count += 1
            
            return news_links
            
        except Exception as e:
            print(f"⚠️ 百度搜索失败: {e}")
            return []
    
    @staticmethod
    def search_google(keyword, max_results=10):
        """使用 Google 搜索（支持 Cookie）"""
        news_links = []
        
        if not GOOGLE_COOKIE:
            print("⚠️ 未配置 GOOGLE_COOKIE，跳过 Google 搜索")
            return []
        
        try:
            print(f"🔍 [Google] 正在搜索: {keyword}")
            
            # Google 搜索 URL
            search_query = f"{keyword} 新闻"
            search_url = f"https://www.google.com.hk/search?q={requests.utils.quote(search_query)}&num={max_results}&hl=zh-CN"
            
            # 模拟浏览器请求头（包含 Cookie）
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cookie': GOOGLE_COOKIE,
                'Referer': 'https://www.google.com/',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
            
            # 发送请求
            response = requests.get(search_url, headers=headers, timeout=15)
            
            if response.status_code != 200:
                print(f"⚠️ Google 返回状态码: {response.status_code}")
                return []
            
            # 解析 HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 方法1：查找 class="yuRUbf" 的 div（Google 搜索结果容器）
            count = 0
            for div in soup.find_all('div', class_='yuRUbf'):
                if count >= max_results:
                    break
                
                a_tag = div.find('a', href=True)
                if a_tag:
                    url = a_tag['href']
                    if url.startswith('http') and not any(x in url for x in [
                        'google.com',
                        'youtube.com',
                        'webcache.googleusercontent.com'
                    ]):
                        news_links.append(url)
                        print(f"✅ 找到链接 {count + 1}: {url[:80]}...")
                        count += 1
            
            # 方法2：如果方法1没找到，尝试查找所有 <a> 标签
            if not news_links:
                print("⚠️ 尝试备用解析方式...")
                for link in soup.find_all('a', href=True):
                    if count >= max_results:
                        break
                    
                    href = link['href']
                    
                    # 提取以 /url?q= 开头的链接
                    if href.startswith('/url?q='):
                        url = href.split('/url?q=')[1].split('&')[0]
                        url = requests.utils.unquote(url)
                        
                        if url.startswith('http') and not any(x in url for x in [
                            'google.com',
                            'youtube.com',
                            'webcache.googleusercontent.com'
                        ]):
                            news_links.append(url)
                            print(f"✅ 找到链接 {count + 1}: {url[:80]}...")
                            count += 1
            
            return news_links
            
        except Exception as e:
            print(f"⚠️ Google 搜索失败: {e}")
            return []
    
    @staticmethod
    def search_bing(keyword, max_results=10):
        """使用 Bing 搜索（更友好的反爬虫策略）"""
        news_links = []
        
        try:
            print(f"🔍 [Bing] 正在搜索: {keyword}")
            
            # Bing 搜索 URL
            search_query = f"{keyword} 新闻"
            search_url = f"https://www.bing.com/search?q={requests.utils.quote(search_query)}&count={max_results * 2}&setlang=zh-CN"
            
            # 模拟浏览器请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Referer': 'https://www.bing.com/'
            }
            
            # 发送请求
            response = requests.get(search_url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"⚠️ Bing 返回状态码: {response.status_code}")
                return []
            
            # 解析 HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Bing 搜索结果通常在 <li class="b_algo"> 中
            count = 0
            for result in soup.find_all('li', class_='b_algo'):
                if count >= max_results:
                    break
                
                # 查找链接
                link = result.find('a', href=True)
                if link:
                    url = link['href']
                    
                    # 过滤掉不相关的链接
                    if url and url.startswith('http') and not any(x in url for x in [
                        'bing.com',
                        'microsoft.com',
                        'youtube.com'
                    ]):
                        news_links.append(url)
                        print(f"✅ 找到链接 {count + 1}: {url[:80]}...")
                        count += 1
            
            return news_links
            
        except Exception as e:
            print(f"⚠️ Bing 搜索失败: {e}")
            return []


    @classmethod
    def search(cls, keyword, max_results=10, timelimit='a'):
        """
        综合搜索（智能组合多个搜索引擎）
        
        策略：
        1. 优先使用 Google（如果配置了 GOOGLE_COOKIE）
        2. 如果数量不够，用百度补充
        3. 如果还不够，用 Bing 补充
        4. 自动去重，确保链接唯一
        """
        all_links = []
        seen_urls = set()  # 用于去重
        
        # 难以爬取的网站黑名单
        blocked_domains = [
            'zhihu.com', 'weibo.com', 'twitter.com', 'facebook.com',
            'instagram.com', 'youtube.com', 'bilibili.com', 'douyin.com'
        ]
        
        def is_valid_url(url):
            """检查URL是否有效（不在黑名单中）"""
            return not any(domain in url for domain in blocked_domains)
        
        def add_unique_links(new_links):
            """添加链接并去重"""
            added = 0
            for url in new_links:
                if url not in seen_urls and len(all_links) < max_results and is_valid_url(url):
                    all_links.append(url)
                    seen_urls.add(url)
                    added += 1
                elif not is_valid_url(url):
                    print(f"   ⚠️ 过滤黑名单网站: {url[:50]}...")
            return added
        
        # 1. 如果配置了 Google Cookie，优先使用 Google
        if GOOGLE_COOKIE:
            print(f"🔍 [1/3] 使用 Google 搜索（目标: {max_results} 篇）...")
            google_links = cls.search_google(keyword, max_results)
            added = add_unique_links(google_links)
            print(f"   ✅ Google 找到 {added} 篇，当前总数: {len(all_links)}/{max_results}")
        
        # 2. 如果数量不够，使用百度补充
        if len(all_links) < max_results:
            remaining = max_results - len(all_links)
            print(f"🔍 [2/3] 使用百度补充（还需: {remaining} 篇）...")
            baidu_links = cls.search_baidu(keyword, remaining * 2)  # 多搜一些，因为可能有重复
            added = add_unique_links(baidu_links)
            print(f"   ✅ 百度补充 {added} 篇，当前总数: {len(all_links)}/{max_results}")
        
        # 3. 如果还不够，使用 Bing 补充
        if len(all_links) < max_results:
            remaining = max_results - len(all_links)
            print(f"🔍 [3/3] 使用 Bing 补充（还需: {remaining} 篇）...")
            bing_links = cls.search_bing(keyword, remaining * 2)
            added = add_unique_links(bing_links)
            print(f"   ✅ Bing 补充 {added} 篇，当前总数: {len(all_links)}/{max_results}")
        
        # 最终结果
        if all_links:
            print(f"\n🎉 搜索完成！共找到 {len(all_links)} 篇文章")
        else:
            print("\n❌ 所有搜索引擎都未找到结果")
        
        return all_links
