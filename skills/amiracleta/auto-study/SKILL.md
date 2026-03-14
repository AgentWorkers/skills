---
name: auto-study
description: 适用于基于浏览器的学习、测验和练习任务。特别适合使用如Yuketang、Xuexitong、Pintia等类似的学习或问答平台，这些平台需要用户拥有持久的个人资料（profile），并通过代理-浏览器（agent-browser）建立CDP（Content Delivery Platform）连接，同时还需要简洁的答案提示或页面操作指导。
metadata:
  openclaw:
    emoji: "🎓"
    category: "study"
    tags: ["study platform", "practice", "quiz", "automation tasks"]
---
# 自动学习功能

此功能为学习平台提供了浏览器工作流程，适用于日常练习场景。它可以根据需要返回答案、选择选项、填写答案、清除答案并提交它们。

## 使用场景

- 希望在浏览器中自动完成学习平台上的答题任务（如练习题、小测验和作业）。
- 需要获取页面上问题的答案。
- 希望在日常练习页面上选择、填写或清除答案。

## 工作流程

1. 使用指定的持久化网站配置文件和CDP端口启动Chrome浏览器，或连接到已经开启CDP端口的现有Chrome实例。
2. 在执行任何操作之前，先验证当前激活的标签页和URL，然后对页面状态进行快照或检查。
3. 根据用户的需求与页面进行交互，例如选择答案、填写答案、清除答案或点击提交按钮。

## 核心规则

- 默认情况下，将所有页面视为普通练习页面，除非用户另有说明。
- 如果用户请求执行某些操作，应依次执行这些操作，并在每次操作之间稍作停顿（通常约0.1秒）。
- 如果问题以图片形式呈现，直接读取图片内容。
- 如果页面上的DOM可见文本被混淆、加密或显示为无意义的字符，首先尝试理解其含义；如果仍无法理解，请截图后进行回答。
- 当登录状态重要时，对同一网站使用相同的浏览器配置文件。
- 持久化配置文件仅用于辅助登录状态，不能保证自动登录。它可能会恢复cookies、本地存储或仅保存的凭据，因此某些网站可能仍需要用户手动点击登录或确认。
- 通过CDP连接到网站后，先验证当前激活的标签页和URL；如果当前页面不是目标页面，请使用`tab list`功能切换到目标页面。
- 不要重新点击已经与目标状态匹配的选项。
- 尽可能遵循正常用户的操作流程，避免使用普通用户无法完成的操作。
- 保持答案简洁易懂。
- 除非用户明确要求，否则不要自动提交答案。
- 除非用户明确要求，否则不要在网络上进行搜索。

## 输出规则

### 单选题

仅返回最终选择的选项字母。

### 多选题

以逗号分隔的形式返回所有选中的选项字母。

### 填空题或简答题

仅返回预期的单词或短语。

## 配置文件存储

- 配置文件的根目录默认为`%LOCALAPPDATA%\AutoStudy\browser`。
- 当在非工作区环境中使用Chrome浏览器执行此功能时，将配置文件保存在当前激活的配置文件目录下，并重复使用相同的网站配置文件。

## 特定环境说明

- 对于Windows原生环境，请参阅`references/runtime-windows.md`。
- 对于通过WSL运行Windows Chrome的环境，请参阅`references/runtime-wsl.md`。

## 浏览器相关说明

- 请参阅`references/browser.md`。

## 平台特定说明

- 对于Xuexitong平台，请参阅`references/xuexitong.md`。
- 对于Yuketang平台，请参阅`references/yuketang.md`。
- 对于Pintia平台，请参阅`references/pintia.md`。

## 先决条件

- **Google Chrome**（Windows版本）
- [Agent Browser CLI](https://github.com/vercel-labs/agent-browser)
- [Agent Browser Skill](https://clawhub.ai/MaTriXy/agent-browser-clawdbot)