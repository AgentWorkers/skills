---
name: cashu-emoji
description: 使用 Unicode 变体选择器（Unicode Variation Selectors）对隐藏在表情符号（emoji）内部的 Cashu 令牌进行编码和解码。
metadata:
  openclaw:
    emoji: "🥜"
    examples:
      - "Decode an emoji token from a full chat message"
      - "Encode a Cashu token into an emoji for sending"
---
# Cashu表情符号令牌（变体选择器编码）

该技能帮助代理**解码**以表情符号形式接收的Cashu令牌，并**编码**用于发送的令牌；同时支持在表情符号中嵌入**普通隐藏信息**。

如果解码后的文本以`cashu`开头，那么它很可能是Cashu令牌；否则应将其视为普通隐藏信息。

## 为何需要这个功能

某些服务使用Unicode变体选择器（VS1..VS256）将`cashu...`令牌嵌入到表情符号中。聊天应用通常只显示表情符号，但会保留隐藏的选择器字符。

**重要提示**：许多通讯工具可能会截断或规范化Unicode数据。如果变体选择器丢失，嵌入的令牌将无法被恢复。

## 快速入门（复制/粘贴）

```bash
git clone https://github.com/robwoodgate/cashu-emoji.git
cd cashu-emoji
npm ci

# decode a whole message (recommended)
node ./bin/cashu-emoji.js decode "<paste message>"

# decode and print mint/unit/amount if it’s a cashu token
node ./bin/cashu-emoji.js decode "<paste message>" --metadata

# decode as structured JSON (agent-friendly)
node ./bin/cashu-emoji.js decode "<paste message>" --metadata --json

# encode a hidden message
node ./bin/cashu-emoji.js encode "🥜" "hello from inside an emoji"

# encode a cashu token
node ./bin/cashu-emoji.js encode "🥜" "cashuB..."
```

## 功能介绍

### 1) 解码

- 输入：完整消息文本（可能包含其他文本/表情符号）
- 输出：嵌入的UTF-8文本，通常是`cashuA...`/`cashuB...`令牌

```bash
node ./bin/cashu-emoji.js decode "<paste entire message>"
```

**解码说明**：解码器会忽略普通字符，直到找到第一个变体选择器字节，然后收集后续字节，直到遇到该数据包之后的第一个普通字符。

### 2) 编码

- 输入：一个载体表情符号（推荐使用`🥜`）和令牌字符串
- 输出：一个外观与原始表情符号相同，但实际上包含隐藏令牌的表情符号字符串

```bash
node ./bin/cashu-emoji.js encode "🥜" "cashuB..."
```

**提示**：如果表情符号后面有任何普通文本（哪怕只有一个字符），某些通讯工具更有可能完整地传递该令牌。这不是强制要求，但可以提高传递的可靠性。

**Telegram提示**：将令牌以代码块或“等宽”格式发送，有助于保留隐藏字符，便于用户通过点击复制。

## 可选元数据

为了在不兑换令牌的情况下验证其有效性，可以请求元数据。

**编程/代理使用建议**：优先选择JSON格式的输出：

```bash
node ./bin/cashu-emoji.js decode "<message>" --metadata --json
```

**示例JSON响应（Cashu令牌）：**

```json
{
  "text": "cashuB...",
  "isCashu": true,
  "metadata": {
    "mint": "https://mint.example",
    "unit": "sat",
    "amount": 21
  },
  "metadataError": null
}
```

**示例JSON响应（普通隐藏信息）：**

```json
{
  "text": "hello from inside an emoji",
  "isCashu": false
}
```

**示例JSON响应（包含元数据）：**

```bash
node ./bin/cashu-emoji.js decode "<message>" --metadata
```

该示例使用`@cashu/cashu-ts`和`getTokenMetadata()`方法打印出令牌的铸造数量/单位/金额（不涉及铸造操作）。

## 新代理需要注意的事项

- 解码后的`cashu...`令牌是一种**载体资产**，应将其视作现金处理。
- `--metadata`选项仅用于本地解析，无法证明令牌是否未被使用或有效。
- 如果解码结果不完整或无意义，很可能是因为通讯工具损坏了变体选择器；此时应要求重新发送令牌（通常令牌后面会附带一些普通文本）。

## 相关文件

- `src/emoji-encoder.ts`：核心编码/解码逻辑
- `bin/cashu-emoji.js`：命令行工具封装
- `examples/`：测试用例

## 安全性说明

该工具仅用于文本的编码/解码，不会涉及任何资金操作。