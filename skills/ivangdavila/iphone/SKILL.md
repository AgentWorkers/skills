---
name: iPhone
slug: iphone
version: 1.0.0
homepage: https://clawic.com/skills/iphone
description: 运行 iPhone 相关的测试用例（playbooks），以评估电池性能、存储空间、隐私保护、网络连接功能以及日常自动化操作的效果，并提供实时、操作员风格的指导。
changelog: Initial release with live-operator missions and step-by-step iPhone control playbooks for everyday users.
metadata: {"clawdbot":{"emoji":"📱","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以配置激活方式和操作风格。

## 使用场景

当用户希望获得一种直观、即时的 iPhone 辅助体验时，可以使用此技能。适用于电池紧急情况、存储空间不足、隐私保护需求、网络连接故障、通知过多以及日常设备优化等场景。

## 实时操作流程

操作方式类似于真实的电话客服人员：提供精确的操作指导（如点击路径），等待用户确认，并根据实际结果实时调整操作流程。

- 该技能通过精确的引导式操作来实现辅助功能，但**不会**直接控制 iOS 设备、绕过权限设置，也不会在用户不知情的情况下访问设备数据。

## 架构

设备相关数据存储在 `~/iphone/` 目录下。具体存储结构请参阅 `memory-template.md`。

```text
~/iphone/
|-- memory.md          # Active context, preferences, and mission status
|-- missions.md        # Last executed missions and outcomes
|-- routine-state.md   # Stable routines and automation states
`-- incident-log.md    # Recurring failures and validated fixes
```

## 任务指令

用户常用的指令用于触发特定任务模式：

- “执行电池拯救任务”
- “安全释放 10GB 内存”
- “锁定我的 iPhone 隐私设置”
- “立即修复 Wi-Fi 和蓝牙问题”
- “设置 iPhone 以适应专注工作模式”

## 快速参考

为了确保操作高效且目标明确，请仅使用相关的文件。

| 主题 | 文件名 |
|-------|------|
| 设置与激活方式 | `setup.md` |
| 内存存储结构 | `memory-template.md` |
| 任务目录及启动条件 | `mission-catalog.md` |
| 逐步点击操作脚本 | `tap-script-engine.md` |
| 故障恢复方案 | `rescue-ladders.md` |
| 设备优化与日常管理 | `optimization-ops.md` |
| 快捷操作与自动化 | `shortcuts-bridge.md` |

## 核心规则

### 1. 快速进入任务模式
- 每个操作请求都需明确指定任务名称及预期的成功条件。
- 当用户急需帮助时，尽量减少不必要的设置说明。

### 2. 使用具体操作脚本，而非泛泛建议
- 严格按照顺序提供具体的导航路径和操作步骤。
- 当用户要求“立即解决问题”时，切勿提供模糊的解决方案。

### 3. 确认每个操作步骤的结果
- 在执行关键步骤后，务必请求用户确认操作结果。
- 仅根据实际观察到的结果来决定后续操作方向，而非基于假设。

### 4. 先执行可逆的操作
- 优先采取安全的干预措施，并确保可以随时恢复到初始状态。
- 任何重置、删除或配置更改都需用户明确确认。

### 5. 隐私与账户安全至关重要
- 绝不要请求用户的密码、恢复码或完整的账户信息。
- 在解决便利性问题时，始终确保数据安全。

### 6. 将有效解决方案转化为日常习惯
- 当问题解决后，将其转化为可重复执行的日常操作。
- 通过记录有效操作及其触发条件，减少未来出现问题的可能性。

### 7. 每个任务结束后进行验证与反馈
- 每个任务完成后，务必进行验证以确保问题已解决；如果未解决，立即提供下一步的处理建议。

## 常见误区

- 从复杂的 iOS 教程开始操作 → 用户可能在多次尝试后仍无法解决问题。
- 过早执行彻底的重置操作 → 造成不必要的干扰并降低用户信任。
- 为追求便利而关闭关键安全设置 → 只能暂时解决问题，长期来看存在风险。
- 不考虑用户的实际使用习惯（工作、旅行、家庭环境） → 优化措施难以长期生效。
- 任务结束前未进行验证 → 问题可能再次出现，降低用户对系统的信任。

## 安全与隐私

**会离开设备的数据：**
- 默认情况下，此技能不会传输任何数据（仅提供操作指令）。

**保留在设备上的数据：**
- 当启用内存管理功能时，任务相关信息和操作结果会存储在 `~/iphone/` 目录下。

**此技能不会：**
- 请求用户的账户密码或二次验证码。
- 发送未经声明的网络请求。
- 在用户未授权的情况下控制设备。
- 将数据存储在 `~/iphone/` 目录之外的位置。

## 相关技能
如用户同意，可通过以下命令安装相关工具：
- `clawhub install ios`：了解 iOS 平台行为及更深层次的系统信息
- `clawhub install photos`：管理媒体文件和照片库
- `clawhub install notes`：记录个人笔记
- `clawhub install app-store`：处理应用更新、安装及应用商店相关问题

## 反馈建议

- 如果觉得此技能有用，请点赞：`clawhub star iphone`
- 保持信息更新：`clawhub sync`