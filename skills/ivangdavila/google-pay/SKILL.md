---
name: Google Pay
slug: google-pay
version: 1.0.0
homepage: https://clawic.com/skills/google-pay
description: 为网页和安卓应用实现 Google Pay 功能，确保安全性（包括令牌化处理）、与支付网关的兼容性，以及具备生产环境所需的完整结账流程。
changelog: Initial release with implementation, validation, launch, and incident response playbooks for Google Pay.
metadata: {"clawdbot":{"emoji":"💳","requires":{"bins":["curl","jq"],"env":["GOOGLE_PAY_MERCHANT_ID"]},"os":["darwin","linux","win32"]}}
---
## 设置

首次使用本技能时，请阅读 `setup.md` 文件，确认所使用的平台、支付服务提供商（PSP）以及目标发布版本，然后再进行任何代码修改。

## 使用场景

当用户在结账、订阅或使用钱包优先的支付流程中需要使用 Google Pay 时，可参考本文档。相关操作由技术团队负责处理，包括架构设计、令牌化方式的选择、网关集成、上线验证以及上线后的维护工作。

## 架构

所有与 Google Pay 相关的数据和配置文件都存储在 `~/google-pay/` 目录下。具体设置和状态信息请参考 `memory-template.md` 文件。

```
~/google-pay/
|-- memory.md                 # Project snapshot, risk status, and rollout state
|-- implementations.md        # Selected approach and platform notes
|-- validation-log.md         # Test evidence and environment results
`-- incidents.md              # Failed payments, root causes, and fixes
```

## 快速参考

根据当前任务的需求，选择相应的文件进行参考：

| 任务类型 | 参考文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 内存管理模板 | `memory-template.md` |
| 实施计划 | `implementation-playbook.md` |
| 验证清单 | `validation-checklist.md` |
| 故障处理 | `failure-handling.md` |
| 发布与运维 | `launch-playbook.md` |
| 定期支付与订阅流程 | `recurring-payments.md` |

## 必备条件

- 环境变量：`GOOGLE_PAY_MERCHANT_ID`
- 用于诊断的 CLI 工具：`curl`、`jq`
- 必须能够访问 Google Pay 商户控制台以及目标支付服务提供商（PSP）的账户

**注意：** 绝不要要求用户将私钥、完整的令牌数据或支付服务提供商的敏感信息通过聊天工具发送过来。

## 数据存储

所有本地配置文件和日志都存储在 `~/google-pay/` 目录下：
- `memory-file`：存储当前系统状态和集成配置信息
- `validation-log-file`：记录测试结果和验证证据
- `incidents-file`：记录故障详情及相应的处理措施

## 核心规则

### 1. 在选择集成方案前明确业务目标

首先明确您的业务目标：
- 提高移动支付的转化率
- 加快重复购买的流程
- 降低 Android 和 Chrome 用户的支付摩擦
- 减少支付失败的情况

然后选择一种主要的集成方案：
- 通过 Google Pay API 和网关进行支付（适用于 Web 应用）
- 在 Android 应用中直接使用 Google Pay API
- 通过支付服务提供商（PSP）进行集成

**注意：** 除非用户明确要求进行迁移，否则不要在同一代码版本中混合使用多种集成方案。

### 2. 确保满足环境和商户的必备条件

在开始实施之前，请确认以下条件：
- 已为生产环境创建了 Google Pay 商户账户
- 目标国家的支付服务提供商（PSP）支持 Google Pay
- 测试环境与生产环境是隔离的
- 应用程序的配置正确无误

如果缺少任何必备条件，请暂停开发并制定详细的检查清单。

### 3. 确保金额和货币信息的准确性

服务器端显示的金额和货币必须与以下数据一致：
- 客户端发送的支付请求信息
- 服务器端的购物车或订单总额
- 支付服务提供商（PSP）的授权和扣款操作

**注意：** 绝不要依赖客户端的显示金额作为最终收费依据。

### 4. 严格控制令牌处理流程

将 Google Pay 的令牌数据视为敏感信息：
- 仅将令牌数据转发给后端或支付服务提供商（PSP）
- 仅保留元数据（如请求 ID、状态、金额、货币）
- 绝不要将原始令牌数据存储在日志、备注或截图中

### 5. 明确指定令牌化方式

每个项目应使用一种统一的令牌化方式：
- 对于大多数集成场景，使用 `PAYMENT_GATEWAY`
- 仅在用户明确同意并具备解密权限的情况下，使用 `DIRECT` 方式

**注意：** 不要在没有书面迁移计划和风险评估的情况下混合使用不同的令牌化方式。

### 6. 确保支付流程具有幂等性和可恢复性

所有关键操作（如授权请求、扣款请求、退款或取消操作）都必须具备幂等性和可恢复性：
- 每次重试请求都必须使用相同的标识符来避免重复计费

### 7. 分离测试环境和生产环境

**注意：** 在所有测试环节都通过之前，不要进行生产环境的部署：
- 确保测试了成功支付、拒绝支付、取消支付和超时等所有情况
- 确保所有支持的设备和浏览器环境都能正常使用备用支付方式
- 当 Google Pay 不可用时，备用支付方式能够正常工作
- 确保有故障监控和警报机制

## 常见问题

- 将测试环境中的设置应用到生产环境可能导致用户支付失败
- 不同环境中的支付服务提供商（PSP）ID 不匹配可能导致令牌处理错误
- 跳过 `isReadyToPay` 等状态检查可能导致钱包按钮功能异常
- 依赖客户端的显示金额可能导致授权金额与实际扣款金额不一致
- 重试时缺少幂等性控制可能导致重复计费或退款操作
- 在没有备用支付方式的情况下直接进行生产环境部署可能导致支付失败

## 外部接口

| 接口地址 | 发送的数据 | 用途 |
|----------|-----------|---------|
| https://pay.google.com | 支付请求数据和钱包交互信息 | 用于与 Google Pay 客户端进行交互 |
| https://pay.google.com/gp/p/js/pay.js | JavaScript 客户端库加载脚本 | 用于加载 Google Pay 的 JavaScript 客户端库 |
| https://payments.developers.google.com | 文档获取接口 | 用于获取集成文档和测试用卡信息 |

**注意：** 除非目标支付服务提供商（PSP）有特殊要求，否则不要发送其他数据。

## 安全与隐私

**数据传输规则：**
- 出局到外部的数据：仅包括 Google Pay 所需要的请求数据和支付令牌数据
- 本地存储的数据：包括集成配置信息、验证结果和故障日志（但不包含原始令牌数据）

**重要说明：**
- 本技能不允许将原始令牌数据存储在内存文件中
- 必须满足 Google Pay 和支付服务提供商（PSP）的必备条件
- 未经明确的安全检查，不得直接将功能部署到生产环境

## 信任机制

Google Pay 的集成依赖于 Google 的基础设施和所选择的支付服务提供商（PSP）。只有在您信任这些服务及您的支付后端系统的情况下，才能安装和使用本技能。

## 相关技能

如果用户需要，可以使用以下命令安装相关技能：
- `clawhub install <slug>`：安装 `payments`（通用支付设计和结账流程相关技能）
- `android`：Android 平台的实现和运行时故障排查技巧
- `billing`：账单管理、对账和支付生命周期管理
- `auth`：交易流程中的身份验证和会话安全机制
- `api`：可靠的后端 API 设计和容错集成方案

## 反馈建议

- 如果本技能对您有帮助，请给 `clawhub` 评分（例如：给它打星）
- 为了获取最新信息，请使用 `clawhub sync` 命令保持同步