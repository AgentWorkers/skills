---
name: openclaw-warden-pro
description: "全套工作区安全解决方案：能够检测未经授权的修改行为，扫描潜在的命令注入攻击模式，并自动采取应对措施（如快照恢复、技能隔离、Git回滚以及自动化防护扫描）。这是为代理工作区提供的完整安装后安全防护层。"
user-invocable: true
metadata: {"openclaw":{"emoji":"🛡️","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Warden Pro

[openclaw-warden](https://github.com/AtlasPA/openclaw-warden) 的所有功能（免费版本）+ 自动化应对措施。

**免费版本仅能检测威胁；Pro 版本能够对这些威胁做出响应。**

## 检测命令（免费版本中也包含）

```bash
python3 {baseDir}/scripts/integrity.py baseline --workspace /path/to/workspace
python3 {baseDir}/scripts/integrity.py verify --workspace /path/to/workspace
python3 {baseDir}/scripts/integrity.py scan --workspace /path/to/workspace
python3 {baseDir}/scripts/integrity.py full --workspace /path/to/workspace
python3 {baseDir}/scripts/integrity.py status --workspace /path/to/workspace
python3 {baseDir}/scripts/integrity.py accept SOUL.md --workspace /path/to/workspace
```

## Pro 版本的应对措施

### 从快照中恢复

将被篡改的文件恢复到其基线快照状态。在设置基线时，关键文件、配置文件和技能文件会自动被创建快照。

```bash
python3 {baseDir}/scripts/integrity.py restore SOUL.md --workspace /path/to/workspace
```

### Git 回滚

将文件恢复到其最后一次提交的 Git 状态。

```bash
python3 {baseDir}/scripts/integrity.py rollback SOUL.md --workspace /path/to/workspace
```

### 将技能置于隔离状态

通过重命名相关目录来禁用可疑技能。代理程序将不会加载被隔离的技能。

```bash
python3 {baseDir}/scripts/integrity.py quarantine bad-skill --workspace /path/to/workspace
```

### 解除技能的隔离状态

在调查后，恢复被隔离的技能。

```bash
python3 {baseDir}/scripts/integrity.py unquarantine bad-skill --workspace /path/to/workspace
```

### 保护（自动响应）

一次性完成全面扫描和自动应对措施：恢复被篡改的关键文件，隔离恶意技能，并标记剩余的问题。这是启动会话时推荐的命令。

```bash
python3 {baseDir}/scripts/integrity.py protect --workspace /path/to/workspace
```

## 推荐的集成方式

### 会话启动钩子（Claude Code）

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 scripts/integrity.py protect",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Heartbeat（OpenClaw）

将相关代码添加到 HEARTBEAT.md 文件中，以实现定期保护：
```
- Run workspace integrity protection (python3 {skill:openclaw-warden-pro}/scripts/integrity.py protect)
```

### 安装新技能后

运行 `protect` 命令，自动隔离修改了工作区文件的技能。

## 监控内容

| 类别 | 文件 | 警报级别 |
|----------|-------|-------------|
| **关键文件** | SOUL.md, AGENTS.md, IDENTITY.md, USER.md, TOOLS.md, HEARTBEAT.md | 警告 |
| **内存** | memory/*.md, MEMORY.md | 信息提示 |
| **配置文件** | 工作区根目录下的 *.json 文件 | 警告 |
| **技能文件** | skills/*/SKILL.md | 警告 |

## 应对措施汇总

| 命令 | 动作 |
|---------|--------|
| `protect` | 全面扫描 + 自动恢复 + 自动隔离 + 标记问题 |
| `restore <file>` | 从基线快照中恢复文件 |
| `rollback <file>` | 从 Git 提交历史中恢复文件 |
| `quarantine <skill>` | 通过重命名目录来禁用技能 |
| `unquarantine <skill>` | 恢复被隔离的技能 |

## 无外部依赖

仅依赖 Python 标准库，无需安装任何第三方库（如 pip），也不进行网络调用。所有操作都在本地执行。

## 跨平台兼容性

支持与 OpenClaw、Claude Code、Cursor 以及任何遵循 Agent Skills 规范的工具配合使用。