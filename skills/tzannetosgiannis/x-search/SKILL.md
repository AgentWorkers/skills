---
name: x-search
description: 这款由人工智能驱动的 X/Twitter 搜索工具可帮助用户实时查找热门趋势、突发新闻、分析用户情感，并提供社交媒体洞察。当用户需要搜索 Twitter 或 X 上的主题、标签、热门内容或公众观点时，可使用该工具。通过 Base 网络上的 x402 协议，每次请求的费用仅为 0.05 美元（USDC）。
---

# X 搜索

使用基于人工智能的代理在 X/Twitter 上进行搜索，以获取实时洞察和社交媒体情报。

## 配置

私钥必须通过以下方式之一获取：

**选项 1：环境变量**
```bash
export X402_PRIVATE_KEY="0x..."
```

**选项 2：配置文件（推荐）**

脚本会按以下顺序查找 `x402-config.json` 文件：
1. 当前目录：`./x402-config.json`
2. 主目录：`~/.x402-config.json` ← **推荐**
3. 工作目录：`$PWD/x402-config.json`

创建配置文件：
```json
{
  "private_key": "0x1234567890abcdef..."
}
```

**示例（主目录 - 适用于任何用户）：**
```bash
echo '{"private_key": "0x..."}' > ~/.x402-config.json
```

## 使用方法

使用查询语句运行搜索脚本：
```bash
scripts/search.sh "<search query>"
```

脚本会执行带有支付处理的 `npx CLI` 工具：
- 每个请求的费用为 0.05 美元（Base 网络）
- 返回经过人工智能处理的搜索结果

## 示例

**用户：**“人们在 Twitter 上对 AI 代理有什么评价？”
```bash
scripts/search.sh "AI agents discussions and opinions"
```

**用户：**“查找关于加密货币的热门话题”
```bash
scripts/search.sh "cryptocurrency trends today"
```

**用户：**“显示关于气候变化的病毒式内容”
```bash
scripts/search.sh "viral climate change posts"
```

## 功能
- 实时趋势和突发新闻
- 社交媒体情感分析
- 病毒式内容追踪
- 公众意见研究
- 标签和话题分析

## 错误处理
- **“支付失败：USDC 不足”** → 通知用户向 Base 钱包充值 USDC
- **“X402 私钥缺失”** → 指导用户配置私钥（参见上述配置）
- **超时错误** → API 有 5 分钟的超时限制；复杂查询可能需要更多时间