---
name: setup-solidity-contracts
description: "使用 OpenZeppelin Contracts 设置一个 Solidity 智能合约项目。适用于以下场景：  
(1) 用户需要创建一个新的 Hardhat 或 Foundry 项目；  
(2) 为 Solidity 安装 OpenZeppelin Contracts 的依赖项；  
(3) 配置 Foundry 的重映射（remappings）；  
(4) 了解 OpenZeppelin 的 Solidity 导入规范。"
license: AGPL-3.0-only
metadata:
  author: OpenZeppelin
---
# Solidity 开发环境搭建

对于现有的项目，可以通过查找 `hardhat.config.*`（Hardhat）或 `foundry.toml`（Foundry）文件来确定所使用的开发框架。对于新项目，需要询问用户他们倾向于使用哪种框架。

## Hardhat 开发环境搭建

- 初始化项目（仅在新项目启动时执行）

```bash
npx hardhat init        # Hardhat v2
npx hardhat --init      # Hardhat v3
```

- 安装 OpenZeppelin Contracts：

```bash
npm install @openzeppelin/contracts
```

- 如果使用可升级的合约（upgradeable contracts），还需要安装相应的可升级版本：

```bash
npm install @openzeppelin/contracts-upgradeable
```

## Foundry 开发环境搭建

- 安装 Foundry：

```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

- 初始化项目（仅在新项目启动时执行）

```bash
forge init my-project
cd my-project
```

- 添加 OpenZeppelin Contracts：

```bash
forge install OpenZeppelin/openzeppelin-contracts@v<VERSION>
```

- 如果使用可升级的合约，还需要添加相应的可升级版本：

```bash
forge install OpenZeppelin/openzeppelin-contracts-upgradeable@v<VERSION>
```

> 请访问 [https://github.com/OpenZeppelin/openzeppelin-contracts/releases](https://github.com/OpenZeppelin/openzeppelin-contracts/releases) 查看当前版本，并将其固定到一个特定的版本标签上。如果不指定版本标签，`forge install` 命令会下载默认分支，该分支可能不稳定。

- 如果不使用可升级合约，请创建 `remappings.txt` 文件：

```text
@openzeppelin/contracts/=lib/openzeppelin-contracts/contracts/
```

- 如果使用可升级合约，请创建 `remappings.txt` 文件：

```text
@openzeppelin/contracts/=lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/
@openzeppelin/contracts-upgradeable/=lib/openzeppelin-contracts-upgradeable/contracts/
```

> **注意：**
> 上述的路径映射规则意味着 `@openzeppelin/contracts/`（包括代理合约）和 `@openzeppelin/contracts-upgradeable/` 都来自 `openzeppelin-contracts-upgradeable` 子模块及其子目录。这些子目录中包含了与 `openzeppelin-contracts` 相同版本号的合约副本。这种路径格式是 Etherscan 验证所必需的。特别需要注意的是，任何单独安装的 `openzeppelin-contracts` 副本都不会被 Etherscan 验证工具识别。

## 导入合约的约定

- 标准合约的导入格式：`@openzeppelin/contracts/token/ERC20/ERC20.sol`
- 可升级合约的导入格式：`@openzeppelin/contracts-upgradeable/token/ERC20/ERC20Upgradeable.sol`
- 仅在通过代理（proxies）部署合约时使用可升级版本；否则应使用标准版本。