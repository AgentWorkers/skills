---
name: regex-writer
description: 根据用户提供的英文描述生成正则表达式模式。这种方法适用于用户在不熟悉正则表达式语法的情况下，仍能够快速创建所需的正则表达式。
---

# 正则表达式生成器（Regex Writer）

将普通的英文描述转换为可执行的正则表达式模式。请详细说明您想要匹配的内容，并提供经过测试的正则表达式模式，同时附上解释和示例。

## 使用方法

```bash
npx ai-regex "your description here"
```

## 示例

```bash
# Match email addresses
npx ai-regex "match valid email addresses"

# Extract phone numbers
npx ai-regex "US phone numbers with optional country code"

# Get JSON output
npx ai-regex --json "URLs starting with https"
```

## 注意事项：
- 该项目为免费、开源软件，采用 MIT 许可协议。
- 由 LXGIC Studios 开发。
- 项目托管在 GitHub 上：https://github.com/LXGIC-Studios/ai-regex