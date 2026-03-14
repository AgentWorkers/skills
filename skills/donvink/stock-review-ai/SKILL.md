---
name: stock-review
description: A股市场自动化审查与分析系统，利用Gemini AI生成每日市场洞察，支持将分析结果发布到Hugo博客和微信公众号。
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/donvink/stock-review
    requires:
      anyBins:
        - python3
        - python
---
# 🚀 股票分析工具

👉 **[实时演示博客](https://donvink.github.io/stock-review/)**

## 语言支持

**自动匹配用户语言**：根据用户使用的语言进行响应。如果用户使用中文，回复中文；如果用户使用英文，回复英文。

## 脚本目录

**脚本执行**：将此 SKILL.md 文件所在的目录视为 `{baseDir}`，然后使用 `{baseDir}/scripts/<name>.py`。确保已安装 Python 3.10+ 并配置了所有依赖项。

| 脚本 | 功能 |
|------|------|
| `scripts/fetch_data.py` | 获取 A 股市场数据（指数、股票、行业等） |
| `scripts/analyze.py` | 使用 Gemini AI 分析市场数据 |
| `scripts/post_to_hugo.py` | 发布到 Hugo 博客 |
| `scripts/post_to_wechat.py` | 发布到微信官方账号 |
| `scripts/main.py` | 主执行脚本，协调整个工作流程 |

## 配置偏好设置

1. 检查是否存在 `config.yaml` 文件：`{baseDir}/stock-review/config.yaml`
2. 检查是否存在 `.env` 文件，并且其中配置了 `GEMINI_API_KEY`、`WECHAT_APP_ID`、`WECHAT_APP_SECRET`：`{baseDir}/stock-review/.env`

**`config.yaml` 支持的配置项**：
- 默认发布平台
- 是否默认跳过 AI 分析
- 默认数据回溯天数
- 默认请求延迟
- 默认重试次数
- API 密钥配置

**`.env` 文件支持的配置项**：
- API 密钥配置

**最低支持配置项**（不区分大小写，支持 `1/0` 或 `true/false`）：

| 配置项 | 默认值 | 说明 |
|-----|---------|------|
| `date` | `null` | 日期（YYYYMMDD 格式） |
| `force_refresh` | `false` | 是否强制刷新已获取的数据 |
| `skip_ai_analysis` | `false` | 是否跳过 AI 分析 |
| `platforms` | `["hugo"]` | 默认发布平台（['hugo'], ['wechat'], ['hugo', 'wechat'] |
| `data_dir` | `null` | 数据存储目录 |
| `max_retries` | `3` | 默认重试次数 |
| `request_delay` | `0.5` | 默认请求延迟（秒） |
| `backtrack_days` | `0` | 默认数据回溯天数 |
| `type` | `gemini` | 模型类型 |
| `model_name` | `gemini-2.5-flash` | 模型名称 |

**推荐的 `config.yaml` 示例**：

```yml
# default configuration for stock review skill
review:
  markets:                          # can include "shanghai", "shenzhen", "hongkong"
    - "shanghai"
    - "shenzhen"
    - "hongkong"
  default_period: "daily"           # can be "daily", "weekly", "monthly"
  date: null                        # can be specific date "YYYYMMDD" like "20260101" or null for today
  force_refresh: false              # whether to force refresh data even if cached data is available
  skip_ai_analysis: false           # whether to skip AI analysis and just return raw data
  platforms: ["hugo"]               # platforms to publish the report, e.g. ['hugo', 'wechat'] or ['hugo'] or ['wechat']

paths:
  data_dir: null                    # directory to store fetched data and cache, null means current project directory

parameters:
  max_retries: 3
  request_delay: 0.5
  backtrack_days: 0
  
models:
  type: "gemini"
  model_name: "gemini-2.5-flash"
```

**`.env` 文件示例**：

```md
# Gemini API Key
GEMINI_API_KEY="your_gemini_api_key"

# WeChat Official Account Configuration
WECHAT_APP_ID="your_wechat_app_id"
WECHAT_APP_SECRET="your_wechat_app_secret"
```

### 如何获取 Gemini API 密钥：
1. 访问官方门户：前往 https://aistudio.google.com/ 并使用您的 Google 账户登录。
2. 创建 API 密钥：在左侧菜单栏中点击“获取 API 密钥”，然后点击“在新项目中创建 API 密钥”，并复制生成的字符串（请妥善保存——关闭窗口后您将无法再次看到完整的密钥）。
3. 重要提示：
   - **免费 tier**：提供免费配额，但有请求频率限制（RPM/RPD）。
   - **数据隐私**：免费 tier 的数据可用于模型改进。对于敏感的商业数据，请考虑启用付费模式。

### 如何获取微信官方账号凭证：
1. 访问 https://developers.weixin.qq.com/platform/
2. 进入“我的企业” → “官方账号” → “开发密钥”
3. 添加开发密钥，复制 AppID 和 AppSecret
4. **将您的机器 IP 地址添加到白名单**

## 环境检查

首次使用前，请安装所有依赖项。

```bash
pip install -r {baseDir}/requirements.txt
```

检查以下内容：
- Python 版本
- 依赖项
- API 密钥
- 网络连接
- 目录权限

**如果任何检查失败**，提供相应的解决方法：

| 检查内容 | 解决方法 |
|-------|----------|
| Python 版本 | 安装 Python 3.10+：`brew install python@3.10`（macOS）或 `apt install python3.10`（Linux） |
| 依赖项 | 运行 `pip install -r {baseDir}/requirements.txt` |
| Gemini API 密钥 | 在 `.env` 文件中配置或通过环境变量设置 |
| 微信官方账号凭证 | 在 `.env` 文件中配置或通过环境变量设置 |
| 网络连接 | 检查网络代理设置 |
| 目录权限 | 确保 `data/` 和 `content/posts/` 目录具有写入权限 |

## 工作流程概述

请复制此检查清单，并在操作过程中逐项进行检查：

```
Review Analysis Progress:
- [ ] Step 0: Load preferences (config.yaml, .env), determine execution parameters
- [ ] Step 1: Fetch market data
- [ ] Step 2: Run AI analysis (optional)
- [ ] Step 3: Generate report
- [ ] Step 4: Publish to platforms
- [ ] Step 5: Report complete
```

### 第 0 步：加载配置

检查并加载 `config.yaml` 的设置（参见上面的“配置偏好设置”部分），解析并存储默认值以供后续步骤使用。

### 第 1 步：获取市场数据

获取指定日期的以下数据：

| 数据类型 | 来源 | 文件 |
|----------|------|------|
| 指数数据 | `stock_zh_index_spot_sina` | `data/{date}/index_{date}.csv` |
| 涨停池 | `stock_zt_pool_em` | `data/{date}/zt_pool_{date}.csv` |
| 跌停池 | `stock_zt_pool_dtgc_em` | `data/{date}/dt_pool_{date}.csv` |
| 失败的涨停池 | `stock_zt_pool_zbgc_em` | `data/{date}/zb_pool_{date}.csv` |
| 全市场数据 | `stock_zh_a_spot_em` | `data/{date}/A_stock_{date}.csv` |
| 流量排名前 20 的股票 | 计算得出 | `data/{date}/top_amount_stocks_{date}.csv` |
| 行业板块 | `stock_board_concept_name_em` | `data/{date}/concept_summary_{date}.csv` |
| 顶级交易者列表 | `stock_lhb_detail_daily_sina` | `data/{date}/lhb_{date}.csv` |
| 关注列表 | 计算得出 | `data/{date}/watchlist*_{date}.csv` |

**重试机制**：
- 默认重试 3 次
- 请求间隔 0.5 秒
- 失败时自动切换到备用接口

### 第 2 步：运行 AI 分析

**重要提示**：仅在以下情况下运行 AI 分析：
- `--skip-ai` 未设置
- `GEMINI_API_KEY` 已配置（通过 `config.yaml` 或环境变量）

**AI 分析提示**：

```python
prompt = f"""
Role Setting: You are a seasoned A-share strategy analyst with 20 years of experience...

Task Description: Conduct a multi-dimensional review based on the [daily review data]:
1. 🚩 Market Sentiment Diagnosis
2. 💰 Core Themes and Capital Flow
3. 🪜 Consecutive Limit-up Gradient and Space Game
4. ⚡ Key Stocks with Abnormal Movements Analysis
5. 🧭 Next Trading Day Strategy Recommendations

📊 Daily Review Data:
{market_summary}
"""
```

**输出结果**：`data/{date}/ai_analysis_{date}.md`

### 第 3 步：生成报告

**市场总结报告**：
- 文件：`data/{date}/market_summary_{date}.md`
- 格式：Markdown
- 内容：所有数据的表格总结

**AI 分析报告**（如果运行）：
- 文件：`data/{date}/ai_analysis_{date}.md`
- 格式：Markdown
- 内容：由 Gemini 生成的深入分析

### 第 4 步：发布到平台

**Hugo 博客发布**：

```bash
python3 {baseDir}/scripts/post_to_hugo.py --market-summary <file> --ai-analysis <file> --date <date>
```

**输出结果**：`content/posts/stock-analysis-{YYYY-MM-DD}.md`

**微信官方账号发布**（需要 API 凭证）：

```bash
python3 {baseDir}/scripts/post_to_wechat.py --market-summary-file <file> --ai-analysis-file <file> --date <date> --cover-file <file> --title <title>
```

**微信官方账号 API 请求规则**：
- 端点：`POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN`
- `article_type`：`news`
- 需要 `thumb_media_id`（封面图片）
- 评论设置：`need_open_comment=1`, `only_fans_can_comment=0`

### 第 5 步：完成报告

**成功报告**：

```
✅ A-share Review Analysis Complete!

Date: 2026-03-04
Data: data/20260304/ (12 files)
AI Analysis: ✓ Generated (Gemini 2.0 Flash)

Published Platforms:
→ Hugo Blog: content/posts/stock-analysis-2026-03-04.md
→ WeChat Official Account: Draft ID: abc123def456

Market Snapshot:
• Shanghai Composite: 3350.52 (+1.02%)
• Turnover: 1.95 trillion
• Advance/Decline: 2857 / 2058
• Limit-up/Limit-down: 78 / 3

View Blog: https://donvink.github.io/stock-review/
```

**错误报告**：

```
❌ Review Analysis Failed

Error: Unable to fetch limit-up pool data
Suggestions: 
1. Check network connection
2. Try --force parameter to force refresh
3. Use --date to specify another date
```

## 详细功能描述

### 数据获取模块

| 功能 | 功能 | 重试机制 | 缓存 |
|------|------|------|------|
| `stock_summary()` | 获取指数数据 | ✓ | ✓ |
| `stock_zt_dt_pool()` | 获取涨停/跌停数据 | ✓ | ✓ |
| `fetch_all_stock_data()` | 获取全市场数据 | ✓（最多尝试 3 次） | ✓ |
| `get_top_amount_stocks()` | 获取流量排名前 20 的股票 | ✓ | ✓ |
| `get_concept_summary()` | 获取行业板块数据 | ✓ | ✓ |
| `get_lhb_data()` | 获取顶级交易者列表 | ✓ | ✓ |

### AI 分析模块

**模型**：`gemini-2.5-flash`

**分析维度**：
1. **市场情绪诊断** - 上涨/下跌比例、涨停/跌停对比、成交量
2. **核心主题跟踪** - 资本流动、热门行业
3. **连续涨停梯度分析** - 行情板高度、涨停结构
4. **异常波动股票分析** | 高成交量股票、顶级交易者列表
5. **次日策略建议** | 基于数据的交易建议

### 发布模块

| 平台 | 方法 | 需求 | 输出 |
|------|------|------|------|
| Hugo 博客 | 文件写入 | 无 | Markdown 文件 |
| 微信官方账号 | API | AppID/Secret | 草稿 ID |

## 功能比较

| 功能 | 数据获取 | AI 分析 | Hugo 发布 | 微信发布 |
|------|----------|--------|----------|----------|
| 自动获取最新数据 | ✓ | - | - | - |
| 数据缓存 | ✓ | - | - | - |
| 重试机制 | ✓ | - | - | - |
| 多源备份 | ✓ | - | - | - |
| 格式化数值（百万/万） | ✓ | - | - | - |
| 过滤 ST 股票 | ✓ | - | - | - |
| 关注列表构建 | ✓ | - | - | - |
| 市场情绪诊断 | - | ✓ | - | - |
| 涨停梯度分析 | - | ✓ | - | - |
| 策略建议 | - | ✓ | - | - |
| Markdown 格式 | - | ✓ | ✓ | ✓ |
| 时区处理 | - | - | ✓ | - |
| Hugo 前言内容 | - | - | ✓ | - |
| 微信 HTML 转换 | - | - | - | ✓ |
| 评论设置 | - | - | - | ✓ |

## 先决条件

**必需条件**：
- Python 3.10+
- 依赖项：`pip install -r requirements.txt`
- Gemini API 密钥（用于 AI 分析）

**可选条件**：
- 微信官方账号 AppID 和 AppSecret（用于微信发布）
- Hugo 博客环境（用于博客发布）

**配置位置**（优先级顺序）：
1. 命令行参数
2. `config.yaml`、`.env`（项目级/用户级）
3. 环境变量
4. 默认值

## 故障排除

| 问题 | 解决方法 |
|------|----------|
| 无法获取数据 | 检查网络连接，更换日期 |
| Gemini API 错误 | 检查 API 密钥是否有效，配额是否足够 |
| 涨停池数据为空 | 可能是非交易日，尝试更换日期 |
| 微信发布失败 | 检查 AppID/Secret，确认 IP 地址是否在白名单中 |
| 中文字符编码问题 | 确保文件编码为 UTF-8 |
| 数据格式错误 | 检查 CSV 文件，确保代码列未被转换为数字 |
| 超时错误 | 增加 `request_delay` 或 `max_retries` |
| 内存不足 | 减少数据量或分批处理 |

## 扩展支持

可以通过 `config.yaml` 进行自定义。请参阅“配置偏好设置”部分以了解支持的选项。

## 相关参考资料

| 主题 | 参考链接 |
|------|------|
| AkShare 文档 | https://akshare.akfamily.xyz/index.html |
| Gemini API | https://aistudio.google.com/ |
| 微信官方账号 API | https://developers.weixin.qq.com/platform |
| Hugo 文档 | https://gohugo.io/ |

## 版本历史

| 版本 | 发布日期 | 更新内容 |
|------|------|------|
| 1.0.0 | 2026-03-11 | 初始版本 |