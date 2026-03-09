---
name: help-and-support
description: 获取帮助、入门指南以及问题报告。当您或用户需要关于钱包的使用帮助、对功能有疑问、希望获得操作步骤指导、首次使用该工具，或者需要报告错误/问题时，请使用此功能。涵盖以下主题：“我该如何使用这个工具？”，“请帮助我入门”，“我是新手”，“某个功能出现了问题”，“如何报告错误”，“这个工具的版本是多少？”
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(fdx status*)", "Bash(fdx call helpNarrative*)", "Bash(fdx call onboardingAssistant*)", "Bash(fdx call reportIssue*)", "Bash(fdx call getAppVersion*)"]
---
# 帮助与支持

您可以获取关于 Finance District 代理钱包的上下文相关帮助、入门指南以及问题报告功能。本技能涵盖了面向用户的支持工具。

## 帮助功能 — 回答问题

当用户对钱包的使用方式有具体疑问时，可以使用此功能：

```bash
fdx call helpNarrative --question "<question>"
```

### 参数

| 参数                | 是否必填 | 说明                                      |
| ---------------------- | -------- | ------------------------------------------- |
| `--question`         | 是       | 需要回答的问题                             |
| `--locale`          | 否       | 语言/地区偏好（例如 `en`、`zh`）                         |
| `--tone`            | 否       | 回答语气（例如 `友好`、`专业`）                         |

### 示例

```bash
fdx call helpNarrative --question "How do I send tokens?"
fdx call helpNarrative --question "What chains are supported?"
fdx call helpNarrative --question "How does the swap work?" --tone technical
```

## 入门助手 — 指导新用户

当用户是新手或需要了解某个特定主题的详细操作步骤时，可以使用此功能：

```bash
fdx call onboardingAssistant --question "<question>"
```

### 参数

| 参数                | 是否必填 | 说明                                      |
| ---------------------- | -------- | ------------------------------------------- |
| `--question`         | 是       | 需要指导的主题或问题                             |
| `--context`          | 否       | 用户的额外情况说明                             |
| `--locale`          | 否       | 语言/地区偏好                             |
| `--tone`            | 否       | 回答语气                             |

### 示例

```bash
# First-time user
fdx call onboardingAssistant --question "I just signed up, what should I do first?"

# With context
fdx call onboardingAssistant \
  --question "How do I start earning yield?" \
  --context "I have USDC on Ethereum"
```

## 报告问题 — 错误报告

当用户遇到问题时，可以使用此功能进行问题报告：

```bash
fdx call reportIssue \
  --title "<short title>" \
  --description "<detailed description>"
```

### 参数

| 参数                | 是否必填 | 说明                                      |
| ---------------------- | -------- | --------------------------------------------------------- |
| `--title`           | 是       | 问题的简要概述                             |
| `--description`     | 是       | 问题发生的详细情况                             |
| `--severity`        | 否       | 问题严重程度（例如 `低`、`中`、`高`、`紧急`）                   |
| `--category`        | 否       | 问题类别（例如 `错误`、`功能请求`、`疑问`）                   |

### 示例

```bash
fdx call reportIssue \
  --title "Swap fails on Polygon" \
  --description "Attempting to swap USDC to ETH on Polygon returns a timeout error after 30 seconds" \
  --severity high \
  --category bug
```

## 检查应用版本

此功能用于在错误报告中包含版本信息或验证应用程序的兼容性：

```bash
fdx call getAppVersion
```

## 新用户的操作流程

1. 检查当前状态：`fdx status`
2. 如果用户未登录，请引导他们使用 `authenticate` 功能进行登录
3. 运行入门指导：`fdx call onboardingAssistant --question "我是新手，首先应该做什么？"`
4. 与用户一起逐步完成操作指南
5. 帮助用户了解钱包功能（使用 `wallet-overview` 功能）和充值操作（使用 `fund-wallet` 功能）

## 问题报告的流程

1. 让用户描述遇到的问题
2. 检查应用版本：`fdx call getAppVersion`
3. 检查用户登录状态：`fdx status`
4. 提交问题报告：`fdx call reportIssue --title "..." --description "..." --severity <level>`
5. 向用户确认问题已成功报告

## 先决条件

- `helpNarrative` 和 `onboardingAssistant` 功能无需用户登录即可使用
- `reportIssue` 功能需要用户登录（通过 `fdx status` 检查登录状态，详见 `authenticate` 功能）