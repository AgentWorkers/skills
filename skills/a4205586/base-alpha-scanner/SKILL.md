---
name: base-alpha-scanner
description: "**ZHAO（CryptoZhaoX）的实时Base链智能分析工具**  
该工具适用于以下场景：  
- 扫描Base系列MEME代币，以寻找第二波投资机会或早期优质代币的发布；  
- 监控GMGN智能资金流动情况；  
- 分析Base代币的持有者分布；  
- 检查Clanker或Bankr.fun等平台上的高质量叙事代币项目；  
- 监控VIRTUAL Protocol的AI代理程序的发布情况；  
- 在Base链上运行AI叙事分析工具；  
- 生成关于Base系列MEME代币或主流资产（BTC/ETH/UNI）的交易提醒；  
- 执行任何与Base链相关的链上分析任务。"
---
# Base Alpha Scanner

这是赵（ZHAO）为 Base 链开发的链上智能工具包。该工具以数据为核心，不追求炒作，仅在高置信度的情况下发出警报。

## 脚本

### scan_base.py — 核心链上扫描脚本
```
python3 skills/base-alpha-scanner/scripts/scan_base.py --mode <mode> [addr]
```
可用模式：
- `trending`：根据置信度得分（1小时）对 Base 链上的热门代币进行排名
- `new`：新上线代币的扫描：0–45分钟和45分钟–3小时的时间段
- `token <addr>`：对特定代币进行深入分析（所有时间范围）
- `holders <addr>`：检查代币持有者的分布情况
- `gmgn <addr>`：查询 GMGN 智能资金的数据（可能需要使用浏览器）

### scan_narrative.py — 故事分析与平台扫描脚本
```
python3 skills/base-alpha-scanner/scripts/scan_narrative.py --mode <mode>
```
可用模式：
- `clanker`：查询 Base 链上最新的 Clanker 代币部署情况
- `bankr`：Farcaster 平台上热门的代币
- `virtual`：虚拟协议（VIRTUAL Protocol）的 AI 代理生态系统
- `ai`：对 Base 链上的 AI 相关内容进行全面扫描

## 工作流程

### 标准市场扫描（按需运行或每 1–2 小时运行）：
1. `scan_base.py --mode trending`：识别市场热点
2. 对于置信度得分 ≥ 60 的代币：`scan_base.py --mode token <addr>` 进行深入分析
3. 如果有 AI 分析结果或 Farcaster 的提示：`scan_narrative.py --mode ai` + `clanker`
4. 应用警报规则；只有在满足条件时才向 ZHAO 发送警报

### 新上线代币扫描（持续后台运行）：
1. `scan_base.py --mode new`：检查 0–45 分钟的时间段
2. 如果置信度得分 ≥ 60 且信号正常：立即使用 `token` 模式进行深入分析
3. 与 `scan_narrative.py --mode clanker` 结合使用，确认代币的来源（Farcaster）
4. 如果所有检查都通过：立即发出警报

### 持有者分布检查：
1. `scan_base.py --mode holders <addr>`
2. 如果前 5 大持有者占总供应量的 40% 以上，或任何单个钱包的持有量超过 15%，则发出警报
3. 与 DexScreener 的买卖数据交叉验证，以确认持有者的真实分布情况

## 警报规则

详细规则请参阅 `references/alert-rules.md`。总结如下：
- **立即警报**：仅适用于一级代币（成交量激增、有明确的市场趋势、流动性良好且市值超过 10 万美元）
- **第二波警报**：成立 45 分钟至 3 小时内的代币，成交量持续上升且持有者数量增加，置信度得分 ≥ 65
- **新上市代币**：成立时间小于 45 分钟，置信度得分 ≥ 60，团队背景良好且具有实际市场动力。每天最多发出 2–3 次警报
- **主流代币（BTC/ETH/UNI）**：关键价格突破、链上资金流动异常等情况

## API 参考

所有 API 端点、字段名称和数据来源的详细信息请参阅 `references/api-endpoints.md`。

**关键地址**：
- VIRTUAL 代币（Base 链）：`0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b`
- cbBTC（Base 链）：`0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf`

## 置信度得分（0–100）

该得分机制内置于 `scan_base.py` 中。置信度得分 ≥ 65 的代币被视为潜在的警报对象；得分 < 50 的代币将被忽略。
评估因素包括：1 小时的成交量、流动性、买入压力比、代币的活跃时间（45分钟–3小时为活跃期）、市场动力以及代币的总市值（MCAP）。

## 关于 GMGN 的注意事项

GMGN 通常会限制直接通过 API 访问其数据。备用方法如下：
1. 使用 `browser` 工具访问 `https://gmgn.ai/base/token/<addr>`
2. 如有需要，可截取网页截图并发送给 ZHAO
3. 在 `https://gmgn.ai/base/address/<wallet>` 查看钱包的交易记录

## 关于 Bankr 的注意事项

Bankr 没有公开的 API。其相关信息可通过 Warpcast 获取：
- 频道：`https://warpcast.com/~/channel/bankr`
- 使用 `web_search` 查找 Bankr 的最新提及内容，或使用 `web_fetch` 功能查看 Warpcast 上的相关内容
- 强烈信号：当拥有超过 5,000 名关注者的用户在使用 Bankr 功能进行交易时（在平台上线后的 30 分钟内）