---
name: social-flow
description: 使用 Social Flow 作为代理控制平面，通过已安装的 `social` CLI 和 Gateway API 来执行 Meta 操作。当用户需要执行多步骤操作、请求审批、自动化操作，或者在认证、洞察、产品组合、Instagram、WhatsApp、Marketing API 以及 Gateway/Studio 工作流程中生成命令时，这种方案非常理想。它能够将自然语言指令转换为明确、经过风险控制的 Social Flow 命令，并在执行前进行确认。
metadata:
  openclaw:
    homepage: "https://github.com/vishalgojha/social-flow"
    requires:
      bins:
        - social
    install:
      - id: social-flow-cli-node
        kind: node
        package: "@vishalgojha/social-flow"
        bins:
          - social
        label: Install Social Flow CLI (npm)
---
# Social Flow 技能

将 **Social Flow** 作为 Meta 操作的代理控制平面来使用。

该技能可将自然语言操作请求转换为确定的 `social` 命令流，并在适用的情况下触发执行引擎、网关（Gateway）、SDK 以及托管层（Hosted layer）的相关操作。它适用于以下场景：

- 多步骤 Meta 操作（如身份验证、数据洞察、项目组合管理、内容发布、潜在客户管理工作流程）；
- 需要考虑速率限制和令牌（token）的执行逻辑；
- 通过 `social ops` 实现审批、警报和运行手册（runbooks）等功能；
- 根据需要启动或路由到 Hatch、Studio 或 Gateway。

我们的目标是确保操作的可靠性，而不仅仅是制定漂亮的计划。

## 核心工作流程

对于每个新任务或会话：

1. 在执行第一个命令之前验证环境。
2. 将用户意图解析到一个主要领域（domain）。
3. 当状态未知时，先进行只读检查。
4. 在执行前提出具体的命令。
5. 对写入操作应用风险控制机制，并请求用户确认。
6. 执行最少的命令序列。
7. 在失败时，进行有针对性的诊断，并仅在安全的情况下尝试重试。

## 验证环境

在执行任何复杂操作之前，请执行以下步骤：

- 运行 `social --version` 命令。
- 运行 `social doctor` 命令。

如果 `social` 不存在或明显过时，请检查其来源包：

- `https://www.npmjs.com/package/@vishalgojha/social-flow`
- `https://github.com/vishalgojha/social-flow`

建议由人工执行安装或升级操作：

```bash
npm install -g @vishalgojha/social-flow
```

之后重新运行：

```bash
social --version
social doctor
```

如果 `social doctor` 报告配置错误，请优先修复配置问题（包括身份验证、令牌设置和环境设置），然后再尝试执行复杂的工作流程。

## 领域路由

将用户意图路由到相应的领域：

- 身份验证与状态检查：`social auth ...`、`social doctor`、`social marketing status`
- 营销/广告：`social marketing ...`
- Instagram：`social marketing ...`（可使用 Instagram 相关接口），或 `social query instagram-*`（如果可用）
- WhatsApp：`social whatsapp ...`
- 操作/审批：`social ops ...`
- 代理/网关/Studio/托管层：`social hatch`、`social gateway ...`、`social studio ...`

仅加载或引用所选路径所需的特定领域文档，以及相关的安全/风险指南。

内部参考文档映射（如果存在）如下：

- 身份验证、查询、基本发布操作：`references/workflows-core.md`
- 营销和 WhatsApp 相关操作：`references/workflows-marketing-whatsapp.md`
- 操作、代理、网关、Studio 相关操作：`references/workflows-ops-agent-gateway.md`
- 命令查找及相关信息：`references/command-map.md`
- 错误处理与恢复指南：`references/troubleshooting.md`
- 风险管理指南：`references/safety-and-risk.md`

这些参考文档为内部使用，不应作为面向用户的公开要求展示。

## 执行策略

- 优先使用具体的 CLI 命令，而非模糊的描述。
- 当用户指定了客户端或工作空间时，确保命令与这些环境设置相匹配。
- 不要打印完整的令牌或敏感信息。
- 在确认安全之前，将未知的写入操作视为高风险操作。
- 当配置的可靠性较低或用户表示这是新机器时，先运行 `social doctor` 命令。

在响应操作时：

1. 显示一个简短的操作计划。
2. 展示一个或多个可执行的命令块。
3. 说明关键假设（工作空间、账户 ID、页面、时间范围等）。
4. 对于非只读操作，在执行前请求用户确认。

## 风险策略

请参考 `references/safety-and-risk.md` 以了解风险分类和相应的表述规则：

- 只读操作（如状态查询、数据洞察、测试性操作）可以立即执行。
- 低风险和中等风险的写入操作（如仅用于草稿的修改、沙箱环境中的操作）需要明确的用户确认。
- 高风险操作包括以下行为：
  - 支出预算；
  - 向真实用户发送消息；
  - 修改正在运行的活动、广告或创意内容；
  - 大规模处理潜在客户或联系人数据。

对于高风险操作：

- 提供明确的支出或交付警告；
- 提供可用的回滚或缓解措施。

如有疑问，应将任何操作视为高风险操作，并先征求用户确认。

## 输出格式

当该技能执行操作时，输出内容应包括：

1. 用一句话总结用户意图和选择的操作领域。
2. 按顺序列出要执行的 `social` 命令。
3. 说明相关假设（工作空间、账户 ID、日期范围、渠道等）。
4. 标明哪些命令是：
   - 安全的/仅限读取的；
   - 可写入但风险较低的；
   - 高风险的（并附带警告）。

在执行任何写入操作或高风险操作之前，务必请求用户明确确认。

该技能充当可靠的 Meta 操作辅助工具：提供精确的、基于风险控制的 `Social Flow` 命令建议，并由用户进行最终确认。