# 多平台漏洞赏金扫描器

## 概述

自动扫描 50 多个漏洞赏金和开源软件（OSS）赏金平台，以发现新的机会。节省大量手动搜索的时间。

## 适用场景

在以下情况下使用此工具：
- 您希望在多个平台上寻找新的漏洞赏金机会；
- 您需要自动化每日漏洞赏金扫描；
- 您希望根据技术栈、奖励金额或难度来筛选赏金；
- 您厌倦了手动检查 50 多个网站。

## 安装

**使用自动化脚本：**
```bash
clawhub install multi-bounty-scanner
```

**或手动安装：**
```bash
cd ~/.openclaw/workspace/skills/multi-bounty-scanner
chmod +x scanner.js
npm link
```

## 使用方法

### 基本扫描
```bash
bounty-scan
```

### 按技术栈筛选
```bash
bounty-scan --tech javascript,python,rust
```

### 按最低奖励金额筛选
```bash
bounty-scan --min-reward 100
```

### 导出到 JSON 格式
```bash
bounty-scan --output bounties.json
```

### 与 OpenClaw 集成

将脚本添加到 cron 任务中，实现每日自动扫描：
```bash
openclaw cron add \
  --name "Daily Bounty Scan" \
  --every 24h \
  --session isolated \
  --message "Run: cd ~/.openclaw/workspace/skills/multi-bounty-scanner && node scanner.js"
```

## 配置

创建 `~/.bounty-scanner/config.json` 文件：
```json
{
  "filters": {
    "techStack": ["javascript", "python", "rust"],
    "minReward": 50,
    "platforms": ["github", "code4rena", "immunefi"]
  }
}
```

## 支持的平台

目前已支持的平台：
- ✅ GitHub（带有赏金标签）

即将支持的平台：
- Code4rena
- Immunefi
- HackerOne
- Bugcrowd
- Intigriti
- Algora.io
- 以及更多平台

## 输出结果

扫描器会记录已发现的漏洞，并仅显示新的漏洞。输出内容包括：
- 漏洞标题
- 平台名称
- 奖励金额
- 技术栈
- 网站链接
- 漏洞描述

## 系统要求

- Node.js 18 及以上版本
- 用于扫描 GitHub 的 GitHub CLI（`gh`）

## 价格

- **免费**：仅支持 GitHub 平台的扫描；
- **专业版（5 美元/月）**：支持所有 50 多个平台（即将推出）。

## 技术支持

问题反馈：https://github.com/your-repo/issues

## 许可证

MIT 许可证