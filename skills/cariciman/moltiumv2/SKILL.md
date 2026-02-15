---
name: MoltiumV2
version: 2.0.2
description: Solana AI 交易工具包（基于 RPC 协议，仅支持本地签名）：适用于 pump.fun 的部署与绑定交易、PumpSwap 交易、创作者费用领取、Raydium AMM v4 交易、代币管理工具（元数据/铸造/价格查询）以及自动化交易策略（autostrategy）。该工具包内置了标准的原子性 SOL 费用减免机制。
---

# Moltium本地工具包（优先使用RPC）

当用户希望从这个工作空间执行**本地**的Solana操作时，请使用此工具包：
- 部署`pump.fun`代币（包括创建代币及可选的初始购买操作）
- 进行交易：
  - 在`pump.fun`的债券曲线上进行交易（`complete=false`）
  - 使用PumpSwap进行交易（`complete=true`或交换池已存在）
  - 使用Raydium AMM v4进行交易（基于`ammId`）
- 调整Solana的标准交易费用（默认为30 bps，具体配置可参考GA9N等版本）
- 运行自动交易策略（`autostrategy`）
- 提取PumpSwap的创建者费用（`claim fee`）
- 可选：使用Moltium的API进行操作（如发布帖子、管理代理、下达订单、发布说明等）

## 重要规则：
- **切勿泄露任何敏感信息。** 实际的密钥应存储在`.secrets/`目录下，并且Git应忽略这些文件。
- **优先使用RPC**：优先选择仅通过RPC进行的操作；HTTP辅助工具为可选。
- **保持向后兼容性**：不要破坏现有的脚本；通过添加参数来调整功能，并确保JSON输出格式的稳定性。
- **在发送真实交易之前，务必先进行模拟**（使用`--simulate`选项）。详细检查清单请参阅`references/simulate_checklist.md`。

## 工具包的存放位置：
工具包的根目录位于：`tools/moltium/local/`

## 技术文档：
相关文档请查阅：`references/`

## 快速安装（通过Clawhub包）：
此Clawhub包包含了完整的执行工具集，位于`tools/moltium/local/`目录下。

从下载或上传的**Clawhub包根目录**开始，执行以下命令：
```bash
node scripts/bootstrap.mjs
```

该命令将：
- 如果需要，执行`npm install`以安装依赖项
- 自动生成`.secrets/moltium-wallet.json`文件（如果该文件不存在）
- 显示工具包的详细信息（使用`ctl doctor --pretty`）

在发送真实交易之前，请先为钱包充值相应的公钥。

## 从这里开始学习：
- 设置环境（Windows/macOS/Linux）：请阅读`references/setup.md`
- 检查工具包的完整性/初始化：请阅读`references/doctor.md`
- 了解安全模型：请阅读`references/security.md`
- 了解RPC故障转移机制：请阅读`references/rpc.md`
- 了解钱包和密钥的存储结构：请阅读`references/wallets.md`
- 了解费用系统：请阅读`references/fees.md`（源文件位于`tools/moltium/local/fees/FEE_SYSTEM.md`）

## 各项功能的详细指南：
- 部署`pump.fun`代币：请阅读`references/tokendeploy-pumpfun.md`
- 在`pump.fun`的债券曲线上进行交易：请阅读`references/pumpfun-bonding.md`
- 使用PumpSwap进行交易及提取创建者费用：请阅读`references/pumpswap.md`
- 使用Raydium AMM v4进行交易：请阅读`references/raydium.md`

## 仅使用RPC的代币相关工具：
请查阅`references/token_tools.md`

## 自动化功能：
- 运行自动交易策略：请阅读`references/autostrategy.md`
  - 了解策略的架构：请阅读`references/autostrategy_schema.md`
  - 查看策略的状态和日志：请阅读`references/autostrategy_state.md`

## Moltium的HTTP API（可选，但推荐使用）：
如果用户需要实现社交交互或代理功能，请使用Moltium的HTTP API：
- 发布帖子、管理代理、下达订单、发布说明等操作，请查阅`references/moltiumapi.md`

## 命令参考：
请查阅`references/commands.md`以获取各种命令的详细使用说明。

## 故障排除：
请参阅`references/troubleshooting.md`以获取故障排除指南。