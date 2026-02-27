---
name: openclaw-snitch
version: 1.0.0
description: >
  OpenClaw的多层阻止列表防护机制：  
  - 对符合禁止模式的工具调用进行强制阻止；  
  - 在代理程序启动时注入安全指令；  
  - 对传入的消息发出警告；  
  - 通过Telegram发送警报；  
  - 默认情况下会阻止对clawhub/clawdhub的访问。
metadata:
  openclaw:
    emoji: "🚨"
    events:
      - agent:bootstrap
      - message:received
      - before_tool_call
---
# openclaw-snitch

这是一个为 OpenClaw 配置的块列表（blocklist）防护机制，具有三层执行机制：

1. **引导指令（Bootstrap Directive）**：将安全策略注入每个代理的上下文中。
2. **消息警告（Message Warning）**：标记包含被阻止词汇的传入消息。
3. **强制阻止（Hard Block）**：拦截并终止相关工具的调用，并通过 Telegram 发送警报。

## 安装

### 钩子（Bootstrap 指令与消息警告）

安装此插件后，将钩子目录复制到您的工作空间中：

```bash
cp -r ~/.openclaw/workspace/skills/openclaw-snitch/hooks/snitch-bootstrap ~/.openclaw/hooks/snitch-bootstrap
cp -r ~/.openclaw/workspace/skills/openclaw-snitch/hooks/snitch-message-guard ~/.openclaw/hooks/snitch-message-guard
```

然后在 `openclaw.json` 中启用它们：

```json
{
  "hooks": {
    "snitch-bootstrap": { "enabled": true },
    "snitch-message-guard": { "enabled": true }
  }
}
```

### 插件（强制阻止与 Telegram 警报）

对于强制阻止机制，需要安装相应的 npm 包：

```bash
npm install -g openclaw-snitch
```

接着将其添加到 `openclaw.json` 中：

```json
{
  "plugins": {
    "allow": ["openclaw-snitch"]
  }
}
```

安装完成后，锁定插件文件，以防止代理自行修改它们：

```bash
chmod -R a-w ~/.openclaw/extensions/openclaw-snitch
```

## 配置

在 `openclaw.json` 的 `plugins.config.openclaw-snitch` 部分进行配置：

```json
{
  "plugins": {
    "config": {
      "openclaw-snitch": {
        "blocklist": ["clawhub", "clawdhub"],
        "alertTelegram": true,
        "bootstrapDirective": true
      }
    }
  }
}
```

| 参数 | 默认值 | 说明 |
|-----|---------|-------------|
| `blocklist` | `["clawhub", "clawdhub"]` | 需要阻止的词汇列表（不区分大小写，以单词边界进行匹配） |
| `alertTelegram` | `true` | 向被阻止的来源地址发送 Telegram 警报 |
| `bootstrapDirective` | `true` | 将安全指令注入每个代理的启动上下文中 |

### 基于环境变量的钩子配置

如果设置了 `SNITCH_BLOCKLIST`（以逗号分隔的列表），则钩子会使用该列表进行匹配；否则将使用默认值：

```bash
SNITCH_BLOCKLIST=clawhub,clawdhub,myothertool
```

## 被阻止的情况

当 **工具名称** 或 **工具参数** 包含被阻止的词汇时，防护机制会触发。这可以防止代理间接调用被禁止的工具（例如，通过 `exec` 命令并传入 `clawhub install` 作为参数）。

## 安全注意事项：

- 位于 `~/.openclaw/hooks/` 目录下的钩子会无条件地被执行，因此具有较高的防篡改能力。
- 插件层需要 `plugins.allow` 配置才能生效；如果代理修改了 `openclaw.json`，钩子仍然会继续运行。
- 通过设置扩展名目录的权限为 `chown root:root`，可以防止代理自行修改插件文件。