---
name: openclaw-signet-pro
description: "完整的加密验证套件：支持 SHA-256 签名和篡改检测功能，能够自动拒绝未签名的技能（技能数据），隔离被篡改的技能数据，并提供可信的快照恢复功能。所有这些功能都包含在 openclaw-signet（免费工具）中，同时还配备了自动化的防护措施。"
user-invocable: true
metadata: {"openclaw":{"emoji":"🔏","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Signet Pro

[openclaw-signet](https://github.com/AtlasPA/openclaw-signet)（免费版本）的所有功能，外加自动化防护措施。

**免费版本仅提供检测功能；Pro版本具备阻止、隔离和防御恶意行为的能力。**

## 检测命令（免费版本也提供）

### 生成技能的哈希值

为所有已安装的技能生成SHA-256哈希值，并将其存储在信任清单中。
```bash
python3 {baseDir}/scripts/signet.py sign --workspace /path/to/workspace
```

### 签署单个技能

```bash
python3 {baseDir}/scripts/signet.py sign openclaw-warden --workspace /path/to/workspace
```

### 验证技能状态

将当前技能的状态与信任清单中的签名进行比较，精确报告哪些文件被修改、添加或删除。
```bash
python3 {baseDir}/scripts/signet.py verify --workspace /path/to/workspace
```

### 列出已签署的技能

显示信任清单，包括哈希值、文件数量以及被隔离的技能。
```bash
python3 {baseDir}/scripts/signet.py list --workspace /path/to/workspace
```

### 快速状态检查

提供一键式状态检查：显示技能是否经过验证、是否被篡改、是否未签名以及被隔离的数量。
```bash
python3 {baseDir}/scripts/signet.py status --workspace /path/to/workspace
```

## Pro版本的防护措施

### 拒绝未签名的技能

将未签名的技能从工作区中移除，并将其放入`.quarantine/signet/`目录，同时记录拒绝的原因。
```bash
# Reject all unsigned skills
python3 {baseDir}/scripts/signet.py reject --workspace /path/to/workspace

# Reject a specific unsigned skill
python3 {baseDir}/scripts/signet.py reject untrusted-skill --workspace /path/to/workspace
```

### 隔离被篡改的技能

通过为该技能的目录添加`.quarantined-`前缀来禁用该技能，防止代理程序加载它。同时将篡改的证据（预期哈希值与实际哈希值的对比结果、被修改的文件）记录在`.quarantine/signet/{skill}-evidence.json`文件中。
```bash
python3 {baseDir}/scripts/signet.py quarantine bad-skill --workspace /path/to/workspace
```

### 解除技能的隔离状态

将被隔离的技能恢复到其原始名称，并警告用户在使用前需要重新签署该技能。
```bash
python3 {baseDir}/scripts/signet.py unquarantine bad-skill --workspace /path/to/workspace
```

### 创建已签署技能的快照

为已签署的技能创建一个可信的备份。只有当技能当前通过验证（哈希值与清单一致）时，此操作才会成功。快照存储在`.signet/snapshots/{skill}/`目录中。
```bash
python3 {baseDir}/scripts/signet.py snapshot openclaw-warden --workspace /path/to/workspace
```

### 从快照中恢复技能

从可信的快照中恢复技能。在恢复前会验证快照的完整性，并更新信任清单以反映恢复后的状态。
```bash
python3 {baseDir}/scripts/signet.py restore openclaw-warden --workspace /path/to/workspace
```

### 自动化防护扫描

提供全面的自动化防护扫描功能。建议在会话启动时执行：
1. 根据信任清单验证所有技能。
2. 自动隔离被篡改的技能（并记录证据）。
3. （可选）拒绝未签名的技能（默认设置为不执行此操作）。
4. 为所有通过验证的技能创建/更新快照。
```bash
# Standard protection (quarantine tampered, snapshot clean)
python3 {baseDir}/scripts/signet.py protect --workspace /path/to/workspace

# Strict protection (also reject unsigned skills)
python3 {baseDir}/scripts/signet.py protect --reject-unsigned --workspace /path/to/workspace
```

## 推荐的集成方式

### 会话启动时的集成（Claude Code）

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 scripts/signet.py protect",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 定期防护机制（OpenClaw）

将相关代码添加到`HEARTBEAT.md`文件中，以实现定期防护：
```
- Run skill signature protection (python3 {skill:openclaw-signet-pro}/scripts/signet.py protect)
```

## 防护措施总结

| 命令 | 功能 |
|---------|--------|
| `protect` | 进行全面扫描：验证技能状态、隔离被篡改的技能并创建快照备份 |
| `protect --reject-unsigned` | 进行全面扫描并拒绝未签名的技能 |
| `reject [skill]` | 将未签名的技能移至隔离区 |
| `quarantine <skill>` | 禁用被篡改的技能，并记录证据 |
| `unquarantine <skill>` | 恢复被隔离的技能（建议重新签署） |
| `snapshot <skill>` | 为已验证的技能创建可信备份 |
| `restore <skill>` | 从可信快照中恢复技能 |

## 错误代码

- `0` — 所有技能均通过验证/操作成功
- `1` — 检测到未签名的技能/存在警告
- `2` — 检测到被篡改的技能/存在严重问题

## 无外部依赖

仅依赖Python标准库，无需安装任何第三方库（如pip），也不进行网络请求。所有操作均在本地执行。

## 跨平台兼容性

支持OpenClaw、Claude Code、Cursor以及任何遵循Agent Skills规范的工具。