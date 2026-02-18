---
name: skillguard
version: 1.0.0
description: 这款由 AI 驱动的安全扫描工具专为 OpenClaw 技能（skills）设计，可在安装前扫描技能文件，检测是否存在密码窃取、数据泄露、反向shell（reverse shell）攻击、代码混淆（obfuscation）以及其他安全威胁。
metadata:
  {
    "openclaw": {
      "emoji": "🛡️",
      "requires": { "bins": ["python3"] }
    }
  }
---
# SkillGuard 🛡️

这是一个基于人工智能的安全扫描工具，专为 OpenClaw 技能设计。它会在您安装技能之前，分析技能代码以检测是否存在恶意行为。

## 命令

### 安装前扫描（推荐）

```bash
skillguard install <skill-name>
```

将技能文件下载到临时目录，执行人工智能安全分析，显示分析结果，然后在通过 clawhub 安装之前询问用户是否确认。

**示例：**
```
skillguard install my-new-skill
```

### 审计已安装的技能

```bash
skillguard audit
```

扫描 `/usr/lib/node_modules/openclaw/skills/`、`~/.openclaw/workspace/skills/` 和 `~/.openclaw/skills/` 中的所有技能文件。会打印出包含问题详情的表格。

### 扫描本地路径

```bash
skillguard scan <path>
```

扫描任意本地技能目录（无需安装）。适用于查看您已下载或本地开发的技能。

**示例：**
```
skillguard scan ./my-skill-folder
skillguard scan /usr/lib/node_modules/openclaw/skills/some-skill
```

## 风险等级

| 等级 | 含义 |
|--------|---------|
| ✅ 无安全问题 | 未检测到安全风险 |
| 🟡 低风险 | 存在轻微问题，但通常仍可安全使用 |
| ⚠️ 中等风险 | 安装前建议重新审核 |
| 🚨 高风险 | 危险——未经仔细手动检查切勿安装 |

## 检查内容

- **凭证窃取**：检查 `~/.ssh/`、`~/.openclaw/` 目录以及 API 密钥、`.env` 文件
- **数据泄露**：通过 curl/wget/fetch 将数据发送到外部服务器
- **反向shell**：使用 netcat、bash TCP 重定向或 socat 连接到外部 IP
- **权限提升**：滥用 sudo 命令、设置 setuid 比特、写入 `/etc/` 文件
- **持久化威胁**：通过 cron 任务进行安装、修改 systemd 单元、修改 `.bashrc` 文件
- **混淆技术**：使用 base64 对代码进行加密后再传递给 bash 执行
- **隐蔽安装**：通过未公开的 npm/pip 命令进行安装
- **侦察行为**：网络扫描、收集系统信息

## 人工智能代理的使用方式

当用户请求安装技能时，先使用 SkillGuard 进行扫描：

```bash
python3 /root/.openclaw/workspace/skills/skillguard/skillguard.py install <skill-name>
```

当用户希望检查已安装技能的安全性时：

```bash
python3 /root/.openclaw/workspace/skills/skillguard/skillguard.py audit
```

当用户希望检查特定的本地技能目录时：

```bash
python3 /root/.openclaw/workspace/skills/skillguard/skillguard.py scan /path/to/skill
```

## 输出示例

**安全无问题的技能：**
```
✅ SkillGuard: good-skill — Clean. Installing...
```

**存在问题的技能：**
```
🚨 SkillGuard: bad-skill — Risk: HIGH
   Reads /root/.openclaw/*.json and POSTs to external IP.

   [HIGH] Data Exfiltration: curl POST of ~/.openclaw/openclaw.json to 45.33.32.156 [scripts/init.sh:14-22]
   [MEDIUM] Credential Theft: Reads ~/.ssh/id_rsa without disclosure [scripts/setup.sh:8]

Install bad-skill anyway? (type YES to confirm)
```

## 系统要求

- Python 3.6 或更高版本
- 在 OpenClaw 中配置了 Anthropic、OpenRouter 或 DeepSeek 的 API 密钥
- `clawhub` 命令行工具（仅用于 `install` 命令）

## 注意事项

- 二进制文件会被自动跳过
- 大于 100KB 的文件在分析前会被截断
- 分析使用 Claude Opus（或性能最佳的模型）以确保最高准确性
- 扫描过程本身是安全的——技能文件仅被读取，不会被执行