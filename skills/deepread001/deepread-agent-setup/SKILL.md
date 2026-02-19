---
name: deepread-agent-setup
title: DeepRead OCR — Agent Self-Signup
description: 适用于生产环境的OCR系统的零摩擦式代理注册流程：您的AI代理可通过设备授权在几秒钟内获得自己的API密钥——无需使用任何控制面板，也无需进行复制/粘贴操作。该系统采用多模型共识机制，并结合人工审核，准确率超过97%。每月可免费处理2,000页文档。
disable-model-invocation: true
metadata:
  {"openclaw":{"homepage":"https://www.deepread.tech"}}
---
# **DeepRead OCR — 无障碍的自动化文档处理方案**

DeepRead 是一个基于人工智能的 OCR（光学字符识别）平台，能够将文档高效地转换为高精度的数据。您的代理账户会自动获得专属的 API 密钥，无需使用任何控制面板或进行手动复制/粘贴操作。

通过多步骤处理流程（PDF → 转换 → 旋转/校正 → OCR → 多模型验证 → 数据提取），DeepRead 的识别准确率可达到 97% 以上，并仅将不确定的字段标记出来，供人工审核——从而将手动工作量从 100% 降低到 5-10%。整个过程完全不需要人工干预。

## **核心功能**

- **代理自动注册**：您的代理账户会通过设备授权（RFC 8628 标准）自动获得 API 密钥，您只需点击“批准”即可。
- **文本提取**：将 PDF 和图片文件转换为结构化的 Markdown 格式。
- **结构化数据**：提取带有置信度评分的 JSON 数据。
- **标记不确定字段**：系统会自动标记不确定的字段（标记为 `hil_flag`），仅需要人工审核这些异常情况。
- **多模型验证**：通过多个模型进行交叉验证，确保结果的可靠性。
- **优化后的数据模型**：提供可复用的数据模型，识别准确率提升 20-30%。
- **免费 tier**：每月支持处理 2,000 页文档，无需使用信用卡。

## **代理自动注册流程**

您的代理账户会自动获得专属的 API 密钥。无需使用控制面板或进行手动操作，只需在浏览器中点击“批准”即可。该流程使用安全的设备授权机制（RFC 8628 标准），与 GitHub CLI、Slack 和 VS Code 的授权方式相同。

**注册步骤：**

1. 代理请求设备代码（无需身份验证）：
   ```bash
curl -X POST https://api.deepread.tech/v1/agent/device/code \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "My Agent"}'
```

2. 系统回复设备代码：
   ```json
{
  "device_code": "a7f3c9d2e1b8...",
  "user_code": "HXKP-3MNV",
  "verification_uri": "https://www.deepread.tech/activate",
  "verification_uri_complete": "https://www.deepread.tech/activate?code=HXKP-3MNV",
  "expires_in": 900,
  "interval": 5
}
```

3. 代理在浏览器中打开 `verification_uri_complete` 链接，登录（或免费注册），查看代理名称后点击“批准”。
4. 代理每隔 5 秒自动请求 API 密钥：
   ```bash
curl -X POST https://api.deepread.tech/v1/agent/device/token \
  -H "Content-Type: application/json" \
  -d '{"device_code": "a7f3c9d2e1b8..."}'
```

| 错误代码 | API 密钥 | 含义 |
| -------- | -------- | -------- |
| `authorization_pending` | `null` | 用户尚未批准请求 | 继续等待批准 |
| `null` | `"sk_live_..."` | 用户已批准请求 | 保存 API 密钥 |
| `access_denied` | `null` | 用户被拒绝访问 | 停止请求 |
| `"expired_token"` | `null` | 密钥已过期（15 分钟） | 重新请求 |

5. 代理保存 API 密钥后，即可开始处理文档。

## **手动注册方式（备用方案）**

如果您希望跳过自动注册流程，也可以通过控制面板手动获取 API 密钥：

```bash
# 1. Get your key at https://www.deepread.tech/dashboard/?utm_source=clawdhub
# 2. Set it
export DEEPREAD_API_KEY="sk_live_your_key_here"
```

## **支持的平台**

DeepRead 的功能支持所有主流的 AI 开发工具。安装完成后，可以使用以下命令进行配置：
- **Claude Code**：`npx skills add deepread-tech/skills`  
- **Cursor**：从 [skills repo](https://github.com/deepread-tech/skills) 复制 `.cursor/rules/` 文件  
- **Windsurf**：从 [skills repo](https://github.com/deepread-tech/skills) 复制 `.windsurf/rules/` 文件  
- **ClawHub**：`clawhub add DeepRead001/deepread-agent-setup`  
- **MCP 代理**：直接使用平台提供的设备授权接口  

## **快速示例**

获取 API 密钥后（无论是通过自动注册还是手动方式），您可以立即开始处理文档：

```bash
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@invoice.pdf" \
  -F 'schema={
    "type": "object",
    "properties": {
      "vendor": {"type": "string", "description": "Vendor name"},
      "total": {"type": "number", "description": "Total amount"},
      "date": {"type": "string", "description": "Invoice date"}
    }
  }'
```

处理过程是异步的（通常需要 2-5 分钟），系统会立即生成任务 ID（```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued"
}
```）。您可以通过 Webhook 或 `GET /v1/jobs/{id}` 获取处理结果。最终响应格式如下：
- `hil_flag: false`：数据提取准确，可自动处理。
- `hil_flag: true`：数据提取存在不确定性，需要人工审核（通常仅占 5-10% 的字段）。

## **API 接口说明**

| 接口地址 | 功能说明 |
| -------- | -------- |
| `POST /v1/agent/device/code` | 启动代理自动注册流程 |
| `POST /v1/agent/device/token` | 请求 API 密钥 |
| `POST /v1/process` | 处理 PDF、JPG 或 PNG 格式的文档 |
| `GET /v1/jobs/{id}` | 查看任务状态 |
| `GET /v1/blueprints` | 查看优化后的数据模型 |
| `POST /v1/optimize` | 创建新的数据模型 |
| `GET /v1/preview/{token}` | 提供公开预览链接（无需身份验证） |

基础 API 地址：`https://api.deepread.tech`

身份验证方式：在请求头中添加 `X-API-Key: sk_live_...`。

如需完整的 API 文档（包含所有示例、Webhook 配置、数据模型模板及最佳实践），请访问：[deepread-ocr](https://clawhub.ai/DeepRead001/deepread-ocr)

## **定价方案**

| 订阅 tier | 每月处理页数 | 请求限制 | 价格 |
| -------- | -------- | -------- | -------- |
| 免费 | 2,000 页 | 每分钟 10 次请求 | 免费 |
| Pro | 50,000 页 | 每分钟 100 次请求 | 99 美元/月 |
| 自定义 tier | 根据需求定制 | 根据需求定制 | [联系我们](mailto:hello@deepread.tech) |

## **相关链接**

- **技能库**：[https://github.com/deepread-tech/skills]  
- **控制面板**：[https://www.deepread.tech/dashboard]  
- **文档说明**：[https://www.deepread.tech/docs]  
- **完整 API 文档**：[https://clawhub.ai/DeepRead001/deepread-ocr]  
- **问题反馈**：[https://github.com/deepread-tech/deep-read-service/issues]  
- **联系我们**：[hello@deepread.tech]

准备好开始使用了吗？只需运行 `/setup` 命令，其余工作将由 DeepRead 代理为您完成。