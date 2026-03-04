---
name: chitin-moat
description: >
  根据通信渠道的信任级别，为AI代理实施上下文相关的权限限制。这些限制会约束代理的功能（如执行命令、文件读写、访问敏感信息以及发送消息），而非基于消息内容本身。这种机制有助于防止社会工程攻击和在群聊中注入恶意指令。适用场景包括：  
  (1) 为每个频道或群组配置代理权限；  
  (2) 为公共Discord或Telegram频道设置只读模式；  
  (3) 实现不同的信任等级（如主权级、受信任级、保护级、观察级或静默级）；  
  (4) 审计代理的频道权限；  
  (5) 当用户提及“信任频道”、“频道权限”或“只读模式”时。
---
# 凝胶质保护层（Chitin Moat）

根据对话发生的环境来执行相应的代理权限控制。

## 信任等级

| 等级 | 名称 | 权限 |
|-------|------|-------------|
| 0 | `sovereign` | 完全自主权（与经过验证的所有者进行一对一通信） |
| 1 | `trusted` | 读写权限，可使用特定工具，但不能访问机密信息（属于已知的私密群体） |
| 2 | `guarded` | 仅对@mention消息作出响应，无法使用任何工具（半公开环境） |
| 3 | `observer` | 仅能进行响应（公共频道） |
| 4 | `silent` | 无法进行任何交互（被屏蔽的频道） |

## 配置

在代理工作区的根目录下创建 `chitin-trust-channels.yaml` 文件：

```yaml
version: "0.1"

owner:
  telegram: "<owner_user_id>"

channels:
  - id: "telegram:<owner_user_id>"
    level: sovereign

  - id: "discord:<server_id>"
    level: guarded
    overrides:
      - channel: "owners-lounge"
        level: trusted
      - channel: "pro-*"
        level: trusted

  - id: "telegram:group:*"
    level: observer

defaults:
  unknown_channel: observer
  unknown_dm: guarded
```

## 设置步骤

1. 复制示例配置文件：`cp references/example-config.yaml chitin-trust-channels.yaml`
2. 根据实际情况修改频道ID和所有者信息。
3. 运行验证脚本：`python3 scripts/validate_config.py chitin-trust-channels.yaml`
4. 运行审计脚本：`python3 scripts/audit_channels.py chitin-trust-channels.yaml`

## 权限矩阵

完整的权限与信任等级对应关系请参见 `references/permission-matrix.md`。

## 脚本

- `scripts/validate_config.py <config>` — 验证信任通道配置文件的有效性。
- `scripts/audit_channels.py <config>` — 根据配置文件审核当前频道的权限设置，并报告任何不一致之处。
- `scripts/resolve_channel.py <config> <channel_id>` — 为指定的频道ID确定其信任等级。

## 与 AGENTS.md 的集成

将以下内容添加到代理的工作区配置中：

```markdown
## Chitin Moat
Before responding in any channel, resolve the trust level using `chitin-trust-channels.yaml`.
Constrain capabilities to the resolved level. Never escalate beyond the channel ceiling.
```