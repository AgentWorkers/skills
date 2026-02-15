---
name: solidity-lsp
description: **Solidity语言服务器**  
该服务器提供智能合约开发的全方位支持，包括编译、代码检查（linting）、安全分析以及代码智能功能（code intelligence），适用于`.sol`文件。无论您是在处理Ethereum智能合约、Substrate框架中的智能合约，还是任何需要编译、安全检测、Gas优化或代码导航的Solidity代码，这款服务器都是不可或缺的工具。对于ClawChain框架的开发来说，它更是至关重要。
---

# Solidity LSP

Solidity LSP（Language Server Protocol）是一个用于集成Solidity语言服务器的工具，通过`solc`（Solidity编译器）和`solhint`（代码检查工具）提供全面的智能合约开发支持。

## 功能

- **编译**：使用`solc`编译Solidity智能合约。
- **代码检查**：利用`solhint`进行静态分析，确保代码遵循最佳实践并不存在安全问题。
- **安全性检测**：识别常见的安全漏洞（如重入（reentrancy）、溢出（overflow）等。
- **Gas优化**：识别耗时的操作，提高合约的执行效率。
- **代码智能**：提供语法高亮显示和错误检测功能。
- **支持的文件扩展名**：`.sol`。

## 安装

请先安装Solidity编译器和`solhint`：

```bash
# Solidity compiler
npm install -g solc

# Solidity linter
npm install -g solhint
```

安装完成后，请验证安装是否成功：

```bash
solcjs --version
solhint --version
```

## 使用方法

### 编译Solidity合约

```bash
solcjs --bin --abi contract.sol
```

### 带有优化的编译

```bash
solcjs --optimize --bin --abi contract.sol
```

### 检查合约代码

- 单个文件：运行`solhint`对文件进行代码检查。
- 整个项目：运行`solhint`对整个项目进行代码检查。

### 安全性分析

`solhint`默认包含了安全规则。如需进行更高级的安全性分析，可以考虑使用额外的工具。

```bash
# Install slither (requires Python)
pip3 install slither-analyzer

# Run security analysis
slither contracts/
```

## 配置

### `solhint`配置

在项目根目录下创建`.solhint.json`文件以配置`solhint`的行为：

```json
{
  "extends": "solhint:recommended",
  "rules": {
    "compiler-version": ["error", "^0.8.0"],
    "func-visibility": ["warn", {"ignoreConstructors": true}],
    "max-line-length": ["warn", 120],
    "not-rely-on-time": "warn",
    "avoid-low-level-calls": "warn",
    "no-inline-assembly": "warn"
  }
}
```

## 与Hardhat/Foundry的集成

有关完整的开发环境配置，请参阅`references/frameworks.md`。

## 开发流程

在开发智能合约时，请遵循以下步骤：

1. **编写代码**：编写Solidity合约代码。
2. **代码检查**：运行`solhint`以尽早发现潜在问题。
3. **编译**：使用`solcjs`验证代码是否能够成功编译。
4. **安全性分析**：在部署前使用安全工具进行检测。
5. **测试**：编写全面的单元测试。

## 常见问题

- **编译器版本不匹配**：在合约中指定正确的`pragma`版本。
- **Gas优化**：尽可能使用`view`或`pure`修饰符来减少Gas消耗。
- **安全性**：切勿使用`tx.origin`进行身份验证。
- **最佳实践**：遵循“检查（Checks）- 动作（Effects）- 相互作用（Interactions）”的设计模式。

## 更多信息

- [Solidity官方文档](https://docs.soliditylang.org/)
- [Solhint GitHub仓库](https://github.com/protofire/solhint)
- [Solidity安全最佳实践](https://consensys.github.io/smart-contract-best-practices/)
- 有关Hardhat/Foundry的集成信息，请参阅`references/frameworks.md`。