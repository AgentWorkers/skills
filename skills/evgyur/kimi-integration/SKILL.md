---
name: kimi-integration
description: 将 Moonshot AI (Kimi) 和 Kimi Code 模型集成到 Clawdbot 的逐步指南。适用于需要了解如何添加 Kimi 模型、配置 Moonshot AI 或在 Clawdbot 中设置 Kimi 用于编程的用户。
---

# Kimi模型集成

本文档提供了将Moonshot AI（Kimi）和Kimi Code模型添加到Clawdbot的完整指南。

## 概述

Kimi提供了两个独立的模型系列：

1. **Moonshot AI（Kimi K2）**：通过OpenAI兼容的API提供通用模型。
2. **Kimi Code**：专门用于代码生成的模型，拥有独立的API端点。

这两个模型都需要从不同来源获取API密钥。

## 先决条件

- Clawdbot已安装并配置完成。
- 已获取API密钥（请参阅“获取API密钥”部分）。

## 获取API密钥

### Moonshot AI（Kimi K2）

1. 访问 [https://platform.moonshot.cn](https://platform.moonshot.cn)。
2. 注册一个账户。
3. 转到“API密钥”部分。
4. 创建一个新的API密钥。
5. 复制密钥（密钥以 `sk-` 开头）。

### Kimi Code

1. 访问 [https://api.kimi.com/coding](https://api.kimi.com/coding)。
2. 注册一个账户。
3. 转到“API密钥”部分。
4. 创建一个新的API密钥。
5. 复制密钥（密钥以 `sk-` 开头）。

**注意：** Moonshot AI和Kimi Code使用不同的API密钥和端点。

## 集成步骤

### 选项1：Moonshot AI（Kimi K2模型）

#### 第1步：设置环境变量

（代码示例）：

或将其添加到 `.env` 文件中：

#### 第2步：添加提供者配置

编辑您的 `clawdbot.json` 配置文件：

#### 第3步：重启Clawdbot

#### 第4步：验证集成

（代码示例）：

您应该能在模型列表中看到Moonshot模型。

#### 第5步：使用模型

- 将其设置为默认模型：
（代码示例）

- 或在聊天中使用模型别名：
（代码示例）

### 选项2：Kimi Code（专门用于代码生成的模型）

#### 第1步：设置环境变量

（代码示例）：

或将其添加到 `.env` 文件中：

#### 第2步：添加提供者配置

编辑您的 `clawdbot.json` 配置文件：

#### 第3步：重启Clawdbot

#### 第4步：验证集成

（代码示例）：

您应该能在模型列表中看到 `kimicode/kimi-for-coding`。

#### 第5步：使用模型

- 将其设置为默认模型：
（代码示例）

- 或在聊天中使用模型别名：
（代码示例）

## 同时使用两种提供者

您可以同时配置Moonshot AI和Kimi Code模型：

（代码示例）：

- 使用别名在模型之间切换：
  - `/model k25` - Kimi K2.5（通用模型）
  - `/model kimi` - Kimi for Coding（专门用于代码生成的模型）

## 故障排除

### 模型未出现在列表中

- 检查配置语法是否正确。
- 验证API密钥是否已正确设置。

### 认证错误

- 确保API密钥以 `sk-` 开头。
- 在提供者控制台上验证密钥的有效性。
- 确保每个提供者的基础URL正确。

### 连接问题

直接测试API端点：

#### 模型推荐

- **Kimi K2.5** (`moonshot/kimi-k2.5`)：适用于一般任务，上下文容量为200K。
- **Kimi for Coding** (`kimicode/kimi-for-coding`)：专门用于代码生成。
- **Moonshot V1 128K** (`moonshot/moonshot-v1-128k`)：旧版本模型，上下文容量为128K。

## 参考资料

- Moonshot AI文档：[https://platform.moonshot.cn/docs](https://platform.moonshot.cn/docs)
- Kimi Code API文档：[https://api.kimi.com/coding/docs](https://api.kimi.com/coding/docs)
- Clawdbot模型提供者文档：[https://home/eyurc/clawdbot/docs/concepts/model-providers.md](https://home/eyurc/clawdbot/docs/concepts/model-providers.md)