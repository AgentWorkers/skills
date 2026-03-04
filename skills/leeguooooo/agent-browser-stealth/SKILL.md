---
name: agent-browser-stealth
description: 一种基于 `agent-browser-stealth` 的 OpenClaw 浏览器自动化工具，优先采用隐蔽策略。适用于需要处理受机器人保护网站、需要规避指纹识别机制的流程、涉及验证码的界面、需要保持登录状态的任务、针对地区敏感目标（如 Shopee/TikTok 等电商平台）的场景，或是任何需要以较低风险进行网页操作自动化的场景。
homepage: https://github.com/leeguooooo/agent-browser
---
# OpenClaw 的 `agent-browser-stealth` 技能

当任务需要网页自动化处理以及提升系统的抗机器人攻击能力时，请使用此技能。

## 该技能的重点：

- 使用 `agent-browser-stealth` 包中的 `agent-browser` 命令行工具（CLI）。
- 优先选择稳定、安全的交互方式，而非一次性、容易出错的脚本。
- 保持命令执行的确定性：`打开页面 -> 截取页面快照 -> 执行操作 -> 重新获取页面快照`。
- 通过模拟人类操作的方式减少机器人的行为特征，并实现会话的稳定复用。

## 安装与基本配置

```bash
pnpm add -g agent-browser-stealth
agent-browser install
agent-browser --version
```

如果您的环境中使用的是默认的 CDP（Content Delivery Protocol）模式，该 CLI 会首先尝试连接到 `localhost:9333`，然后自动进行连接。如有需要，您也可以明确指定 `--cdp` 或 `--auto-connect` 参数。

## 标准执行流程

```bash
agent-browser open <url>
agent-browser wait --load networkidle
agent-browser snapshot -i
# choose refs (@e1, @e2, ...)
agent-browser click @eN
agent-browser fill @eM "..."
agent-browser snapshot -i
```

尽可能使用从页面快照输出中获取的引用信息（`@e1`）。

## 抗机器人攻击策略：

1. 对于敏感目标，优先选择使用“headed”模式进行操作：

```bash
agent-browser --headed --session-name shop open https://example.com
```

2. 重用会话状态，以避免重复产生新的识别特征（即避免重复的“冷启动”行为）：

```bash
agent-browser --session-name shop open https://example.com
```

3. 保持操作过程符合人类使用习惯：

```bash
agent-browser type @e2 "query" --delay 120
agent-browser wait 1200-2600
```

4. 对于支持内容编辑的页面，使用键盘操作模式：

```bash
agent-browser click "[contenteditable='true']"
agent-browser keyboard type "Hello world" --delay 90
```

5. 如果文本中确实需要包含 `--delay` 参数，请使用 `--` 来终止参数解析：

```bash
agent-browser type @e2 -- "--delay 120"
agent-browser keyboard type -- "--delay 120"
```

## 地区敏感型网站

对于受地区限制的网站，直接打开目标域名，并让系统自动调整区域设置和时间区设置：

```bash
agent-browser open https://shopee.tw
```

只有在任务明确要求的情况下，才需要手动修改区域设置和时间区设置。

## 故障恢复策略：

如果遇到连接被阻止或系统运行不稳定的情况：

1. 重新尝试使用 `--headed` 模式。
2. 重用现有的会话名称（`--session-name` 参数）。
3. 减慢操作速度（例如使用 `wait` 或 `type --delay`）。
4. 重新打开页面，并使用 `snapshot -i` 命令重新获取页面快照。

## 最小化操作步骤：

- 登录流程：

```bash
agent-browser --session-name account open https://example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "$USERNAME"
agent-browser fill @e2 "$PASSWORD"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
```

- 搜索并捕获所需信息：

```bash
agent-browser open https://example.com
agent-browser snapshot -i
agent-browser type @e2 "iphone" --delay 120
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser screenshot result.png
```

## OpenClaw 的输出要求：

使用此技能后，需要返回以下信息：

- 执行的具体命令。
- 页面状态的关键变化（如 URL、标题或重要元素的文本内容）。
- 遇到的任何抗机器人攻击措施及其具体内容。
- 下一步安全的操作建议。