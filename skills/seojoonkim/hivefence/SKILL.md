---
name: hivefence
version: 1.0.0
description: 针对AI代理的集体免疫网络：当一个代理检测到提示注入攻击时，所有连接的代理都会获得免疫能力。该系统具备实时模式检测、社区投票以及分布式威胁情报功能，是基于Prompt-Guard技术构建的。
---

# HiveFence v1.0.0

🐝 **当其中一个受到攻击时，所有代理都会获得免疫力。**

这是一个为AI代理设计的集体防御网络，能够共同抵御攻击。

## 什么是HiveFence？

HiveFence在“prompt-guard”的基础上，增加了一个分布式免疫系统：
1. **检测** — 代理会扫描传入的提示信息，检查其是否符合15种以上的攻击模式。
2. **报告** — 新发现的攻击模式会被哈希处理后提交到网络中。
3. **免疫** — 社区成员会对这些攻击模式进行验证，随后所有连接的代理都会收到更新。

## 主要特性：
- 🔍 **实时检测** — 在50毫秒内完成模式匹配和语义分析。
- 🌍 **多语言支持** — 支持英语（EN）、韩语（KO）、日语（JA）和中文（ZH）的攻击检测。
- 🗳️ **社区治理** — 新攻击模式的决策通过民主投票来确定。
- 🔐 **保护隐私** — 仅共享攻击模式的SHA-256哈希值，不泄露原始内容。
- 📊 **风险评分** — 根据风险程度对攻击模式进行优先级排序（0-100）。
- ⚡ **分布式部署** — 使用Cloudflare Workers在300多个地点提供服务。

## 安装说明
```bash
# Via ClawdHub
npx clawhub install hivefence

# Or via npm
npm install hivefence
```

## 快速入门
```javascript
import { protect, reportThreat } from 'hivefence'

// Scan incoming prompt
const result = await protect(userInput)

if (result.blocked) {
  console.log(`Threat blocked: ${result.category}`)
  // Pattern automatically reported to network
}
```

## 安全性建议

为了获得最佳的保护效果，请结合使用以下组件：
1. **ACIP** — 高级认知免疫提示系统（用于设置行为边界）。
2. **HiveFence** — 负责攻击模式的检测和集体免疫功能。
3. **SkillGuard** — 在安装前对代理的技能进行审计。

（推荐方案来自[@VittoStack的安全指南](https://x.com/vittostack/status/2018326025373900881)，浏览量超过3.4万次。）

## API接口

| 方法 | 接口地址 | 描述 |
|--------|----------|-------------|
| POST | `/api/v1/threats/report` | 提交新的攻击模式信息。 |
| GET | `/api/v1/threats/pending` | 获取正在等待投票的攻击模式列表。 |
| POST | `/api/v1/threats/:id/vote` | 对特定攻击模式进行投票。 |
| GET | `/api/v1/threats/latest` | 获取已批准的攻击模式列表。 |
| GET | `/api/v1/stats` | 查看网络统计信息。 |

**基础URL：** https://hivefence-api.seojoon-kim.workers.dev

## 为什么选择HiveFence？

**未使用HiveFence时的情况：**
- 注入攻击的成功率高达91%。
- 数据提取的成功率高达84%。
- 系统提示信息可能在攻击的第一轮就被泄露。

（来源：[ZeroLeaks安全评估](https://x.com/NotLucknite/status/2017665998514475350)）

**使用HiveFence后的效果：**
- 实时阻止攻击模式。
- 通过集体防御机制提高系统安全性。
- 所有攻击模式都经过社区验证，误报率为零。

## 相关链接：
- **官方网站：** https://hivefence.com
- **GitHub仓库：** https://github.com/seojoonkim/hivefence
- **API文档：** https://hivefence.com/docs

## 许可证

MIT © 2026 Simon Kim (@seojoonkim)