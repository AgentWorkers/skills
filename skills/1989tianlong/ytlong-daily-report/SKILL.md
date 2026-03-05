---
name: daily-report-generator
description: 根据 Git 提交记录、日历事件和任务列表自动生成每日/每周的工作报告。当您需要快速生成专业的工作报告而无需手动操作时，可以使用此功能。
tags: [productivity, automation, report, git, calendar]
---
# 日报生成器

通过分析以下数据，自动生成专业的每日/每周工作报告：
- 当日/当周的 Git 提交记录
- 日历事件
- 任务完成情况

## 主要功能

- **多数据源聚合**：从 Git、日历和任务管理工具中提取数据
- **智能汇总**：自动将相关活动归类
- **多种输出格式**：Markdown、HTML、纯文本
- **语言支持**：支持中文和英文输出

## 使用方法

### 生成今日报告

```bash
node index.js today
```

### 生成每周报告

```bash
node index.js week
```

### 生成自定义日期范围的报告

```bash
node index.js range --from 2024-01-01 --to 2024-01-07
```

### 指定输出格式

```bash
node index.js today --format html
node index.js week --format markdown
```

## 配置方法

在项目根目录下创建一个 `.reportrc.json` 文件：

```json
{
  "git": {
    "enabled": true,
    "repos": ["./", "../other-project"]
  },
  "calendar": {
    "enabled": true,
    "sources": ["google", "apple"]
  },
  "tasks": {
    "enabled": true,
    "sources": ["apple-reminders"]
  },
  "output": {
    "language": "zh-CN",
    "format": "markdown",
    "includeStats": true
  }
}
```

## 输出示例

```markdown
# 工作日报 - 2024年1月15日

## 完成的任务
- ✅ 完成用户认证模块开发
- ✅ 修复登录页面样式问题
- ✅ 代码审查：PR #123

## Git 提交
- feat: 添加双因素认证 (abc123)
- fix: 修复移动端显示问题 (def456)
- docs: 更新 API 文档 (ghi789)

## 会议
- 10:00 产品需求评审会
- 14:00 技术方案讨论

## 明日计划
- 继续开发支付模块
- 参加团队周会
```

## 系统要求

- Node.js 18 及以上版本
- Git（用于提交记录分析）
- 可选：日历访问权限（支持 Google/Apple 日历服务）

## 安装方法

```bash
npm install
```

## 许可证

MIT 许可证