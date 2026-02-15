---
name: Solaudit - Smart Contract Security Scanner
description: Solidity 智能合约安全审计工具：能够检测重入（reentrancy）问题、溢出（overflow）问题以及访问控制漏洞。支持识别 50 多种常见的安全漏洞模式。兼容持续集成/持续部署（CI/CD）流程。提供免费的命令行工具（CLI）。
---

# Solaudit

这是一个用于检测Solidity智能合约安全漏洞的扫描工具，可在合约部署前发现潜在问题。

## 安装

```bash
npm install -g solaudit-cli
```

## 命令

### 全面审计
```bash
solaudit audit Contract.sol
solaudit audit ./contracts/ -r              # Recursive
solaudit audit . -s high                    # Only high+ severity
solaudit audit . --gas --best-practices     # Include all checks
```

### 快速检查
```bash
solaudit check Token.sol
solaudit check Vault.sol -s critical
```

### Gas使用情况分析
```bash
solaudit gas Contract.sol
```

### 模式匹配功能
```bash
solaudit patterns
solaudit patterns --category reentrancy
```

## 漏洞类型

### 严重漏洞
- 重入攻击（Reentrancy attacks）
- 未受保护的自我销毁功能（Unprotected self-destruct）
- Delegatecall注入攻击（Delegatecall injection）
- 签名重放攻击（Signature replay）

### 高风险漏洞
- 整数溢出/下溢（Integer overflow/underflow）
- 访问控制问题（Access control issues）
- 未经过检查的返回值（Unchecked return values）
- 价格操纵行为（Price manipulation）

### 中等风险漏洞
- 交易发起者身份验证问题（tx.origin authentication issues）
- 使用了`float`类型的`pragma`指令（Floating pragma）
- 依赖时间戳（Timestamp dependence）
- 面向未来的代码执行风险（Front-running risks）

### 低风险漏洞
- 未使用的变量（Unused variables）
- 缺失的事件处理逻辑（Missing events）
- 变量的可见性设置不当（Implicit visibility）
- 使用了硬编码的数值（Magic numbers）

## 输出格式

```bash
solaudit audit Contract.sol              # Table (default)
solaudit audit Contract.sol -o json      # JSON
solaudit audit Contract.sol -o markdown  # Markdown report
```

## 集成到持续集成/持续部署（CI/CD）流程

```bash
# Fail on critical issues
solaudit audit ./contracts/ -s critical && echo "Passed"

# GitHub Actions
- run: npm install -g solaudit-cli
- run: solaudit audit ./contracts/ -r -s high
```

## 常见使用场景

- **部署前检查**：确保合约安全无误
- **生成审计报告**：提供详细的漏洞分析
- **Gas使用优化**：帮助减少合约运行时的资源消耗

---

**由 [LXGIC Studios](https://lxgicstudios.com) 开发**

🔗 [GitHub](https://github.com/lxgicstudios/solaudit) · [Twitter](https://x.com/lxgicstudios)