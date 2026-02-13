#!/usr/bin/env python3
"""
HTML 报告生成脚本
读取数据并生成美观的 HTML 页面
"""

import os
import json
from datetime import datetime
from pathlib import Path

# HTML 模板
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Agent Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .header h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }

        .header .subtitle {
            color: #666;
            font-size: 14px;
        }

        .main-content {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        .section-title {
            font-size: 20px;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }

        .summary {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            line-height: 1.8;
            color: #333;
        }

        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .news-card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .news-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .news-card h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 16px;
        }

        .news-card .source {
            color: #667eea;
            font-size: 12px;
            margin-bottom: 10px;
        }

        .news-card .summary {
            background: transparent;
            padding: 0;
            margin-bottom: 10px;
            font-size: 14px;
            line-height: 1.6;
        }

        .news-card .impact {
            background: #e8f5e9;
            padding: 10px;
            border-radius: 4px;
            font-size: 13px;
            color: #2e7d32;
        }

        .news-card .link {
            margin-top: 10px;
        }

        .news-card .link a {
            color: #667eea;
            text-decoration: none;
            font-size: 13px;
        }

        .news-card .link a:hover {
            text-decoration: underline;
        }

        .trends {
            background: #fff3e0;
            padding: 20px;
            border-radius: 8px;
        }

        .trends ul {
            list-style: none;
            padding-left: 0;
        }

        .trends li {
            padding: 8px 0;
            padding-left: 24px;
            position: relative;
            color: #333;
        }

        .trends li:before {
            content: "→";
            position: absolute;
            left: 0;
            color: #ff9800;
            font-weight: bold;
        }

        .footer {
            text-align: center;
            color: white;
            padding: 20px;
            font-size: 14px;
        }

        .error {
            background: #ffebee;
            color: #c62828;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }

        @media (max-width: 768px) {
            .news-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Claude Agent Dashboard</h1>
            <p class="subtitle">最后更新: {{ update_time }}</p>
        </div>

        {% if error %}
        <div class="main-content">
            <div class="error">
                <h2>⚠️ 数据加载失败</h2>
                <p>{{ error }}</p>
            </div>
        </div>
        {% else %}
        <div class="main-content">
            <h2 class="section-title">📊 今日概览</h2>
            <div class="summary">{{ summary }}</div>

            <h2 class="section-title">📰 热点新闻</h2>
            <div class="news-grid">
                {% for news in news_items %}
                <div class="news-card">
                    <h3>{{ news.title }}</h3>
                    <p class="source">📍 {{ news.source }}</p>
                    <p class="summary">{{ news.summary }}</p>
                    <div class="impact"><strong>影响分析:</strong> {{ news.impact }}</div>
                    {% if news.url %}
                    <p class="link"><a href="{{ news.url }}" target="_blank">查看详情 →</a></p>
                    {% endif %}
                </div>
                {% endfor %}
            </div>

            <h2 class="section-title">📈 趋势洞察</h2>
            <div class="trends">
                <ul>
                    {% for trend in trends %}
                    <li>{{ trend }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        {% endif %}

        <div class="footer">
            <p>Powered by Claude Agent Skills | 自动运行于 GitHub Actions</p>
        </div>
    </div>
</body>
</html>"""


def format_timestamp(iso_string):
    """格式化时间戳"""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return iso_string


def generate_html():
    """生成 HTML 报告"""
    # 读取结果数据
    data_dir = Path(__file__).parent.parent / "data"
    results_file = data_dir / "results.json"

    # 默认值
    template_vars = {
        "update_time": "未知",
        "error": None,
        "summary": "暂无数据",
        "news_items": [],
        "trends": []
    }

    try:
        if results_file.exists():
            with open(results_file, 'r', encoding='utf-8') as f:
                results = json.load(f)

            if results.get("status") == "success":
                data = results.get("data", {})

                template_vars.update({
                    "update_time": format_timestamp(results.get("timestamp", "")),
                    "summary": data.get("summary", "暂无概要"),
                    "news_items": data.get("news", []),
                    "trends": data.get("trends", [])
                })
            else:
                template_vars["error"] = "数据获取失败"
        else:
            template_vars["error"] = "数据文件不存在，请等待首次工作流运行完成"

    except Exception as e:
        template_vars["error"] = f"读取数据时出错: {str(e)}"

    # 使用模板生成 HTML
    html = HTML_TEMPLATE

    # 简单的模板替换（为了不依赖 jinja2）
    html = html.replace("{{ update_time }}", template_vars["update_time"])
    html = html.replace("{{ summary }}", template_vars["summary"])

    # 处理新闻列表
    if template_vars["error"]:
        html = html.replace("{% if error %}", "").replace("{% else %}", "").replace("{% endif %}", "")
        html = html.replace("{{ error }}", template_vars["error"])
        # 移除正常内容部分
        html = html.split("<div class=\"main-content\">")[0] + "<div class=\"main-content\">" + html.split("{% else %}")[1].split("<div class=\"main-content\">")[1].split("</div>")[0] + "</div>" + html.split("</div>")[-1]
    else:
        # 移除错误处理部分
        html = html.replace("{% if error %}", "").replace("{% else %}", "").replace("{% endif %}", "")
        # 移除错误显示div
        html = html.replace('<div class="error">\n                <h2>⚠️ 数据加载失败</h2>\n                <p>{{ error }}</p>\n            </div>\n            ', "")

    # 生成新闻卡片
    news_html = ""
    for news in template_vars["news_items"]:
        title = news.get("title", "无标题")
        source = news.get("source", "未知来源")
        summary = news.get("summary", "暂无摘要")
        impact = news.get("impact", "暂无分析")
        url = news.get("url", "")

        card = f"""                <div class="news-card">
                    <h3>{title}</h3>
                    <p class="source">📍 {source}</p>
                    <p class="summary">{summary}</p>
                    <div class="impact"><strong>影响分析:</strong> {impact}</div>"""

        if url:
            card += f'\n                    <p class="link"><a href="{url}" target="_blank">查看详情 →</a></p>'

        card += "                </div>\n"
        news_html += card

    html = html.replace("{% for news in news_items %}                <div class=\"news-card\">...</div>{% endfor %}", news_html.rstrip())

    # 生成趋势列表
    trends_html = ""
    for trend in template_vars["trends"]:
        trends_html += f"                    <li>{trend}</li>\n"

    html = html.replace("{% for trend in trends %}<li>{{ trend }}</li>{% endfor %}", trends_html.rstrip())

    # 确保 docs 目录存在
    docs_dir = Path(__file__).parent.parent / "docs"
    docs_dir.mkdir(exist_ok=True)

    # 写入 HTML 文件
    output_file = docs_dir / "index.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ HTML 报告生成成功: {output_file}")
    print(f"✓ 包含 {len(template_vars['news_items'])} 条新闻")
    print(f"✓ 包含 {len(template_vars['trends'])} 个趋势")


if __name__ == "__main__":
    generate_html()
