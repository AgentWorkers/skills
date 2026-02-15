---
name: handling-commands
description: 在 XMTP 代理中处理命令、验证输入以及过滤消息的模式。这些模式可用于实现斜杠命令（slash commands）、输入验证器（input validators）或消息过滤器（message filters）。它们会在命令处理、输入验证或类型检查（type guards）的环节被触发。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# XMTP命令与验证

处理命令、验证输入以及过滤消息的最佳实践。

## 适用场景

在以下情况下请参考这些指南：
- 实现斜杠命令（slash commands）
- 验证十六进制字符串和地址
- 过滤消息类型
- 使用类型防护（type guards）代替类型断言（type assertions）

## 规则类别（按优先级排序）

| 优先级 | 类别 | 影响程度 | 前缀 |
|----------|----------|--------|--------|
| 1 | 验证器（Validators） | 关键性（CRITICAL） | `validators-` |
| 2 | 过滤器（Filters） | 高优先级（HIGH） | `filters-` |
| 3 | 类型防护（Type Guards） | 高优先级（HIGH） | `guards-` |

## 快速参考

### 验证器（Critical）

- `validators-hex`：使用`validHex()`函数验证十六进制字符串
- `validators-address`：验证以太坊地址

### 过滤器（High Priority）

- `filters-message-types`：按消息类型进行过滤
- `filters-sender`：过滤掉来自发送者的消息
- `filters-content`：检查消息内容是否符合预设要求

### 类型防护（High Priority）

- `guards-codec`：使用`usesCodec()`函数代替类型断言
- `guards-content-type`：利用类型防护机制确保代码的安全性

## 使用方法

有关详细说明，请阅读相应的规则文件：

```
rules/validators-hex.md
rules/filters-message-types.md
rules/guards-codec.md
```