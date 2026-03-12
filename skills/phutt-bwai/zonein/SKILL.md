---
name: zonein
version: 2.1.0
description: 通过 Zonein API，追踪并分析在 Hyperliquid 和 Polymarket 上胜率超过 75% 的顶尖交易者。轻松创建 Hyperliquid 交易代理程序，实现自动化交易流程，同时保留人工干预的机制。
homepage: https://zonein.xyz
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3"],"env":["ZONEIN_API_KEY"]},"primaryEnv":"ZONEIN_API_KEY","files":["scripts/*"],"installer":{"instructions":"1. Go to https://app.zonein.xyz\n2. Log in with your refcode\n3. Click 'Get API Key' button\n4. Copy the key and paste it below"}}}
---
# Zonein: 用于在Hyperliquid和Polymarket上追踪交易代理的智能资金工具

该工具利用捆绑的脚本从Polymarket和HyperLiquid的智能资金钱包获取实时交易情报。

## 设置（凭据）

### 获取API密钥

1. 访问 **https://app.zonein.xyz**
2. 使用您的账户登录（需要一个推荐码进行注册）
3. 点击 **“获取API密钥”** 按钮
4. 复制您的API密钥（以 `zn_` 开头）

### 在OpenClaw中设置API密钥

**选项A — Gateway Dashboard（推荐）：**
1. 打开您的 **OpenClaw Gateway Dashboard**
2. 转到侧边栏的 **`/skills`**
3. 在工作区技能中找到 **“zonein”**，然后点击 **“启用”**
4. 输入您的 `ZONEIN_API_KEY` 并保存

**选项B — 环境变量：**
```bash
export ZONEIN_API_KEY="zn_your_key_here"
```