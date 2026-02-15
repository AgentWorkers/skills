---
name: clanker
description: 使用 Clanker SDK 在 Base 上部署 ERC20 代币。这些代币配备了内置的 Uniswap V4 流动性池，支持 Base 主网和 Sepolia 测试网。配置文件中需要包含 PRIVATE_KEY。
metadata: {"clawdbot":{"emoji":"🪙","homepage":"https://clanker.world","requires":{"bins":["curl","jq","python3"]}}}
---

# Clanker 技能

使用 Clanker 协议在 Base 上部署 ERC20 代币，并利用内置的 Uniswap V4 流动性池。

## 设置

### 1. 配置

在 `~/.clawdbot/skills/clanker/config.json` 文件中创建配置文件：

**安全提示：** 请勿将您的私钥提交到版本控制系统中。建议使用环境变量或仓库外的单独配置文件来存储私钥。

### 2. 获取测试网 ETH

对于 Base Sepolia 的测试，您可以从以下地址获取免费的 ETH：
- https://cloud.base.org/faucet
- https://sepoliafaucet.com

**注意：** 使用这些 faucet 可能需要：
- 安装 MetaMask 或类似的钱包
- 使用社交账号（如 GitHub、Twitter）登录
- 每天仅允许请求 1-2 次

### 3. 安装依赖项（用于部署）

为了部署代币，需要安装 `web3` Python 包：

为了执行只读操作，只需安装 `curl`、`jq` 和 `python3` 即可。

## 使用方法

### 在主网上部署代币

使用以下命令在 Uniswap V4 上部署一个 ERC20 代币，并设置初始流动性为 0.1 ETH：

### 检查部署状态

检查部署交易是否成功。

### 获取代币信息

返回代币的名称、符号、总供应量等详细信息。

### 按部署者查找代币

查找由特定地址部署的所有代币。

### 在测试网（Sepolia）上部署

将代币部署到 Base Sepolia 测试网进行测试。

### 使用测试网

所有命令都支持 `--network testnet` 标志：

## 命令参考

| 命令 | 描述 | 参数 |
|---------|-------------|------------|
| `deploy` | 在主网上部署代币 | `<名称> <符号> <初始流动性 ETH>` |
| `testnet-deploy` | 在 Sepolia 测试网上部署 | `<名称> <符号>` |
| `status` | 检查部署状态 | `<交易哈希>` |
| `info` | 获取代币信息 | `<代币地址>` |
| `get-token` | 按部署者查找代币 | `<部署者地址>` |

## 示例

---

## 测试指南

### 第 1 步：设置测试网配置

### 第 2 步：获取测试网 ETH

1. 访问 https://cloud.base.org/faucet
2. 连接您的钱包（例如 MetaMask）
3. 请求测试网 ETH（0.001-0.01 ETH 应该足够）

**其他可选的 faucet：**
- https://sepoliafaucet.com
- https://faucet.paradigm.xyz

### 第 3 步：部署测试代币

使用以下命令部署一个代币：

或者，如果您希望设置初始流动性，可以使用以下命令：

### 第 4 步：验证部署

1. **检查交易状态：**
2. **获取代币信息：**
3. **在浏览器中查看交易详情：**
   - 打开 https://sepolia.basescan.org/tx/\<交易哈希\>
   - 在 https://sepolia.basescan.org/token/\<代币地址\> 查看代币合约

### 故障排除

**交易失败？**
- 确保您有足够的 ETH 作为交易手续费（gas）
- 确认 Clanker 合约在 Sepolia 上可用
- 检查网络连接是否正常

**无法获取测试网 ETH？**
- 尝试使用其他 faucet
- 每天等待 24 小时后再尝试
- 确认钱包连接是否正确

**私钥相关问题？**
- 确保私钥没有 “0x” 前缀（如果有，请将其删除）
- 检查配置文件的语法是否为有效的 JSON 格式

---

## 测试结果

### 只读操作 ✅

| 命令 | 网络 | 结果 |
|---------|---------|--------|
| `info` (WETH) | 主网 | ✅ 可以正常获取代币信息 |
| `get-token` | 主网 | ✅ 可以获取部署者信息 |
| `status` | 主网 | ✅ 可以检查交易状态 |

### 部署操作 ⚠️

| 功能 | 状态 | 备注 |
|---------|--------|-------|
| 使用 Python 进行部署 | ⚠️ 需要 Clanker 合约地址 |
| 基于 Web 的部署工具 | ✅ 推荐使用 | 可以访问 https://clanker.world |
| 直接调用合约 | 🔲 尚未实现 | 需要 Clanker 合约的 ABI（Application Binary Interface） |

**注意：** 完整的部署过程需要 Base Sepolia 上的 Clanker 合约地址。该协议相对较新，合约地址可能会发生变化。在生产环境中进行部署时，请参考官方文档。

---

## 安全最佳实践

1. **切勿将私钥提交到版本控制系统中**
2. **为测试网和主网使用不同的私钥**
3. **在主网部署前先在 Sepolia 上进行测试**
4. **在官方 Clanker 文档中验证合约地址**
5. **首次部署时使用少量的 ETH 作为初始流动性**
6. **监控已部署的代币，防止异常活动**

## 资源

- **官方网站：** https://clanker.world
- **文档：** https://docs.clanker.world
- **GitHub 仓库：** https://github.com/clanker-world
- **Base 主网浏览器：** https://basescan.org
- **Base Sepolia 浏览器：** https://sepolia.basescan.org

## 注意事项

- 所有部署操作都会创建带有内置 Uniswap V4 流动性池的代币
- 需要初始的 ETH 作为流动性来源
- 测试网上的部署是免费的（无需使用真实资金，但需要测试网 ETH）
- 如果 Clanker 合约不可用，部署可能会失败
- 如果操作超时，请检查网络连接是否正常