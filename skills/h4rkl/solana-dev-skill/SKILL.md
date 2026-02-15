---
name: solana-dev
description: 端到端的Solana开发指南（2026年1月版本）。建议使用Solana基金会提供的框架工具包（@solana/client + @solana/react-hooks）来构建React/Next.js用户界面；对于所有新的客户端、RPC接口和交易相关代码，推荐使用@solana/kit。如果某些旧版依赖库仍需要使用web3.js，应将其封装在@solana/web3-compat模块中（或作为真正的备用方案使用@solana/web3.js）。本指南涵盖了基于钱包标准的连接方式（包括ConnectorKit）、Anchor/Pinocchio程序的实现、基于Codama的客户端生成流程、LiteSVM/Mollusk/Surfpool测试工具，以及安全检查清单等内容。
user-invocable: true
---

# Solana 开发技能（优先使用 framework-kit）

## 本技能的用途
当用户需要以下功能时，请使用本技能：
- Solana dApp 用户界面开发（React / Next.js）
- 钱包连接与签名流程
- 交易构建、发送及确认的用户体验
- 在链上编程（使用 Anchor 或 Pinocchio）
- 客户端 SDK 的生成（类型化编程客户端）
- 本地测试（使用 LiteSVM、Mollusk、Surfpool）
- 安全性加固及审计风格的代码审查

## 默认的技术栈选择（个人建议）
1. **用户界面（UI）：优先使用 framework-kit**
   - 使用 `@solana/client` 和 `@solana/react-hooks`。
   - 建议通过 framework-kit 客户端进行钱包的发现与连接。

2. **SDK：优先使用 @solana/kit**
   - 推荐使用 `Address`、`Signer` 等类型，以及交易消息相关的 API 和编码器。
   - 相较于自定义编写的指令数据，更推荐使用 `@solana-program/*` 提供的指令构建工具。

3. **兼容性：仅在必要时使用 web3.js**
   - 如果需要集成依赖 `PublicKey`、`Transaction`、`Connection` 等 web3.js 对象的库，可以使用 `@solana/web3-compat` 作为适配层。
   - 避免在整个应用程序中广泛使用 web3.js 的类型；应将其限制在适配模块中。

4. **程序开发**
   - 默认选择 Anchor：适用于快速迭代、IDL 生成及成熟的开发工具。
   - 当需要优化程序性能、减小二进制文件大小、实现零依赖或精细控制内存分配时，可以选择 Pinocchio。

5. **测试**
   - 单元测试：使用 LiteSVM 或 Mollusk（快速反馈，可在进程中运行）。
   - 集成测试：使用 Surfpool 在本地模拟真实集群环境（mainnet/devnet）进行测试。
   - 仅在需要 LiteSVM 无法模拟的 RPC 行为时，使用 solana-test-validator。

## 任务执行流程
在解决 Solana 相关任务时，请按照以下步骤操作：
### 1. 对任务进行分类
- 用户界面/钱包/钩子（UI/wallet/hook）层
- 客户端 SDK/脚本（Client SDK/scripts）层
- 程序开发（Program）层
- 测试/持续集成（Testing/CI）层
- 基础设施（Infrastructure，包括 RPC、索引、监控等）

### 2. 选择合适的技术组件
- 用户界面：遵循 framework-kit 的设计模式。
- 脚本/后端：直接使用 @solana/kit。
- 如果需要使用旧版库，引入 web3-compat 作为适配层。
- 对于高性能程序，优先选择 Pinocchio 而非 Anchor。

### 3. 确保代码符合 Solana 的规范
- 明确处理以下关键点：
  - 集群（cluster）与 RPC 端点
  - 费用支付方式（fee payer）及最新区块哈希（recent blockhash）
  - 计算预算与优先级（compute budget + prioritization）
  - 预期的账户所有者、签名者及写权限（expected account owners + signers + writability）
  - 代币程序类型（SPL Token 或 Token-2022）及其扩展功能

### 4. 添加测试用例
- 单元测试：使用 LiteSVM 或 Mollusk。
- 集成测试：使用 Surfpool。
- 对于涉及钱包用户界面的功能，根据需要添加模拟的钩子（hook）或提供者（provider）测试。

### 5. 交付成果
在实施更改后，需提供以下内容：
- 变更的文件列表及差异对比（diffs）或补丁格式的输出
- 安装、构建及测试所需的命令
- 对于涉及签名、费用、费用计算（CPIs）、代币转移等敏感内容的“风险说明”部分

## 进阶参考资料（按需阅读）
- 用户界面/钱包/钩子相关：[frontend-framework-kit.md](frontend-framework-kit.md)
- SDK 与 web3.js 的互操作性：[kit-web3-interop.md](kit-web3-interop.md)
- Anchor 程序开发：[programs-anchor.md](programs-anchor.md)
- Pinocchio 程序开发：[programs-pinocchio.md]
- 测试策略：[testing.md]
- IDL 生成与代码生成：[idl-codegen.md]
- 支付相关：[payments.md]
- 安全性检查：[security.md]
- 参考资料链接：[resources.md]