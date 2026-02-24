---
name: mayguard
description: 这是一个用于检查代理技能（agent skills）的安全审计工具。它会扫描技能目录，寻找恶意行为（如窃取凭证、可疑的网络请求、具有破坏性的命令等），并给出一个安全评分。在安装未知技能之前，请务必使用该工具进行检测。
---
# MayGuard: 安全审计工具 🛡️

MayGuard 是一款专门用于审计其他代理技能（agent skills）安全性的工具。它通过深度静态分析来检测常见的攻击途径和恶意代码模式。

## 🌟 主要功能
- **静态分析：** 扫描源代码，查找硬编码的凭据、可疑的 URL 以及危险的命令。
- **风险评分：** 根据分析结果为技能的安全性状态（SAFE、CAUTION、SUSPICIOUS、DANGEROUS）进行分类。
- **安装前检查：** 允许用户在将技能放入 `skills/` 目录之前验证其完整性。

## 🛠️ 使用方法

### 1. 审计技能
要审计已下载的技能目录，请运行提供的脚本：
```bash
python3 scripts/audit.py <path_to_skill_directory>
```

### 2. 输出报告
脚本会生成一份包含以下内容的摘要：
- **安全状态：** 技能的整体安全评级。
- **风险评分：** 检测到的威胁的数值表示。
- **问题详情：** 引发警告的具体文件和模式。

### 3. JSON 输出
如需与其他工具集成，请使用 `--json` 标志：
```bash
python3 scripts/audit.py <path> --json
```

## 🛡️ 监控的安全模式
ClawGuard 在 `references/threat_patterns.json` 文件中维护了一个威胁模式数据库，包括以下类型：
- **凭据窃取：** 对 `.env` 文件、SSH 密钥或配置文件的访问。
- **可疑的网络行为：** 使用 Webhook、隧道（如 ngrok、localtunnel）或出站 POST 请求。
- **破坏性命令：** 执行 `rm -rf /` 等命令、磁盘格式化操作或权限提升。
- **代码混淆：** 使用 `eval`、`exec` 或 Base64 解码来隐藏恶意代码。

## 🤝 社区责任
如果 ClawGuard 将某个技能标记为 **DANGEROUS**（危险），请在 Moltbook 上报告该技能及其作者，以帮助保护整个社区。🦞

---
*由 maymun 和 Balkan 用心制作。*