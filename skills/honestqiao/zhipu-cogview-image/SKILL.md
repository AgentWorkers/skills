---
name: zhipu-image
description: 使用 Zhipu AI 的 CogView 模型生成图像
allowed-tools: Bash(curl:*) Bash(jq:*)
env:
  - ZHIPU_API_KEY
---
# Zhipu 图像生成

使用 Zhipu AI 的 CogView 模型生成图像。

## ⚠️ 安全要求

**使用此功能之前，需要设置 `ZHIPU_API_KEY` 环境变量。**

### 安全最佳实践：

1. **切勿将 API 密钥存储在 ~/.bashrc 文件中**——这可能导致密钥泄露。
2. **不要导入 shell 配置文件**——这样可以防止任意代码的执行。
3. **在运行脚本时直接设置环境变量**。

## 设置

```bash
export ZHIPU_API_KEY="your_api_key"
```

**从以下链接获取您的 API 密钥：** https://www.bigmodel.cn/usercenter/proj-mgmt/apikeys

## 使用方法

### 快速示例

```bash
export ZHIPU_API_KEY="your_key"

curl -s -X POST "https://open.bigmodel.cn/api/paas/v4/images/generations" \
  -H "Authorization: Bearer $ZHIPU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "cogview-4", "prompt": "your description"}'
```

### 使用脚本

```bash
export ZHIPU_API_KEY="your_key"
./generate.sh "A beautiful Chinese girl in white dress"
```

## 安全分析

### ✅ 安全措施：
- **不导入 ~/.bashrc 或 shell 配置文件**。
- **使用 jq 进行 JSON 转义**（防止注入攻击）。
- **使用支持 TLS 1.2+ 的 HTTPS 协议**。
- **API 密钥通过环境变量传递（而非硬编码）**。
- **对输入进行验证**（限制输入长度）。
- **显示通用错误信息**。

### ⚠️ 需要注意的事项：
- **进程列表可见性**：API 密钥会在 `ps aux` 命令的输出中显示。
- **仅在生产环境中使用此功能**。

## 安全特性

| 特性 | 实现方式 |
|---------|----------------|
| JSON 转义 | 使用 jq 进行 JSON 转义，防止注入攻击。 |
| 输入验证 | 输入长度限制为 1000 个字符。 |
| TLS 协议 | 强制使用 TLS 1.2+ 协议。 |
| 超时设置 | 使用 curl 命令设置 60 秒的超时时间。 |
| 错误处理 | 仅显示通用错误信息。 |

## 模型

使用 Zhipu AI 的 **CogView-4** 模型。

## API 端点

**官方地址：** `https://open.bigmodel.cn/api/paas/v4/images/generations`