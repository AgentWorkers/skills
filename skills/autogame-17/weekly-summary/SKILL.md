# 周度总结生成器

**功能描述：** 自动生成代理活动的周度总结，包括进化周期和收益情况。
**使用方法：** `node skills/weekly-summary/index.js`

## 主要特性：
- 扫描 `RECENT EVENTS.md` 和 `memory/evolution/events.jsonl` 文件
- 计算进化成功率
- 汇总收益数据（模拟数据或实际数据）
- 生成 Feishu Card 的 JSON 格式数据