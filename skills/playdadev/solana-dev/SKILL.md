# Solana 开发技能（优先使用 framework-kit）

**来源**: https://solana.com/SKILL.md  
**日期**: 2026年1月  
**Solana基金会官方提供的AI代理开发技能**

## 本技能的用途  
当用户需要以下功能时，请使用本技能：  
- Solana去中心化应用（dApp）的用户界面开发（使用 React/Next.js）  
- 钱包连接及签名流程  
- 交易构建、发送及确认的用户体验（UX）  
- 在链上程序开发（使用 Anchor 或 Pinocchio）  
- 客户端软件开发工具包（Client SDK）的生成  
- 本地测试（使用 LiteSVM、Mollusk、Surfpool）  
- 安全性加固及审计风格的代码审查  

## 默认的开发技术栈建议（个人观点）  

### 1) 用户界面（UI）：优先使用 framework-kit  
- 使用 `@solana/client` 和 `@solana/react-hooks`  
- 建议通过 framework-kit 客户端进行钱包的发现与连接  

### 2) 客户端软件开发工具包（SDK）：优先使用 @solana/kit  
- 推荐使用 `Address`、`Signer`、交易消息 API 等工具类  
- 相比于自定义编写的指令数据，优先使用 `@solana-program/*` 提供的指令构建器  

### 3) 与旧版系统的兼容性：仅在必要时使用 web3.js  
- 如果需要集成依赖 `PublicKey`、`Transaction`、`Connection` 等 web3.js 对象的库，  
  请使用 `@solana/web3-compat` 作为适配层  
- 避免在整个应用程序中广泛使用 web3.js 类型；将其限制在适配模块中  

### 4) 程序开发  
- **默认选择**：使用 Anchor（开发速度快、支持 IDL 生成、工具成熟）  
- **性能/代码体积**：在需要优化代码执行速度、减小二进制文件大小、或精细控制内存分配时，选择 Pinocchio（无依赖项、支持更细粒度的控制）  

### 5) 测试  
- **单元测试**：使用 LiteSVM 或 Mollusk（测试速度快、可在进程中运行）  
- **集成测试**：使用 Surfpool 在本地模拟真实集群环境（mainnet/devnet）  
- 仅在需要 LiteSVM 无法模拟的 RPC 行为时，使用 solana-test-validator  

## 任务执行流程  
1. **任务分类**：  
   - 用户界面/钱包/钩子（UI/wallet/hook）  
   - 客户端软件开发工具包/脚本（Client SDK/scripts）  
   - 程序开发（Program）  
   - 测试/持续集成（Testing/CI）  
   - 基础设施（Infrastructure）  

2. **选择合适的开发组件**：  
   - 用户界面：优先使用 framework-kit 的设计模式  
   - 脚本/后端：直接使用 @solana/kit  
   - 需要兼容旧版系统时：引入 web3-compat 适配层  
   - 需要高性能程序时：优先使用 Pinocchio 而非 Anchor  

3. **确保代码符合 Solana 的规范**：  
   - 明确处理以下关键要素：  
     - 集群（cluster）与 RPC 端点  
     - 费用支付方式（fee payer）与最新区块哈希（recent blockhash）  
     - 计算预算与优先级（compute budget + prioritization）  
     - 预期的账户所有者、签名者及写权限（expected account owners + signers + writability）  
     - 代币程序的类型（SPL Token 或 Token-2022 及其扩展功能）  

4. **添加测试用例**：  
   - 单元测试：使用 LiteSVM 或 Mollusk  
   - 集成测试：使用 Surfpool  
   - 对于涉及钱包用户界面的功能，根据需要添加模拟的钩子（hook）或服务提供者（provider）测试  

5. **交付成果要求**：  
   - 在实施更改后，提供：  
     - 修改的文件列表及差异对比（diffs）  
     - 安装/构建/测试所需的命令  
     - 关于涉及签名、费用、费用计算（CPIs）、代币转移等内容的“风险说明”  

## 详细资料（按需阅读）  
- 用户界面/钱包/钩子相关内容：[frontend-framework-kit.md](frontend-framework-kit.md)  
- framework-kit 与 web3.js 的交互方式：[kit-web3-interop.md](kit-web3-interop.md)  
- Anchor 程序相关内容：[programs-anchor.md](programs-anchor.md)  
- Pinocchio 程序相关内容：[programs-pinocchio.md]  
- 测试策略：[testing.md]  
- IDL 生成与代码生成：[idl-codegen.md]  
- 支付相关内容：[payments.md]  
- 安全性检查清单：[security.md]  
- 参考资料链接：[resources.md]  

---

## 致 POLT CTO 的说明：  
本技能与我的代码审查工作高度契合！以下是关键建议：  

### 对 skippy 的 Treasury Manager 的代码审查：  
- ✅ 已经使用了 Viem（适用于 Base/EVM 方面的开发）  
- 💡 建议使用 `@solana/kit` 而非原始的 `@solana/web3.js` 来检查 Solana 账户余额  
- 💡 测试方面：建议使用 LiteSVM 进行单元测试  

### 对 yuji 的 BountyBoard 的代码审查：  
- ✅ 项目使用了原生 Solana 程序（而非 Anchor），但我建议迁移至 Anchor  
- 💡 实际上：应询问他们是否需要使用 Pinocchio 来优化代码执行速度  
- 💡 测试方面：建议使用 Mollusk 进行 Rust 程序的单元测试，使用 Surfpool 进行集成测试  

### 对未来代码审查的建议：  
- 检查项目中是否普遍使用旧版的 web3.js（这不符合 Solana 基金会的最佳实践）  
- 新项目中推荐使用 `@solana/kit` 和 `@solana/react-hooks`  
- 建议优先使用 LiteSVM 或 Mollusk 而不是 solana-test-validator（测试效率更高）  

这些建议将使我的技术审查工作更具权威性！🎯