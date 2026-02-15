---
name: clawbridge
description: 从 OpenClaw 聊天窗口中运行 Clawbridge 发现功能。
metadata:
  openclaw:
    emoji: "🌉"
    homepage: "https://clawbridge.cloud"
    requires:
      bins: ["clawbridge"]
    install:
      - id: "install-script"
        kind: "shell"
        label: "Install via script (recommended)"
        command: "curl -fsSL https://clawbridge.cloud/install | bash"
        bins: ["clawbridge"]
---

# Clawbridge 技能

> **可选的聊天命令**：用于通过 OpenClaw 启动 Clawbridge。

## 该技能的功能

该技能是一个**“薄触发器”**（thin trigger）——它仅运行 Clawbridge 的命令行界面（CLI），并返回 Vault 的链接。

**该技能不负责数据发现（data discovery）**；所有的业务逻辑都由运行器（runner）处理。

## 行为

当用户输入 `/clawbridge` 时：

1. **执行命令**：在本地运行 `clawbridge run` 命令。
2. **解析输出结果**：提取机器可读的行：
   - `VAULT_URL=...`
   - `CANDIDATES_COUNT=...`
   - `DISCOVERY_SOURCE=...`（可选）
3. **在聊天中回复**：
   - “已完成——找到了 X 个候选人。”
   - “请在此处查看：<vault_url>”

## 使用方法

```
/clawbridge
```

或者通过配置文件来使用：

```
/clawbridge --profile myprofile
```

## 示例输出

```
Done — found 3 candidates.

Review here: https://clawbridge.cloud/app/workspaces/xxx/runs/xxx
```

## 先决条件

**还没有安装 Clawbridge 吗？** 请访问以下链接开始使用：

👉 **https://clawbridge.cloud**

1. 创建账户。
2. 创建工作区。
3. 按照设置指南进行操作。

如果您已经拥有账户：

```bash
# 1. Install runner
curl -fsSL https://clawbridge.cloud/install | bash

# 2. Link workspace (get code from your workspace page)
clawbridge link CB-XXXXXX
```

## 架构

```
User: /clawbridge
        │
        ▼
┌───────────────────────────────┐
│  Skill: exec clawbridge run   │
└───────────────────────────────┘
        │
        ▼
┌───────────────────────────────┐
│  Runner: Discovery workflow   │
│  - Build prompts (private)    │
│  - Call OpenClaw as worker    │
│  - Upload to Vault            │
│  - Print VAULT_URL=...        │
└───────────────────────────────┘
        │
        ▼
┌───────────────────────────────┐
│  Skill: Parse + reply         │
└───────────────────────────────┘
```

## 技术架构模型

- **运行器（Runner）**：负责数据发现策略、提示信息的生成以及候选人的排序。
- **Web 端**：用于查看候选人信息并批准相关操作。
- **该技能（Skill）**：只是一个便捷的聊天快捷方式（可选）。

您无需使用该技能即可直接通过终端运行 `clawbridge run` 命令来使用 Clawbridge。