---
description: YC Startup School 的 CLI 工具：用于 a16z Speedrun、SPC 以及创业项目的发现与跟踪——提供每周更新、仪表盘、申请流程以及加速器项目的截止日期信息。
allowed-tools: Bash, Read, Write
name: yc
version: 0.3.2
metadata:
  openclaw:
    requires:
      bins:
        - yc
    install:
      - kind: node
        package: "@lucasygu/yc"
        bins: [yc]
    os: [macos]
    homepage: https://github.com/lucasygu/yc-cli
tags:
  - ycombinator
  - startup-school
  - a16z
  - speedrun
  - south-park-commons
  - spc
  - accelerator
  - fellowship
  - incubator
  - discover
  - productivity
---
# YC CLI — YC创业学校、a16z速成计划（Speedrun）以及SPC项目申请工具

这是一个命令行工具（CLI），用于管理您的YC创业学校申请流程、提交a16z速成计划申请，以及查找24家以上的加速器、奖学金项目和孵化器——所有这些操作都可以在终端中完成。

## 前提条件

- Node.js 22及以上版本
- 用于YC相关命令：需使用Chrome浏览器登录[startupschool.org](https://www.startupschool.org/)。
- 用于a16z速成计划命令：无需认证（API为公开接口）。
- 用于SPC相关命令：需要使用Chrome浏览器（以便通过Chrome自动化功能自动填写表单）。

## 快速参考

```bash
# YC Startup School
yc whoami                    # Test connection, show user info
yc dashboard                 # Show streak, curriculum, weekly status
yc updates                   # List all weekly updates
yc show <id>                 # Show a single update in detail
yc new                       # Submit new weekly update (interactive)
yc new --metric 5 --morale 7 --talked-to 3   # Non-interactive

# a16z Speedrun
yc speedrun template         # Generate JSON template
yc speedrun apply            # Interactive application
yc speedrun apply --from-json app.json   # Submit from JSON file
yc speedrun apply --from-json app.json --dry-run  # Validate without submitting
yc speedrun upload-deck deck.pdf   # Upload pitch deck

# South Park Commons
yc spc info                  # Show form URLs and program details
yc spc template              # Generate JSON template (fellowship)
yc spc template --type membership  # Template for community membership
yc spc apply                 # Interactive application
yc spc apply --from-json app.json  # Fill from JSON file
yc spc apply --from-json app.json --dry-run --headed  # Preview
yc spc open                  # Open form in browser

# Discover Programs
yc discover                  # Overview — deadlines + rolling programs
yc discover list             # Browse all 24+ programs
yc discover list --type fellowship   # Filter by type
yc discover list --stage pre-seed    # Filter by stage
yc discover deadlines        # Upcoming deadlines sorted by date
yc discover show yc          # Full details for a program
yc discover search "deep tech"       # Search by name/focus/description
yc discover open yc          # Open application page in browser
```

## YC创业学校相关命令

### `yc whoami`
- 测试连接并显示用户信息（姓名、学习进度、项目ID）。

### `yc dashboard`
- 显示您的创业学校进度面板：
  - 当前的连续更新周数
  - 课程完成情况
  - 下一个课程任务
  - 最近的每周更新状态（是否已提交）

### `yc updates`
- 列出所有每周的更新记录，包括各项指标、团队士气评分和重要事项。

### `yc show <id>`
- 详细显示单个更新的内容，包括目标及其完成状态。

### `yc new`
- 提交新的每周更新记录。默认以交互式模式运行（会提示用户填写每个字段）。

**交互式模式：**
```bash
yc new
# Prompts for: metric value, morale, users talked to, changes, blockers, goals
```

**自动化模式：**
```bash
yc new \
  --metric 10 \
  --morale 8 \
  --talked-to 5 \
  --change "Shipped MVP to first 10 users" \
  --blocker "Payment integration delayed" \
  --learned "Users want simpler onboarding" \
  --goal "Launch public beta" \
  --goal "Set up analytics"
```

## a16z速成计划相关命令

### `yc speedrun template`
- 生成a16z速成计划申请的JSON模板。保存后，填写相关信息，再使用`--from-json`选项提交。

### `yc speedrun apply`
- 提交a16z速成计划申请。有两种提交方式：
  - **交互式模式**：系统会提示用户填写所有字段。
  - **从JSON文件提交**：适用于自动化流程或重复提交的情况。

### `yc speedrun upload-deck <file>`
- 上传项目提案的PDF文件，并获取用于申请的GCS（Google Cloud Storage）链接。

```bash
yc speedrun upload-deck pitch.pdf
```

### a16z速成计划的分类
```
B2B / Enterprise Applications
Consumer Applications
Deep Tech
Gaming / Entertainment Studio
Infrastructure / Dev Tools
Healthcare
GovTech
Web3
Other
```

## 全局选项

- `--cookie-source <browser>`：指定从哪个浏览器中读取cookie（支持chrome、safari、firefox）。默认为chrome。
- `--chrome-profile <name>`：指定特定的Chrome浏览器配置文件路径。
- `--json`：以原始JSON格式输出结果（适用于脚本编写）。

## South Park Commons相关命令

- SPC项目申请使用Airtable表格进行管理。该CLI通过Playwright（无头Chromium）自动填写并提交表单。

### `yc spc info`
- 显示可申请的SPC项目及其对应的Airtable表单链接。

### `yc spc template`
- 生成SPC项目的JSON申请模板。

```bash
yc spc template                    # Founder Fellowship (default)
yc spc template --type membership  # Community Membership
```

### `yc spc apply`
- 通过Playwright（无头浏览器）填写并提交SPC项目申请。

### `yc spc open`
- 在默认浏览器中打开SPC项目的申请页面。

```bash
yc spc open                    # Founder Fellowship
yc spc open --type membership  # Community Membership
```

### SPC项目列表

| 项目名称 | 资金支持 | 项目时长 |
|---------|---------|----------|
| Founder Fellowship | 40万美元（初始投资）+ 随后追加60万美元 | 每年春季/秋季招生 |
| Community Membership | 无资金支持 | 最长6个月 |

## 项目查找相关命令

- 查找24家以上的加速器、奖学金项目和孵化器，包括截止日期、项目详情和申请链接。
- `yc discover`：查看所有开放或即将截止的项目的概览。
- `yc discover list`：以表格形式列出所有项目。支持过滤选项：
  - `--type <type>`：筛选类型（加速器、奖学金、孵化器、社区项目）
  - `--stage <stage>`：筛选项目阶段（预创意阶段、种子阶段）
  - `--focus <focus>`：按领域筛选（人工智能、深度科技、金融科技等）
  - `--tier <tier>`：筛选项目级别（1级：精英项目；2级：主要项目；3级：知名项目）
  - `--json`：以JSON格式输出结果
- `yc discover deadlines`：按截止日期排序的所有即将截止的项目。
- `yc discover show <slug>`：查看特定项目的详细信息（投资条款、股权结构、截止日期、重点领域、申请链接）。
- `yc discover search <query>`：按名称、领域或描述搜索项目。
- `yc discover open <slug>`：在默认浏览器中打开项目的申请页面。

## 工作流程

- **每周更新流程**：```bash
yc dashboard            # Check status
yc new                  # Submit if needed
yc updates              # Verify
```

- **通过Claude Code提交a16z速成计划申请**：
  - 当用户决定申请a16z速成计划时，生成JSON模板，填写相关信息后提交。

- **通过Claude Code提交SPC项目申请**：```bash
yc spc template > /tmp/spc-app.json                        # Generate template
# ... Claude fills in the JSON ...
yc spc apply --from-json /tmp/spc-app.json --dry-run --headed  # Preview in browser
yc spc apply --from-json /tmp/spc-app.json                     # Submit
```

- **项目发现流程**：```bash
yc discover                         # What's open right now?
yc discover list --type fellowship  # Browse fellowships
yc discover show yc                 # Deep dive on YC
yc discover open yc                 # Open YC application
```

## 认证要求

- **YC创业学校**：需要从Chrome浏览器中提取会话cookie（请先登录[startupschool.org]）。
- **a16z速成计划**：无需认证（API为公开接口）。
- **South Park Commons**：无需认证，使用Playwright（无头Chromium）自动填写Airtable表单。