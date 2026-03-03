# 多渠道收入追踪器

该工具可追踪来自多种渠道的收入（如 GitHub 奖金、ClawHub、toku.agency、交易等），并具备自动分类和 ROI（投资回报率）分析功能。

## 主要功能

- 支持多渠道收入追踪
- 自动对收入进行分类
- 为每个收入渠道计算 ROI
- 提供每日/每周/每月的报告
- 支持目标跟踪
- 支持渠道绩效对比

## 安装

```bash
clawhub install multi-channel-income-tracker
```

## 使用方法

```bash
# Add income
node tracker.js income --source "toku.agency" --amount 50 --description "Code review service"

# Add expense
node tracker.js expense --category "api" --amount 2 --description "OpenAI API"

# View report
node tracker.js report --period "week"

# Channel comparison
node tracker.js channels
```

## 支持的收入渠道

- GitHub 奖金
- ClawHub 技能任务
- toku.agency
- Fiverr
- Medium/YouTube
- 咨询服务
- 自定义收入渠道

## 报告功能

- 按渠道显示收入情况
- 显示每个渠道的 ROI
- 提供收入趋势分析
- 监控目标完成进度
- 显示成本明细

## 许可证

MIT 许可证