---
name: ga-deep-dive
displayName: GA4 Deep Dive
version: 1.0.3
description: 全面的 Google Analytics 4 分析功能——能够提取 API 提供的所有数据，包括健康状况评分（Health scores）、页面滚动深度（Scroll depth）、用户群体（Cohorts）、人口统计信息（Demographics）等。
triggers:
  - analytics
  - ga4
  - google analytics
  - traffic
  - engagement
  - bounce rate
  - sessions
  - users
  - metrics
  - deep dive
  - report
---
# GA4深度分析 📊

**所有者作战室** — GA4能为你提供的关于产品的所有信息。

## 你将获得什么

| 脚本 | 用途 |
|--------|---------|
| `deep_dive_v3.py` | 包含7个健康指标的执行摘要 |
| `deep_dive_v4.py` | 全面分析结果：滚动深度、用户群体、人口统计信息 |
| `send_report_email.py` | 每两周发送一次电子邮件报告 |

### 健康指标
- **用户参与度** — 用户是否积极参与？
- **流量来源多样性** — 是否过度依赖某个渠道？
- **用户留存率** — 用户是否会重复访问？（日活跃用户/月活跃用户）
- **业务增长** — 业务是否在增长？
- **内容质量** | 是否存在问题页面？
- **移动设备适配** — 网站是否适合移动设备？
- **地域覆盖范围** — 全球范围内的访问情况？

### 深度分析（v4）
- 📜 **滚动深度** — 用户实际阅读的内容长度
- 🔗 **外部链接** — 用户点击访问的链接
- 🔍 **站点搜索** — 用户的搜索内容
- 👥 **人口统计** — 用户的年龄、性别、兴趣爱好
- 🌐 **搜索控制台** — 自然搜索的表现
- 📊 **用户群体留存率** | 周与周之间的用户留存情况
- 🎯 **目标受众** | 定制受众的表现

---

## 快速入门

**向你的OpenClaw代理请求：**
> “帮我为我的网站设置ga-deep-dive功能”

代理将指导你完成以下步骤：
1. 创建Google Cloud OAuth凭证
2. 获取你的GA4属性ID
3. 运行首次分析

---

## 手动设置

### 1. 安装依赖项

```bash
cd ~/.openclaw/skills/ga-deep-dive
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. 获取Google OAuth凭证

1. 访问[Google Cloud Console](https://console.cloud.google.com/)
2. 创建一个项目（或使用现有项目）
3. 启用**Google Analytics Data API**
4. 创建**OAuth 2.0客户端ID**（适用于桌面应用程序）
5. 下载JSON文件 → 保存为`~/.config/ga-deep-dive/credentials.json`

### 3. 获取你的GA4属性ID

1. 打开[Google Analytics](https://analytics.google.com/)
2. 进入**管理** → **属性设置**
3. 复制**属性ID**（9位数字）

### 4. 首次运行（身份验证）

```bash
source ~/.openclaw/skills/ga-deep-dive/.venv/bin/activate
python3 scripts/deep_dive_v3.py YOUR_PROPERTY_ID
```

系统会打开一个浏览器窗口以获取OAuth授权。批准授权后，设置就完成了！

---

## 使用方法

### 运行分析

```bash
# By property ID
python3 scripts/deep_dive_v3.py 123456789

# By name (if configured)
python3 scripts/deep_dive_v3.py mysite

# Full monty
python3 scripts/deep_dive_v4.py 123456789

# Custom period
python3 scripts/deep_dive_v3.py mysite --days 60
```

### 配置属性名称

编辑`scripts/deep_dive_v3.py`文件，并在`PROPERTIES`部分添加相应的属性名称：

```python
PROPERTIES = {
    'mysite': '123456789',
    'blog': '987654321',
}
```

### 电子邮件报告（可选）

通过环境变量进行配置：

```bash
# Required for email functionality
export GA4_REPORT_RECIPIENTS="you@example.com,team@example.com"
export AGENTMAIL_INBOX="youragent@agentmail.to"
export AGENTMAIL_API_KEY="am_your_key_here"
```

使用以下命令运行脚本：
```bash
# Generate and send report
python3 scripts/send_report_email.py mysite --days 14

# Dry run (generate report only, no email)
python3 scripts/send_report_email.py mysite --dry-run
```

设置定时任务以每两周生成一次报告：
```bash
# Mondays & Thursdays at 9am (adjust env vars path)
0 9 * * 1,4 source ~/.ga4-env && cd ~/.openclaw/skills/ga-deep-dive && .venv/bin/python3 scripts/send_report_email.py mysite
```

---

## GA4设置建议

为了获得最佳分析结果，请在GA4管理界面启用以下功能：

| 功能 | 设置位置 | 原因 |
|---------|-------|-----|
| **Google Signals** | 数据设置 → 数据收集 | 人口统计信息 |
| **搜索控制台** | 产品链接 → 搜索控制台 | 自然搜索数据 |
| **增强型测量** | 数据流 → Web → 增强型测量 | 用户滚动行为、外部链接点击 |
| **关键事件** | 事件设置 → 标记为关键事件 | 跟踪转化情况 |

---

## 示例输出

```
🏥 HEALTH SCORES
   ✅ Engagement           ████████████████░░░░ 81/100
   ❌ Traffic Diversity    █████░░░░░░░░░░░░░░░ 27/100
   ✅ Mobile               ██████████████████░░ 90/100
   
   🎯 OVERALL: 66/100 (Grade B)

💡 ACTIONABLE INSIGHTS
   🔴 72% traffic from Direct — DIVERSIFY NOW
   🚨 Fix /agents/me/claim — 100% bounce rate
   🟢 China has highest quality traffic — consider localization
```

---

## 故障排除

**“令牌过期”**
```bash
rm ~/.config/ga-deep-dive/token.json
# Run again to re-auth
```

**“没有人口统计数据”**
- 在GA4中启用**Google Signals**功能
- 每个用户群体需要至少50名用户才能生成有效数据（隐私保护限制）

**“没有搜索控制台数据”**
- 在GA4管理界面中将搜索控制台链接添加到**产品链接**设置中
- 等待24-48小时以完成数据同步

---

## 许可证

MIT许可证 — 由[ClaudiusThePirateEmperor](https://solvr.dev/agents/agent_ClaudiusThePirateEmperor)开发 🏴‍☠️

代码仓库：https://github.com/fcavalcantirj/ga-deep-dive