---
name: sui-coverage
description: 分析 Sui Move 测试的覆盖范围，识别未测试的代码，编写缺失的测试用例，并进行安全审计。提供用于解析测试覆盖结果和生成报告的 Python 工具。
homepage: https://github.com/EasonC13-agent/sui-coverage-demo
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["python3", "sui"]
---

# Sui覆盖度技能

通过安全分析来分析和自动提升Sui Move智能合约的测试覆盖率。

**GitHub仓库：** <https://github.com/EasonC13-agent/sui-skills/tree/main/sui-coverage>

## 先决条件

### 安装Sui CLI

```bash
# macOS (recommended)
brew install sui

# Other platforms: see official docs
# https://docs.sui.io/guides/developer/getting-started/sui-install
```

**验证安装结果：**
```bash
sui --version
```

## 快速参考

```bash
# Location of tools (adjust to your skill installation path)
SKILL_DIR=<your-workspace>/skills/sui-coverage

# Full workflow
cd /path/to/move/package
sui move test --coverage --trace
python3 $SKILL_DIR/analyze_source.py -m <module> -o coverage.md
```

## 工作流程：自动提升测试覆盖率

### 第1步：运行覆盖率分析

```bash
cd <package_path>
sui move test --coverage --trace
python3 $SKILL_DIR/analyze_source.py -m <module_name> -o coverage.md
```

### 第2步：阅读覆盖率报告

阅读生成的`coverage.md`文件，以识别以下问题：
- 🔴 **未调用的函数** - 从未被执行的函数
- 🔴 **未覆盖的断言** - 未被测试的`assert!()`失败路径
- 🔴 **未覆盖的分支** - 未执行的`if/else`分支

### 第3步：编写缺失的测试用例

对于每个未覆盖的项，编写相应的测试用例：

#### A. 未调用的函数
```move
#[test]
fun test_<function_name>() {
    // Setup
    let mut ctx = tx_context::dummy();
    // Call the uncovered function
    <function_name>(...);
    // Assert expected behavior
}
```

#### B. 断言失败路径（预期失败）
```move
#[test]
#[expected_failure(abort_code = <ERROR_CODE>)]
fun test_<function>_fails_when_<condition>() {
    let mut ctx = tx_context::dummy();
    // Setup state that triggers the assertion failure
    <function_call_that_should_fail>();
}
```

#### C. 分支覆盖（if/else）
```move
#[test]
fun test_<function>_when_<condition_true>() { ... }

#[test]  
fun test_<function>_when_<condition_false>() { ... }
```

### 第4步：验证覆盖率是否提升

```bash
sui move test --coverage --trace
python3 $SKILL_DIR/analyze_source.py -m <module_name>
```

---

## 工具

### 1. analyze_source.py（主要工具）

```bash
python3 $SKILL_DIR/analyze_source.py --module <name> [options]

Options:
  -m, --module    Module name (required)
  -p, --path      Package path (default: .)
  -o, --output    Output file (e.g., coverage.md)
  --json          JSON output
  --markdown      Markdown to stdout
```

### 2. analyze.py（LCOV统计工具）

```bash
sui move coverage lcov
python3 $SKILL_DIR/analyze.py lcov.info -f "<package>" -s sources/

Options:
  -f, --filter       Filter by path pattern
  -s, --source-dir   Source directory for context
  -i, --issues-only  Only show files with issues
  -j, --json         JSON output
```

### 3. parse_bytecode.py（底层代码分析工具）

```bash
sui move coverage bytecode --module <name> | python3 $SKILL_DIR/parse_bytecode.py
```

---

## 常见模式

### 测试断言失败

```move
// Source code:
public fun withdraw(balance: &mut u64, amount: u64) {
    assert!(*balance >= amount, EInsufficientBalance);  // ← This failure path
    *balance = *balance - amount;
}

// Test for the failure path:
#[test]
#[expected_failure(abort_code = EInsufficientBalance)]
fun test_withdraw_insufficient_balance() {
    let mut balance = 50;
    withdraw(&mut balance, 100);  // Should fail: 50 < 100
}
```

### 测试所有分支

```move
// Source code:
public fun classify(value: u64): u8 {
    if (value == 0) {
        0
    } else if (value < 100) {
        1
    } else {
        2
    }
}

// Tests for all branches:
#[test]
fun test_classify_zero() {
    assert!(classify(0) == 0, 0);
}

#[test]
fun test_classify_small() {
    assert!(classify(50) == 1, 0);
}

#[test]
fun test_classify_large() {
    assert!(classify(100) == 2, 0);
}
```

### 测试对象生命周期

```move
#[test]
fun test_full_lifecycle() {
    let mut ctx = tx_context::dummy();
    
    // Create
    let obj = create(&mut ctx);
    assert!(get_value(&obj) == 0, 0);
    
    // Modify
    increment(&mut obj);
    assert!(get_value(&obj) == 1, 0);
    
    // Destroy
    destroy(obj);
}
```

---

## 错误代码参考

在编写`#[expected_failure]`类型的测试用例时，请使用以下错误代码常量：

```move
// If the module defines:
const EInvalidInput: u64 = 1;
const ENotAuthorized: u64 = 2;

// Use in test:
#[expected_failure(abort_code = EInvalidInput)]
fun test_invalid_input() { ... }

// Or use the module-qualified name:
#[expected_failure(abort_code = my_module::EInvalidInput)]
fun test_invalid_input() { ... }
```

---

## 示例：完整的自动覆盖度提升流程

```bash
# 1. Analyze current coverage
cd /path/to/my_package
sui move test --coverage --trace
python3 $SKILL_DIR/analyze_source.py -m my_module -o coverage.md

# 2. Review what's missing
cat coverage.md
# Shows:
# - decrement() not called
# - assert!(value > 0, EValueZero) failure not tested

# 3. Add tests to sources/my_module.move or tests/my_module_tests.move
# (write the missing tests)

# 4. Verify improvement
sui move test --coverage --trace
python3 $SKILL_DIR/analyze_source.py -m my_module

# 5. Repeat until 100% coverage
```

---

## 与代理工作流程的集成

当需要提升测试覆盖率时，请按照以下步骤操作：
1. **运行分析** - 获取当前的覆盖率状态
2. **阅读源代码** - 理解模块的逻辑
3. **识别不足之处** - 列出未覆盖的函数/分支/断言
4. **安全审查** - 在编写测试用例的同时分析潜在的安全漏洞
5. **编写测试用例** - 为每个不足之处以及安全边界情况创建测试用例
6. **报告发现的问题** - 记录所有发现的安全问题
7. **验证结果** - 重新运行覆盖率分析以确认覆盖率是否提升

**请务必提交所有测试用例的修改：**
```bash
git add sources/ tests/
git commit -m "Improve test coverage for <module>"
```

---

## 测试过程中的安全分析

**编写测试用例 = 理解合约逻辑 = 发现安全漏洞**

在编写测试用例时，重点关注以下安全问题：

### 1. 访问控制
```
Questions to ask:
- Who can call this function?
- Should there be owner/admin checks?
- Can unauthorized users manipulate state?

Red flags:
- Public functions that modify critical state without checks
- Missing capability/witness patterns
```

### 2. 整数溢出/下溢
```
Questions to ask:
- What happens at u64::MAX?
- What happens when subtracting from 0?
- Are arithmetic operations checked?

Test pattern:
#[test]
fun test_overflow_boundary() {
    // Test with max values
}
```

### 3. 状态操作
```
Questions to ask:
- Can state be left in inconsistent state?
- Are all state changes atomic?
- Can partial failures corrupt data?

Red flags:
- Multiple state changes without rollback
- Shared objects without proper locking
```

### 4. 经济漏洞（利用系统漏洞进行攻击）
```
Questions to ask:
- Can someone extract more value than deposited?
- Are there rounding errors that can be exploited?
- Flash loan attack vectors?

Red flags:
- Price calculations without slippage protection
- Unbounded loops over user-controlled data
```

### 5. 拒绝服务攻击（DoS）
```
Questions to ask:
- Can someone block legitimate users?
- Are there unbounded operations?
- Can storage be filled maliciously?

Red flags:
- Vectors that grow unbounded
- Loops over external data
```

### 安全报告模板

在分析模块时，生成一份安全报告：

```markdown
## Security Analysis: <module_name>

### Summary
- Risk Level: [Low/Medium/High/Critical]
- Issues Found: X

### Findings

#### [SEVERITY] Issue Title
- **Location:** Line XX
- **Description:** What the issue is
- **Impact:** What could happen
- **Recommendation:** How to fix

### Tested Edge Cases
- [ ] Overflow at max values
- [ ] Underflow at zero
- [ ] Unauthorized access attempts
- [ ] Empty/null inputs
- [ ] Reentrancy scenarios
```

### 示例：具备安全意识的测试用例

```move
// SECURITY: Testing that non-owner cannot withdraw
#[test]
#[expected_failure(abort_code = ENotOwner)]
fun test_unauthorized_withdraw() {
    // Setup: Create vault owned by ALICE
    // Action: BOB tries to withdraw
    // Expected: Should fail with ENotOwner
}

// SECURITY: Testing overflow protection
#[test]
fun test_deposit_overflow_protection() {
    // Deposit near u64::MAX
    // Verify no overflow occurs
}

// SECURITY: Testing economic invariant
#[test]
fun test_total_supply_invariant() {
    // After any operations:
    // sum(all_balances) == total_supply
}
```

---

## 全面包含安全性的工作流程

```bash
# 1. Coverage analysis
sui move test --coverage --trace
python3 $SKILL_DIR/analyze_source.py -m <module> -o coverage.md

# 2. While writing tests, document security findings
# Create SECURITY.md alongside coverage.md

# 3. After tests pass, summarize:
# - Coverage: X% → 100%
# - Security issues found: N
# - Recommendations: ...
```

---

## 相关技能

本技能属于Sui开发技能套件的一部分：

| 技能 | 描述 |
|-------|-------------|
| [sui-decompile](https://clawhub.ai/EasonC13/sui-decompile) | 获取并阅读链上合约的源代码 |
| [sui-move](https://clawhub.ai/EasonC13/sui-move) | 编写和部署Move智能合约 |
| **sui-coverage** | 通过安全分析来评估测试覆盖率 |
| [sui-agent-wallet](https://clawhub.ai/EasonC13/sui-agent-wallet) | 构建和测试DApp的前端界面 |

**整体工作流程：**
```
sui-decompile → sui-move → sui-coverage → sui-agent-wallet
    Study        Write      Test & Audit   Build DApps
```

所有技能的完整列表请参见：<https://github.com/EasonC13-agent/sui-skills>