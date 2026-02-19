---
name: daily-sales-digest
description: >
  **客户每日销售额汇总功能**：  
  该功能支持与Naver Smart Store、Coupang、Beminseller以及POS系统进行集成，以收集销售额数据，并自动生成每日、每周和每月的汇总报告。这些报告可通过Discord、Kakao Chat或电子邮件方式发送给客户。
metadata:
  {
    "openclaw":
      {
        "emoji": "💰",
        "requires": { "bins": ["node"] },
      },
  }
---
# daily-sales-digest

这是一个用于汇总和分析客户每日销售额的技能。

## 功能

1. **数据收集** — 与Naver Smartstore API、Coupang Wing API、Bamib Seller API以及POS系统进行集成
2. **每日汇总** — 每天早上8点之前生成前一天的销售数据摘要（包括总销售额、订单数量和平均客单价）
3. **对比分析** — 自动计算与前一天的变化率、上周同期的变化率以及上个月的对比情况
4. **异常检测** — 当销售额出现急剧增长或下降时立即发送通知（阈值：±30%）
5. **周报/月报** — 自动生成销售报告并进行趋势分析
6. **渠道发送** — 通过Discord、Kakao Chat或电子邮件发送汇总结果

## 快速入门

### 1. 创建配置文件

编辑 `~/.openclaw/workspace/config/daily-sales-digest.json` 文件，设置API密钥和发送渠道：

### 2. 手动执行

#### 昨天销售额汇总

#### 特定日期的销售额

#### 周报

#### 月报

### 3. 自动调度（使用OpenClaw的cron任务）

每天早上8点自动将前一天的销售额摘要发送到Discord：

#### 周报（每周一上午9点）

#### 月报（每月1日上午9点）

### 4. 异常检测通知

当销售额出现急剧增长或下降时，立即通过Discord发送通知：

## 数据收集

数据以JSON格式存储在 `~/.openclaw/workspace/data/sales/` 目录下：

### 数据文件格式

### 手动数据收集

### 输出格式

- **文本格式（默认）**
- **JSON格式**
- **Markdown格式（用于生成报告）**

## 异常检测通知

当销售额变化超过默认阈值（±30%）时，立即发送通知：

## 安全性与数据管理

- API密钥必须保存在 `~/.openclaw/workspace/config/daily-sales-digest.json` 文件中
- 建议将数据文件添加到 `.gitignore` 文件中
- 禁止将敏感信息记录在日志中
- 建议定期归档过期的数据（超过90天的数据）

## 所需依赖项

- Node.js 18及以上版本
- OpenClaw gateway
- （可选）Discord webhook或消息发送功能
- （可选）电子邮件发送功能（如himalaya）

## 故障排除

- **API连接失败**

- **数据缺失**：手动补充缺失的日期数据

### 日程检查

### 未来改进计划

- [ ] 集成Kakao Chat通知功能
- [ ] 开发基于Canvas的仪表盘网页界面
- [ ] 分析各产品的销售额
- [ ] 分析不同时间段的销售模式
- [ ] 基于AI的销售额预测
- [ ] 集成Slack
- [ ] 实现Google Sheets的自动数据更新

## 参考资料

- Naver Commerce API文档：https://developer.naver.com/docs/commerce/commerce-api/commerce-api.md
- Coupang Wing API：https://wing-developers.coupang.com/
- Bamib Seller API：（另行提供）