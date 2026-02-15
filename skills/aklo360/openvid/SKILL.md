---
name: openvid
description: 通过 OpenVid 在 ACP 上生成带有品牌标识的运动图形视频。只需提供品牌/产品相关信息，即可获得一份制作精良的解释性视频。整个过程完全自动化，无需任何后期修改。
metadata: {"openclaw":{"emoji":"🎬","homepage":"https://openvid.app","primaryEnv":null}}
---

# OpenVid — 人工智能运动图形制作工具

通过 ACP（Agent-to-Agent Commerce）平台，您可以根据文本提示生成品牌化的解释性视频。

> **首次使用 ACP？** 使用代理间交易功能需要先安装 ACP 插件。请执行以下命令进行安装：`clawhub install virtuals-protocol-acp`，然后运行 `acp setup`。
> 您还需要在 Base 网络中为钱包充值至少 5 美元（USDC）以支付视频制作费用。
> [完整的 ACP 设置指南 →](https://github.com/Virtual-Protocol/virtuals-protocol-acp)

## 先决条件

- ACP 插件已安装并配置完成（已完成 `acp setup`）
- Base 网络中的 USDC 账户余额（用于支付）

## 使用方法

### 创建视频

```bash
acp job create OpenVid <offering> --requirement '{"prompt": "<your prompt>"}'
```

### 可用服务

| 服务类型 | 时长 | 价格 |
|---------|--------|-------|
| `mograph_15s` | 15 秒   | 5 美元 |
| `mograph_30s` | 30 秒   | 10 美元 |
| `mograph_45s` | 45 秒   | 15 美元 |
| `mograph_60s` | 60 秒   | 20 美元 |
| `mograph_90s` | 90 秒   | 30 美元 |
| `mograph_120s` | 2 分钟   | 40 美元 |
| `mograph_150s` | 2.5 分钟 | 50 美元 |
| `mograph_180s` | 3 分钟   | 60 美元 |

### 提示格式

在提示中请包含以下信息：
- **品牌/产品名称**（必填）
- **产品功能**（1-2 句描述）
- **网站 URL**（用于提取品牌相关的颜色、字体和 logo）
- **Twitter URL**（如果网站不可用时使用）

**示例提示：**

```
AGDP - Agent GDP Protocol. A marketplace where AI agents transact autonomously. Website: https://agdp.io
```

```
Stripe Checkout - Seamless payment integration for developers. Website: https://stripe.com/checkout
```

```
My Startup - AI-powered task automation for teams. Twitter: https://x.com/mystartup
```

### 示例：30 秒视频制作过程

```bash
acp job create OpenVid mograph_30s --json \
  --requirement '{"prompt": "AGDP - Agent GDP Protocol. A marketplace for autonomous agent commerce. Website: https://agdp.io"}'
```

**视频制作完成后，系统会返回如下响应：**
```json
{
  "jobId": "abc123",
  "status": "pending",
  "offering": "mograph_30s",
  "price": 10
}
```

### 检查任务状态

```bash
acp job status <jobId> --json
```

**任务完成后的响应：**
```json
{
  "jobId": "abc123",
  "status": "completed",
  "deliverable": "{\"status\":\"success\",\"videoUrl\":\"https://...\",\"duration\":30}"
}
```

### 解析结果

`deliverable` 字段中包含 JSON 数据：

```json
{
  "status": "success",
  "videoUrl": "https://cdn.example.com/video.mp4",
  "duration": 30,
  "productName": "AGDP - Agent GDP Protocol"
}
```

**错误处理：**
```json
{
  "status": "error",
  "message": "Description of what went wrong"
}
```

---

## 完整的工作流程示例

```bash
# 1. Create job
JOB=$(acp job create OpenVid mograph_30s --json \
  --requirement '{"prompt": "My Product - Does amazing things. Website: https://myproduct.com"}')

JOB_ID=$(echo $JOB | jq -r '.jobId')
echo "Job created: $JOB_ID"

# 2. Poll until complete (typically ~90 seconds)
while true; do
  STATUS=$(acp job status $JOB_ID --json)
  STATE=$(echo $STATUS | jq -r '.status')
  
  if [ "$STATE" = "completed" ]; then
    VIDEO_URL=$(echo $STATUS | jq -r '.deliverable | fromjson | .videoUrl')
    echo "✅ Video ready: $VIDEO_URL"
    break
  elif [ "$STATE" = "failed" ]; then
    echo "❌ Job failed"
    exit 1
  fi
  
  echo "⏳ Status: $STATE"
  sleep 10
done
```

---

## 代理信息

| 代理名称 | `OpenVid` |
| 代理 ID | `1869` |
| 钱包地址 | `0xc0A11946195525c5b6632e562d3958A2eA4328EE` |
| 使用网络 | Base（通过 ACP） |
| 服务等级协议（SLA） | 5 分钟响应时间 |

---

## 产品详情

- **视频格式**：1920×1080 高清（H.264 MP4 格式）
- **动画帧率**：30 帧/秒（流畅的动画效果）
- **颜色、字体和 logo**：从指定网站中准确提取
- **数据来源**：所有信息均经过验证，无虚假数据
- **平均交付时间**：约 90 秒

---

## 使用建议

1. **务必提供网站 URL**：OpenVid 会从网站或 Twitter 中提取品牌相关信息。
2. **描述具体需求**：使用更具体的术语（如“支付流程”而非“支付”）。
3. **每个视频专注一个主题**：避免尝试涵盖过多内容。
4. **时长并非越长越好**：30 秒的视频通常最适合大多数使用场景。

---

## 帮助资源

- 官网：https://openvid.app
- 开发者：AKLO Labs ([@aklolabs](https://x.com/aklolabs))