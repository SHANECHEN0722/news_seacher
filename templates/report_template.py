"""
HTML Report Template
"""
from datetime import datetime


def generate_html_content(keyword, data):
    """Generate HTML content"""
    
    summary = data.get('main_summary', 'No summary data available')
    themes = data.get('key_sub_themes', [])
    entities = data.get('key_entities', [])
    timeline = data.get('timeline', [])
    sources = data.get('sources', [])
    
    # Format time in English
    now = datetime.now()
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    current_time = f"{months[now.month - 1]} {now.day}, {now.year} {now.strftime('%H:%M')}"
    
    # Generate entity badges
    entities_html = "".join([f'<span class="badge">{entity}</span>' for entity in entities])
    
    # Generate theme list
    themes_html = ''.join([
        f'<div class="theme-item"><div class="bullet"></div><span>{theme}</span></div>' 
        for theme in themes
    ])
    
    # Generate timeline
    timeline_html = ''.join([
        f'''
        <div class="timeline-item">
            <div class="timeline-date">📍 {item.get("date", "Unknown date")}</div>
            <div class="timeline-event">{item.get("event", "")}</div>
            <div class="timeline-source">Source: {item.get("source", "Unknown")[:60]}...</div>
        </div>
        ''' for item in timeline
    ])
    
    # Generate source links
    sources_html = ''.join([
        f'''
        <a href="{url}" target="_blank" class="source-link">
            <span class="source-icon">🌐</span>
            <span class="source-text">{url}</span>
        </a>
        ''' for url in sources
    ])
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{ 
            --primary: #6366f1; 
            --primary-dark: #4f46e5;
            --secondary: #8b5cf6;
            --accent: #ec4899;
            --bg-main: #0f172a;
            --bg-card: #1e293b;
            --bg-hover: #334155;
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --border: #334155;
        }}
        body {{ 
            background: var(--bg-main);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color: var(--text-primary);
            line-height: 1.6;
            padding-bottom: 60px;
        }}
        .header {{ 
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
            padding: 80px 20px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        .header::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.3;
        }}
        .header-content {{ position: relative; z-index: 1; max-width: 900px; margin: 0 auto; }}
        .main-title {{ 
            font-size: 3.5rem; 
            font-weight: 700; 
            margin-bottom: 15px;
            text-shadow: 0 2px 20px rgba(0,0,0,0.3);
            letter-spacing: -1px;
        }}
        .subtitle {{ 
            font-size: 0.95rem; 
            opacity: 0.9; 
            letter-spacing: 3px;
            font-weight: 300;
            text-transform: uppercase;
        }}
        .meta-info {{ margin-top: 20px; font-size: 0.85rem; opacity: 0.8; }}
        .container {{ max-width: 1200px; margin: -40px auto 0; padding: 0 20px; position: relative; z-index: 2; }}
        .card {{ 
            background: var(--bg-card);
            border-radius: 20px;
            padding: 35px;
            margin-bottom: 30px;
            border: 1px solid var(--border);
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .card:hover {{ 
            transform: translateY(-5px);
            box-shadow: 0 12px 24px rgba(99, 102, 241, 0.15);
            border-color: var(--primary);
        }}
        .card-header {{ 
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 2px solid var(--border);
        }}
        .icon {{ 
            width: 48px; height: 48px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }}
        .card-title {{ font-size: 1.4rem; font-weight: 600; color: var(--text-primary); }}
        .summary {{ font-size: 1.1rem; line-height: 1.9; color: var(--text-secondary); text-align: justify; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }}
        .badge {{ 
            display: inline-block;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
            color: var(--text-primary);
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 0.9rem;
            margin: 5px;
            border: 1px solid rgba(99, 102, 241, 0.3);
            transition: all 0.2s;
        }}
        .badge:hover {{ background: linear-gradient(135deg, rgba(99, 102, 241, 0.4), rgba(139, 92, 246, 0.4)); transform: scale(1.05); }}
        .theme-item {{ 
            padding: 15px 0;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.2s;
        }}
        .theme-item:last-child {{ border-bottom: none; }}
        .theme-item:hover {{ padding-left: 10px; color: var(--primary); }}
        .bullet {{ 
            width: 10px; height: 10px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 50%;
            flex-shrink: 0;
        }}
        .timeline {{ position: relative; padding-left: 40px; }}
        .timeline::before {{
            content: '';
            position: absolute;
            left: 15px; top: 0; bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, var(--primary), var(--secondary));
            border-radius: 2px;
        }}
        .timeline-item {{ position: relative; padding: 20px 0 20px 30px; margin-bottom: 15px; }}
        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -32px; top: 25px;
            width: 16px; height: 16px;
            background: var(--primary);
            border: 3px solid var(--bg-card);
            border-radius: 50%;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }}
        .timeline-date {{ color: var(--primary); font-weight: 600; font-size: 0.9rem; margin-bottom: 8px; }}
        .timeline-event {{ color: var(--text-primary); font-weight: 500; margin-bottom: 5px; font-size: 1.05rem; }}
        .timeline-source {{ color: var(--text-muted); font-size: 0.85rem; }}
        .source-link {{ 
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 15px 20px;
            background: var(--bg-hover);
            border: 1px solid var(--border);
            border-radius: 12px;
            text-decoration: none;
            color: var(--text-secondary);
            margin-bottom: 12px;
            transition: all 0.3s;
        }}
        .source-link:hover {{ background: var(--primary); color: white; transform: translateX(5px); border-color: var(--primary); }}
        .source-icon {{ font-size: 1.2rem; }}
        .source-text {{ flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 0.9rem; }}
        footer {{ text-align: center; padding: 40px 20px; color: var(--text-muted); font-size: 0.85rem; }}
        @media (max-width: 768px) {{
            .main-title {{ font-size: 2.5rem; }}
            .grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1 class="main-title">{keyword}</h1>

            <div class="meta-info">Generated: {current_time} | Sources: {len(sources)} articles</div>
        </div>
    </div>
    
    <div class="container">
        <div class="card">
            <div class="card-header">
                <div class="icon">📊</div>
                <div class="card-title">Executive Summary</div>
            </div>
            <p class="summary">{summary}</p>
        </div>
        
        <div class="grid">
            <div class="card">
                <div class="card-header">
                    <div class="icon">🎯</div>
                    <div class="card-title">Key Themes</div>
                </div>
                <div>{themes_html}</div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <div class="icon">🏢</div>
                    <div class="card-title">Related Entities</div>
                </div>
                <div>{entities_html}</div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">
                <div class="icon">📅</div>
                <div class="card-title">Event Timeline</div>
            </div>
            <div class="timeline">{timeline_html}</div>
        </div>
        
        <div class="card">
            <div class="card-header">
                <div class="icon">🔗</div>
                <div class="card-title">References</div>
            </div>
            <div>{sources_html}</div>
        </div>
    </div>
    
    <footer>
        © 2025 AI News Aggregator | Powered by DeepSeek-V3 | Map-Reduce Pipeline
    </footer>
</body>
</html>
"""
