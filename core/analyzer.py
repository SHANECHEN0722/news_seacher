"""
AI 分析模块
"""
import json
from config import client, AI_MODEL, AI_TEMPERATURE


class NewsAnalyzer:
    """新闻分析器（基于 DeepSeek）"""
    
    @staticmethod
    def summarize_article(text):
        """Map 阶段：总结单篇文章"""
        prompt = f"""
        请为以下新闻文本生成一个非常简洁的摘要（约100字）和3个关键点。

        文本：
        {text[:4000]} 

        输出：
        摘要：[此处为摘要]
        关键点：
        - [关键点1]
        - [关键点2]
        - [关键点3]
        """
        
        try:
            response = client.chat.completions.create(
                model=AI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f" [!] DeepSeek 摘要失败: {e}")
            return "摘要生成失败..."
    
    @staticmethod
    def consolidate_summaries(summaries, keyword):
        """Reduce 阶段：整合所有摘要"""
        context = "\n---\n".join(summaries)
        
        prompt = f"""
        基于以下关于「{keyword}」的 **摘要信息**，提取4类信息。
        你必须严格按 JSON 格式输出，不要包含 Markdown 标记。

        需要提取的字段：
        1. main_summary：主摘要（150-200字，综合所有信息）；
        2. key_sub_themes: 关键子主题（列表，例如 ["技术影响", "市场反应", "伦理讨论"]）；
        3. key_entities：关键实体（列表，至少5个，如人名、公司名、地点）；
        4. timeline：时间线（列表，每个元素包含 date（YYYY-MM-DD格式，必须是真实发生的日期，如果不确定具体日期可以只写年月如2024-11）、event（事件描述）、source（来源URL））；

        **重要提示**：
        - timeline 中的 date 必须基于文章中提到的真实时间，不要编造未来的日期
        - 如果文章中没有明确日期，可以根据上下文推断大致时间
        - 当前时间是 2025年11月，不要生成2026年或更晚的日期
        - source 字段应该填写提到该事件的文章URL

        摘要信息输入：
        {context}
        """
        
        try:
            response = client.chat.completions.create(
                model=AI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=AI_TEMPERATURE,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content.strip())
        except Exception as e:
            return f"DeepSeek 最终整合失败：{str(e)}"
    
    @classmethod
    def analyze(cls, articles, keyword):
        """执行完整的 Map-Reduce 分析"""
        print("🚀 [Map-Reduce] Map阶段：正在并行总结文章...")
        
        summaries = []
        for i, article in enumerate(articles):
            print(f"  -> 处理文章 {i + 1}/{len(articles)}: {article['title'][:20]}...")
            summary = cls.summarize_article(article['text'])
            summaries.append(f"摘要 {i + 1} (来源: {article['url']}):\n{summary}\n")
        
        print("🚀 [Map-Reduce] Reduce阶段：正在整合全局信息...")
        structured_data = cls.consolidate_summaries(summaries, keyword)
        
        if isinstance(structured_data, str):
            return structured_data
        
        # 添加来源链接
        structured_data["sources"] = [article['url'] for article in articles]
        return structured_data
