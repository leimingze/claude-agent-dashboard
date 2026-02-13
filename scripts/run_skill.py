#!/usr/bin/env python3
"""
Claude Agent Skill 执行脚本
调用 Claude API 获取数据并保存到 JSON 文件
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from anthropic import Anthropic
except ImportError:
    print("错误: 未安装 anthropic 库")
    print("请运行: pip install anthropic")
    sys.exit(1)


def load_prompt_template():
    """加载 prompt 模板"""
    # 这里定义你的任务描述
    # 你可以根据需要修改这个 prompt 来执行不同的任务
    prompt = """你是一个专业的信息收集和分析助手。请帮我完成以下任务:

1. 获取今天的科技热点新闻（3-5 条）
2. 对每条新闻进行简要分析
3. 总结今天的科技趋势

请以 JSON 格式返回结果，格式如下:
```json
{
  "date": "2025-02-14",
  "summary": "今日科技趋势总结",
  "news": [
    {
      "title": "新闻标题",
      "source": "来源",
      "url": "链接",
      "summary": "摘要",
      "impact": "影响分析"
    }
  ],
  "trends": ["趋势1", "趋势2", "趋势3"]
}
```

请确保返回的是有效的 JSON 格式，不要包含其他文本。"""
    return prompt


def run_claude_skill():
    """执行 Claude Agent Skill 获取数据"""
    # 检查 API Key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("错误: 未设置 ANTHROPIC_API_KEY 环境变量")
        print("请设置: export ANTHROPIC_API_KEY='your-api-key'")
        sys.exit(1)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行 Claude Agent Skill...")

    try:
        # 初始化 Claude 客户端
        client = Anthropic(api_key=api_key)

        # 获取 prompt
        prompt = load_prompt_template()

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在调用 Claude API...")

        # 调用 Claude API
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # 解析响应
        content = message.content[0].text

        # 尝试提取 JSON（Claude 可能在 JSON 前后添加文字）
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # 尝试直接解析整个内容
            json_str = content

        # 解析 JSON
        result_data = json.loads(json_str)

        # 包装结果
        results = {
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "data": result_data
        }

        # 保存到 data 目录
        data_dir = Path(__file__).parent.parent / "data"
        data_dir.mkdir(exist_ok=True)

        output_file = data_dir / "results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        # 同时保存到历史记录
        history_file = data_dir / "history.json"
        history = []
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)

        history.append(results)
        # 只保留最近 50 条记录
        history = history[-50:]

        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ 数据获取成功！")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] - 获取了 {len(result_data.get('news', []))} 条新闻")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] - 历史记录共 {len(history)} 条")

        return results

    except json.JSONDecodeError as e:
        print(f"错误: JSON 解析失败 - {e}")
        print(f"Claude 返回的内容: {content[:500]}...")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {type(e).__name__} - {e}")
        sys.exit(1)


def main():
    """主函数"""
    run_claude_skill()


if __name__ == "__main__":
    main()
