---
name: knowfun
description: 使用 Knowfun.io API 生成教育内容——利用人工智能创建课程、海报、游戏和影片。当用户需要生成教育资源、视觉材料或交互式体验时，可以参考此方法。
argument-hint: "<command> [args]"
disable-model-invocation: false
user-invocable: true
allowed-tools: "Bash(curl *), Read, Write"
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "bins": ["knowfun"], "env": ["KNOWFUN_API_KEY"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": ".",
              "bins": ["knowfun"],
              "label": "Build knowfun skills (npm)",
            },
          ],
      },
  }
---
# Knowfun.io API 技能

该技能可帮助您与 Knowfun.io 的 OpenAPI 进行交互，以生成教育内容、海报、游戏和电影。

## 先决条件

在使用此技能之前，您需要：
1. 一个 Knowfun.io API 密钥（请从 https://www.knowfun.io/api-platform 获取）
2. 账户中有足够的信用点数

## 配置

将您的 API 密钥设置为环境变量：
```bash
export KNOWFUN_API_KEY="kf_your_api_key_here"
```

否则，该技能会在需要时提示您输入密钥。

## 可用命令

调用此技能时，支持以下操作：

### 1. 创建任务

通过创建任务来生成内容。支持四种类型：`course`（课程）、`poster`（海报）、`game`（游戏）、`film`（电影）。

**基本示例：**
```bash
/knowfun create course "Introduction to Machine Learning"
/knowfun create poster "Climate Change Facts"
/knowfun create game "Learn Python Basics"
/knowfun create film "History of the Internet"
```

**使用 URL：**
```bash
/knowfun create course https://example.com/document.pdf
```

### 2. 查查任务状态

通过任务 ID 查查任务的状态：
```bash
/knowfun status <taskId>
```

### 3. 获取任务详情

获取已完成任务的详细信息：
```bash
/knowfun detail <taskId>
```

### 4. 列出任务

列出最近的任务：
```bash
/knowfun list
```

### 5. 查看信用点数

查看您的信用点数余额：
```bash
/knowfun credits
```

### 6. 获取配置选项

获取每种任务类型的可用配置选项：
```bash
/knowfun schema
```

## 任务配置

每种任务类型都有特定的配置选项。详情请参阅 [api-reference.md](api-reference.md)。

### 课程配置
- **contentStyle**：详细、简洁、对话式
- **contentLanguage**：中文、英文等
- **explainLanguage**：中文、英文等
- **voiceType**：标准语音选项
- **ttsStyle**：课堂式、专业式等

### 海报配置
- **usage**：信息图（默认）、商业报告、营销、插图
- **style**：手绘（默认）、写实、动漫、科幻、自定义
- **aspectRatio**：1:1、16:9、9:16 等
- **posterTitle**：海报的自定义标题

### 游戏配置
- **gameType**：故事类、互动类（默认）、探索类、任务类、角色扮演类、模拟类、谜题类、街机类、卡片类、文字类、时间线类、自定义
- **customPrompt**：自定义游戏描述

### 电影配置
- **filmStyle**：旁白（默认）、故事类、纪录片、教程类、概念讲解类、案例研究类、动画类、电影类、宣传类、自定义
- **aspectRatio**：16:9（默认）、9:16、1:1
- **visualStyle**：自定义视觉风格描述

## 此技能的工作原理

1. **提取 API 密钥**：首先检查 KNOWFUN_API_KEY 环境变量是否已设置
2. **解析命令**：解读命令（创建、状态、列表、信用点数、配置选项）
3. **发送 API 请求**：使用 curl 与 Knowfun.io API 进行交互
4. **格式化响应**：以可读的格式呈现结果
5. **处理错误**：提供有用的错误信息和故障排除提示

## API 端点

该技能使用以下基础 URL：
- 生产服务：`https://api.knowfun.io`

## 示例

请参阅 [examples.md](examples.md) 以获取全面的用法示例。

## 错误处理

常见错误及解决方法：
- **401 未经授权**：检查您的 API 密钥是否正确且未过期
- **402 信用点数不足**：请在 https://knowfun.io 充值
- **429 速率限制**：稍后再试
- **400 错误请求**：检查您的输入参数

## 参考文档

有关完整的 API 文档，请参阅 [api-reference.md](api-reference.md)。

## 实现细节

当调用此技能时，Claude 会：
1. 验证 API 密钥是否可用
2. 从 `$ARGUMENTS` 中解析命令和参数
3. 构建适当的 curl 命令以调用 Knowfun.io API
4. 处理认证头部信息
5. 解析 JSON 响应
6. 格式化结果显示结果
7. 提供下一步的操作建议

该技能使用 `curl` 发送 API 请求，并在可用时使用 `jq` 进行 JSON 解析。