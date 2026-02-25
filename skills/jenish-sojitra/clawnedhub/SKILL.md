---
name: clawned
description: 这是一个安全代理工具，用于盘点已安装的 OpenClaw 技能（功能模块），分析其中可能存在的威胁，并将分析结果同步到您的 Clawned 仪表板中。
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": { "bins": ["python3"], "env": ["CLAWNED_API_KEY"] },
        "optionalEnv": ["CLAWNED_SERVER"],
        "homepage": "https://clawned.io",
      },
  }
---
# Clawned — OpenClaw 的安全代理

该工具能够自动检测所有已安装的技能（skills），分析其中可能存在的安全威胁，并将分析结果同步到您的 Clawned 仪表板中。

## 设置

请在 `openclaw.json` 文件中配置您的 API 密钥：

```json
{
  "skills": {
    "entries": {
      "clawned": {
        "enabled": true,
        "env": {
          "CLAWNED_API_KEY": "cg_your_api_key_here",
          "CLAWNED_SERVER": "https://api.clawned.io"
        }
      }
    }
  }
}
```

## 命令

### 将所有已安装的技能同步到仪表板

```bash
python3 {baseDir}/scripts/agent.py sync
```

### 本地扫描单个技能

```bash
python3 {baseDir}/scripts/agent.py scan --path <skill-directory>
```

### 列出所有检测到的技能

```bash
python3 {baseDir}/scripts/agent.py inventory
```

### 检查代理状态

```bash
python3 {baseDir}/scripts/agent.py status
```

## 数据与隐私

**在“同步”操作期间（默认操作）：**
- 仅发送技能的元数据：名称、所有者、slug、版本
- 不会上传任何文件内容
- 绝不会读取 `.env` 文件或任何敏感信息

**在“scan --path”操作期间（仅限用户主动触发）：**
- 会从指定的技能目录中读取源文件（`.md`、`.py`、`.js` 等）进行安全分析
- `.env` 文件将被排除在扫描范围之外
- 文件内容会被发送到 Clawned 服务器进行安全分析

**本地配置访问：**
- 仅读取 `~/.openclaw/openclaw.json` 文件以确定技能目录的位置（`extraDirs` 路径）
- 不会从配置文件中读取任何凭据或敏感信息

## 自动同步

通过 OpenClaw 的 cron 任务，每 6 小时自动执行一次同步操作：

```json
{
  "jobs": [
    {
      "schedule": "0 */6 * * *",
      "command": "Run clawned sync to check all installed skills",
      "description": "Security scan every 6 hours"
    }
  ]
}
```