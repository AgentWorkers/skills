---
name: Apple Pay
slug: apple-pay
version: 1.0.0
homepage: https://clawic.com/skills/apple-pay
description: 为网页和 iOS 平台实现 Apple Pay 功能，包括商户验证、令牌处理以及安全可靠的结账流程。
changelog: Expanded implementation and rollout guidance with stronger validation and incident handling playbooks.
metadata: {"clawdbot":{"emoji":"🍎","requires":{"bins":["curl","jq"],"env":["APPLE_PAY_MERCHANT_ID"]},"os":["darwin","linux","win32"]}}
---
## 设置

首次使用本技能时，请阅读 `setup.md` 文件，确认目标平台、支付服务提供商（PSP）以及发布版本，然后再进行任何代码修改。

## 使用场景

当用户需要使用 Apple Pay 进行结算、订阅或实现“钱包优先”的支付流程改进时，请使用本技能。相关操作由专业代理负责处理，包括架构选择、商户设置、支付令牌的安全管理、上线前的验证以及上线后的运营维护。

## 架构

所有与 Apple Pay 相关的数据和配置文件都存储在 `~/apple-pay/` 目录下。具体设置和状态信息请参考 `memory-template.md` 文件。

```
~/apple-pay/
|-- memory.md                 # Project snapshot, risk status, and rollout state
|-- implementations.md        # Selected approach and platform notes
|-- validation-log.md         # Test evidence and environment results
`-- incidents.md              # Failed payments, root causes, and fixes
```

## 快速参考

根据当前任务的需求，选择最相关的文件进行操作：

| 任务内容 | 对应文件 |
|---------|---------|
| 设置流程 | `setup.md` |
| 内存管理模板 | `memory-template.md` |
| 实施计划 | `implementation-playbook.md` |
| 验证清单 | `validation-checklist.md` |
| 故障处理 | `failure-handling.md` |
| 发布与运营 | `launch-playbook.md` |
| 定期支付与订阅流程 | `recurring-payments.md` |

## 必需条件

- 环境变量：`APPLE_PAY_MERCHANT_ID`
- 用于诊断的 CLI 工具：`curl`、`jq`
- 对目标环境的 Apple 商户账户具有访问权限

**注意**：切勿要求用户在聊天中粘贴私钥或完整的证书信息。

## 数据存储

所有本地配置文件和日志均保存在 `~/apple-pay/` 目录下：
- `memory-file`：存储当前系统状态及集成相关决策
- `validation-log-file`：记录测试结果和验证证据
- `incidents-file`：记录故障信息及相应的处理措施

## 核心规则

### 1. 在选择集成方案前明确业务目标

首先明确目标：
- 提高结算成功率
- 加快重复购买的流程
- 优化移动支付用户体验
- 降低支付失败率

然后选择一种主要的集成方案：
- 使用 Apple Pay 的 JavaScript 和商户会话后端进行 Web 集成
- 使用 PassKit 进行原生 iOS 集成
- 通过支付服务提供商（如 Stripe、Adyen、Braintree）进行中间件集成

**注意**：除非用户明确要求进行迁移，否则不要在同一版本中混合使用多种集成方案。

### 2. 确保商户和域名满足前提条件

在实施之前，请确认以下条件：
- 商户 ID 存在且与目标环境匹配
- 支付处理证书有效且可用
- 域名关联文件已正确配置且可访问
- 沙盒环境和生产环境的认证信息是分开管理的

如果任何前提条件未满足，请暂停开发并制定详细的检查清单。

### 3. 确保金额和货币信息的一致性

金额和货币类型必须在以下所有环节保持一致：
- 客户端发送的请求数据
- 服务器端的购物车或订单总额
- 支付服务提供商的授权和扣款请求

**注意**：切勿依赖客户端提供的总额作为最终收费金额。

### 4. 严格管理支付令牌

将 Apple Pay 的支付令牌视为敏感信息：
- 仅将令牌数据转发给后端或支付服务提供商
- 仅保留元数据（请求 ID、状态、金额、货币类型）
- 绝不要将原始令牌数据存储在日志、笔记或截图中

### 5. 确保支付操作的幂等性和可恢复性

所有关键操作（如授权请求、扣款请求、退款或取消操作）都必须具备幂等性和可恢复性。重复请求时必须使用相同的标识符以避免重复计费。

### 6. 分离沙盒环境和生产环境

建议在所有测试环节都通过后才能进行生产环境的部署：
- 确保沙盒环境中的支付流程、拒绝处理、取消操作和超时处理都能正常工作
- 确保支持的所有设备和浏览器都能正常使用支付功能
- 在 Apple Pay 不可用时，备用支付方式（如信用卡）能够正常使用
- 确保故障能够被及时发现并触发相应的警报

### 7. 提供详细的支持文档

对于每次集成，需提供以下信息：
- 客户在成功和失败情况下看到的界面
- 可恢复的错误类型及相应的处理方法
- 支持团队在遇到不同类型故障时应采取的措施
- 是否需要回滚或紧急停止服务的决策点

**注意**：优先确保支付的稳定性和可靠性，而非功能的全面性。

## 常见错误

- 从客户端执行商户验证操作会导致敏感信息泄露，从而影响审核流程
- 信任客户端提供的总额可能导致授权金额与实际扣款金额不一致
- 在生产环境中重复使用沙盒环境的认证信息可能导致支付失败
- 将仅针对模拟器的测试结果作为正式发布的依据可能导致实际设备出现故障
- 重试操作时缺乏幂等性处理机制可能导致重复计费或退款处理复杂化
- 在没有备用支付方式的情况下直接进行生产环境部署可能导致支付失败

## 外部接口

| 接口 | 发送的数据 | 用途 |
|---------|-----------|---------|
| https://apple-pay-gateway.apple.com | 商户验证请求数据 | 用于在 Web 环境中建立 Apple Pay 的商户会话 |
| https://apple-pay-gateway-cert.apple.com | 商户验证请求数据（沙盒/证书路径） | 用于在非生产环境中验证商户会话 |
| https://appleid.apple.com | 账户和商户身份验证信息 | 用于处理与 Apple 账户和商户相关的操作 |

**注意**：除非指定的支付服务提供商有特殊要求，否则不要发送其他数据。

## 安全与隐私

**数据传输**：
- 发往 Apple 服务器的商户验证请求数据
- 发送给支付服务提供商或后端的支付令牌数据

**数据存储**：
- 所有集成相关的本地配置文件和日志均保存在 `~/apple-pay/` 目录下
- 验证结果和故障日志中不包含原始支付令牌信息

**重要提示**：
- 本技能不会将原始支付令牌存储在内存文件中
- 未满足 Apple 的强制性要求之前，不得进行生产环境的部署
- 未经明确检查，不得直接将本技能投入生产环境

## 信任机制

Apple Pay 的集成依赖于 Apple 的基础设施和所选的支付服务提供商。只有在您信任这些服务及其支付后端的情况下，才能安装和运行本技能。

## 相关技能

如果用户需要，可以使用以下命令进行安装：
- `clawhub install <slug>`：安装相关技能
- `payments`：通用支付设计和结算决策框架
- `app-store-connect`：Apple 生态系统的账户管理和操作流程
- `ios`：iOS 平台的实现及设备级调试工具
- `auth`：交易流程中的身份验证和会话安全机制
- `api`：可靠的后端 API 接口及容错性强的集成方案

## 反馈建议

- 如果本技能对您有帮助，请给 `clawhub` 评分（例如：给它打星）：`clawhub star apple-pay`
- 为了获取最新信息，请定期更新：`clawhub sync`