# 🤖 智谱AI Agent Dashboard

基于 GitHub Actions 和智谱AI GLM 模型的云端自动化信息获取与展示系统。

## ✨ 功能特性

- ⏰ **定时自动运行**: 通过 GitHub Actions 每 6 小时自动运行一次
- 🤖 **AI 驱动**: 使用智谱AI GLM-4 模型智能分析和总结信息
- 📊 **可视化展示**: 自动生成美观的网页报告
- 🚀 **零成本**: 完全基于 GitHub 免费服务
- 📱 **响应式设计**: 支持手机、平板、电脑等多端访问
- 📜 **历史记录**: 自动保存最近 50 次运行结果

## 🏗️ 项目结构

```
zhipuai-agent-dashboard/
├── .github/
│   └── workflows/
│       └── update-dashboard.yml    # GitHub Actions 工作流配置
├── scripts/
│   ├── run_skill.py                # 智谱AI Agent 执行脚本
│   └── generate_html.py             # HTML 生成脚本
├── data/
│   ├── results.json                # 最新结果数据
│   └── history.json                # 历史记录
├── docs/
│   └── index.html                  # 生成的网页
├── requirements.txt                # Python 依赖
└── README.md                       # 项目说明
```

## 🚀 快速开始

### 1. Fork 本仓库

点击右上角的 Fork 按钮将仓库复制到你的账号下。

### 2. 配置 Secrets

在你的仓库中设置以下 Secret:

1. 进入仓库的 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 添加以下 secret:

   | 名称 | 值 |
   |------|-----|
   | `ZHIPUAI_API_KEY` | 你的智谱AI API Key |

> 💡 获取智谱AI API Key: 访问 [智谱AI开放平台](https://open.bigmodel.cn/)

### 3. 启用 GitHub Pages

1. 进入仓库的 **Settings** → **Pages**
2. **Source** 选择 `GitHub Actions`

### 4. 触发首次运行

有两种方式触发工作流:

**方式一: 手动触发**
1. 进入 **Actions** 标签
2. 选择 "Update Dashboard" 工作流
3. 点击 "Run workflow" → "Run workflow"

**方式二: 等待自动运行**
- 工作流会按照以下时间自动运行 (UTC):
  - 00:00 (北京时间 08:00)
  - 06:00 (北京时间 14:00)
  - 12:00 (北京时间 20:00)
  - 18:00 (北京时间 02:00)

### 5. 查看结果

工作流运行完成后，访问:
```
https://YOUR_USERNAME.github.io/claude-agent-dashboard/
```

## 🛠️ 本地开发

如果你想在本地测试:

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export ZHIPUAI_API_KEY='your-api-key'

# 运行数据获取脚本
python scripts/run_skill.py

# 生成 HTML 报告
python scripts/generate_html.py

# 在浏览器中打开 docs/index.html
```

## 📝 自定义配置

### 修改运行频率

编辑 `.github/workflows/update-dashboard.yml`:

```yaml
on:
  schedule:
    - cron: '0 0,6,12,18 * * *'  # 修改这里
```

Cron 格式说明:
- 格式: `分钟 小时 日 月 星期`
- 示例:
  - `0 0 * * *` - 每天 00:00
  - `0 */2 * * *` - 每 2 小时
  - `0 9 * * 1-5` - 工作日早上 9 点

### 修改 Prompt 模板

编辑 `scripts/run_skill.py` 中的 `load_prompt_template()` 函数，修改你想要智谱AI执行的任务。

### 修改页面样式

编辑 `scripts/generate_html.py` 中的 `HTML_TEMPLATE` 变量来自定义网页样式。

## 🔧 故障排查

### 工作流运行失败

1. 检查 Actions 标签下的运行日志
2. 确认 `ZHIPUAI_API_KEY` 是否正确设置
3. 检查 API Key 是否有足够的额度

### 页面显示异常

1. 确认 GitHub Pages 已启用
2. 检查 Source 是否设置为 `GitHub Actions`
3. 等待工作流完成后再访问

### 智谱AI API 调用失败

1. 确认 API Key 有效
2. 检查 API 使用额度
3. 查看工作流日志中的具体错误信息

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 💡 灵感

本项目灵感来自 n8n 的自动化方案，使用 GitHub Actions 和智谱AI GLM 模型实现了完全云端运行的自动化工作流。

---

**Made with ❤️ using 智谱AI & GitHub Actions**
