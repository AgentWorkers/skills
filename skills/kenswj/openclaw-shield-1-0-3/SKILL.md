# OpenClaw Shield

这是一款专为AI代理设计的企业级安全扫描工具。通过静态分析、运行时防护机制以及与ClamAV的集成，能够有效检测凭证盗用、数据泄露和恶意代码。同时提供审计日志记录及防篡改的安全报告。

**适用场景：** 安全扫描、威胁检测、代码审计、AI代理的运行时保护

**相关说明：**

**代码仓库：** https://github.com/pfaria32/OpenClaw-Shield-Security

## 主要功能

### 静态扫描
- 检测凭证盗用、数据泄露及破坏性操作
- 基于模式的分析（无需依赖外部库）
- 仅使用Python标准库（零供应链风险）
- 执行前进行扫描

### 运行时防护
- 文件/网络/执行操作的白名单管理
- 输出内容的安全性处理
- 政策执行
- 实时防护机制

### 集成功能
- 与ClamAV集成（包含360万个病毒签名）
- 发现严重问题时通过Telegram发送警报
- 使用哈希链技术记录审计日志
- 提供防篡改的安全日志

## 安装方法

```bash
cd /home/node/.openclaw/workspace
git clone https://github.com/pfaria32/OpenClaw-Shield-Security.git projects/OpenClaw-Shield

# Test the scanner
python3 projects/OpenClaw-Shield/src/scanner.py /path/to/scan

# Deploy (see repository README for full setup)
```

## 使用说明

### 手动扫描
```bash
python3 projects/OpenClaw-Shield/src/scanner.py workspace --output shield-report.json
```

### 每日自动扫描
请设置定时任务（详见代码仓库中的部署指南）：
```bash
# Daily at 3 AM UTC
0 3 * * * /path/to/scan-script.sh
```

### 运行时防护（可选）
配置允许执行的操作列表并启用运行时保护（具体操作请参考代码仓库中的`openclaw-config.py`文件）。

## 系统状态

✅ 已在该实例（clawdbot-toronto）上成功部署：
- 每日扫描时间：UTC时间凌晨3:00
- ClamAV防护功能已启用（针对整个主机）
- 运行时防护功能已配置（默认未启用）

## 技术来源

**灵感来源：** Manolo Remiddi的Resonant项目  
**原始代码：** https://github.com/ManoloRemiddi/resonantos-open-system-toolkit/blob/main/BUILD_YOUR_OWN_SHIELD.md

开发理念：** “不要轻信，务必验证。”

## 文档资料

完整的文档、威胁模型及部署指南请参见代码仓库的README文件。