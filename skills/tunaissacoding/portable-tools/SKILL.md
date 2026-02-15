---
name: portable-tools
description: 构建跨设备工具时，无需硬编码路径或账户名称。
---

# 便携式工具 - 跨设备开发方法论

这是一种用于构建可在不同设备、命名方案和配置下运行的工具的开发方法论。该方法论基于2026年1月23日的OAuth复习调试会议的经验总结。

## 核心原则

**永远不要假设你的设备是唯一的设备。**

你的本地设置只是众多可能配置中的一种。应为通用情况而非特定实例进行开发。

---

## 编写代码前的三个问题

### 1. “设备之间有哪些差异？”

在编写任何读取配置、数据或凭据的代码之前，需要考虑以下问题：

- **文件路径**：（macOS与Linux，不同的用户目录）
- **账户名称**：（user123 vs default vs oauth）
- **服务名称**：（拼写或大小写上的细微差异）
- **数据结构**：（不同版本，不同格式）
- **环境**：（不同的shell，可用的工具不同）

**来自OAuth复习的例子：**
- ❌ 错误假设：账户名称始终为“claude”
- ✅ 正确做法：账户名称可以是“claude”、“Claude Code”、“default”等

**行动：**列出所有可能变化的变量，并使其可配置或自动检测。

---

### 2. “我如何证明这个工具能够正常工作？”

在声称工具成功之前，需要满足以下条件：

- **明确工具使用前的状态**（具体数值）
- **明确工具使用后的状态**（具体数值）
- **证明状态变化**（通过对比验证）

**来自OAuth复习的例子：**
```
BEFORE:
- Access Token: POp5z1fi...eSN9VAAA
- Expires: 1769189639000

AFTER:
- Access Token: 01v0RrFG...eOE9QAA ✅ Different
- Expires: 1769190268000 ✅ Extended
```

**行动：**始终使用实际数据来展示工具的工作过程。

---

### 3. **当工具出问题时会发生什么？**

在将工具推送到生产环境之前，需要进行以下测试：

- **故意设置错误的配置**  
- **缺少数据**  
- **存在多个条目**  
- **边缘情况**（空值、特殊字符）

**来自OAuth复习的例子：**
- 测试`keychain_account`为“wrong-name”时的行为 → 应该有回退机制
- 测试keychain数据不完整时的行为 → 应该优雅地失败并给出有用的错误信息

**行动：**不仅要测试正常工作的情况，还要测试各种异常情况。

---

## 强制性开发模式

### 模式1：明确而非隐含

**❌ 错误做法：**
```bash
# Ambiguous - returns first match
security find-generic-password -s "Service" -w
```

**✅ 正确做法：**
```bash
# Explicit - returns specific entry
security find-generic-password -s "Service" -a "account" -w
```

**规则：**如果命令存在歧义，必须明确其含义。

---

### 模式2：使用前进行验证

**❌ 错误做法：**
```bash
DATA=$(read_config)
USE_VALUE="$DATA"  # Hope it's valid
```

**✅ 正确做法：**
```bash
DATA=$(read_config)
if ! validate_structure "$DATA"; then
    error "Invalid data structure"
fi
USE_VALUE="$DATA"
```

**规则：**永远不要假设数据具有预期的结构。

---

### 模式3：提供回退机制

**❌ 错误做法：**
```bash
ACCOUNT="claude"  # Hardcoded
```

**✅ 正确做法：**
```bash
# Try configured → Try common → Error with help
ACCOUNT="${CONFIG_ACCOUNT}"
if ! has_data "$ACCOUNT"; then
    for fallback in "claude" "default" "oauth"; do
        if has_data "$fallback"; then
            ACCOUNT="$fallback"
            break
        fi
    done
fi
[[ -z "$ACCOUNT" ]] && error "No account found. Tried: ..."
```

**规则：**为常见的配置差异提供自动回退方案。

---

### 模式4：提供有用的错误信息

**❌ 错误做法：**
```bash
[[ -z "$TOKEN" ]] && error "No token"
```

**✅ 正确做法：**
```bash
[[ -z "$TOKEN" ]] && error "No token found

Checked:
- Config: $CONFIG_FILE
- Field: $FIELD_NAME
- Expected: { \"tokens\": { \"refresh\": \"...\" } }

Verify with:
  cat $CONFIG_FILE | jq '.tokens'
"
```

**规则：**错误信息应帮助用户诊断问题并进行修复。

---

## 调试方法论（Patrick的方法）

### 第一步：获取准确的数据

**不要问：“工具是否出故障了？”**  
**应该问：“你看到了哪些具体的数值？有多少条记录？哪条记录包含了数据？”**

**示例：**
```bash
# Vague
"Check keychain"

# Specific
"Run: security find-generic-password -l 'Service' | grep 'acct'"
"Tell me: 1. How many entries 2. Which has tokens 3. Last modified"
```

---

### 第二步：用具体示例进行验证

**不要说：“现在应该能正常工作了。”**  
**应该展示：**“这是使用前的状态（POp5z...），这是使用后的状态（01v0R...），两者不同。”

**模板：**
```
BEFORE:
- Field1: <exact_value>
- Field2: <exact_value>

AFTER:
- Field1: <new_value> ✅ Changed
- Field2: <new_value> ✅ Changed

PROOF: Values are different
```

---

### 第三步：立即考虑跨设备的情况

**不要想：“在我的机器上可以正常工作。”**  
**应该想：“如果其他设备的配置不同会怎样？”**

**检查清单：**
- [ ] 账户名称是否不同？
- [ ] 文件路径是否不同？
- [ ] 使用的工具或版本是否不同？
- [ ] 权限是否不同？
- [ ] 数据格式是否不同？

---

## 发布前的准备清单

### 发现阶段
- [ ] 列出所有外部依赖项（文件、命令、服务）
- [ ] 记录每个依赖项的功能
- [ ] 确定哪些部分可能在不同设备间存在差异

### 实现阶段
- [ ] 使配置选项可配置（并提供合理的默认值）
- [ ] 为每个输入添加验证机制
- [ ] 为常见配置差异提供回退方案
- [ ] 添加`--dry-run`或`--test`模式

### 测试阶段
- [ ] 使用正确的配置进行测试 → 工具应能正常工作
- [ ] 使用错误的配置进行测试 → 工具应能回退或优雅地失败
- [ ] 测试数据缺失的情况 → 应给出有用的错误信息
- [ ] 测试存在多个条目的情况 → 应能正确处理歧义

### 文档阶段
- [ ] 记录默认的假设条件
- [ ] 记录如何验证本地配置
- [ ] 记录常见的配置差异及处理方法
- [ ] 添加数据流图
- [ ] 添加故障排除指南

---

## 实际案例：OAuth复习

### 原始版本（存在问题）
```bash
# Assumes single entry, no validation, no fallback
KEYCHAIN_DATA=$(security find-generic-password -s "Service" -w)
REFRESH_TOKEN=$(echo "$KEYCHAIN_DATA" | jq -r '.refreshToken')
# Use token (hope it's valid)
```

**问题：**
- 返回第一个按字母顺序匹配的条目（错误）
- 无数据验证（可能导致空值或格式错误）
- 无回退机制（账户名称不同时会导致失败）

### 修复后的版本（具备便携性）
```bash
# Explicit account with validation and fallback
validate_data() {
    echo "$1" | jq -e '.claudeAiOauth.refreshToken' > /dev/null 2>&1
}

# Try configured account
DATA=$(security find-generic-password -s "$SERVICE" -a "$ACCOUNT" -w 2>&1)
if validate_data "$DATA"; then
    log "✓ Using account: $ACCOUNT"
else
    log "⚠ Trying fallback accounts..."
    for fallback in "claude" "Claude Code" "default"; do
        DATA=$(security find-generic-password -s "$SERVICE" -a "$fallback" -w 2>&1)
        if validate_data "$DATA"; then
            ACCOUNT="$fallback"
            log "✓ Found data in: $fallback"
            break
        fi
    done
fi

[[ -z "$DATA" ]] || ! validate_data "$DATA" && error "No valid data found
Tried accounts: $ACCOUNT, claude, Claude Code, default
Verify with: security find-generic-password -l '$SERVICE'"

REFRESH_TOKEN=$(echo "$DATA" | jq -r '.claudeAiOauth.refreshToken')
```

**改进措施：**
- ✅ 明确指定账户参数
- ✅ 验证数据结构
- ✅ 为常见账户名称提供自动回退机制
- ✅ 提供有用的错误信息以辅助验证

---

## 常见的错误做法

### 错误做法1： “在我的机器上可以正常工作”

**修复方法：**使用`$HOME`变量，检测操作系统类型，或使配置参数可配置

---

### 错误做法2： “希望一切都能按预期运行”

**修复方法：**在使用前进行数据验证

---

### 错误做法3： “第一个匹配的条目就是正确的”

**修复方法：**明确指定所需的数据，或列出所有可能的选项

---

### 错误做法4： **故障时没有反馈**

**修复方法：**在出现故障时提供详细的错误信息

---

## 与现有工作流程的集成

### 与`sprint-plan.md`的集成
**在测试部分添加相关内容：**
```markdown
## Cross-Device Testing
- [ ] Test with different account names
- [ ] Test with wrong config values
- [ ] Test with missing data
- [ ] Document fallback behavior
```

### 与`PRIVACY-CHECKLIST.md`的集成
**在发布前添加以下内容：**
```markdown
## Portability Check
- [ ] No hardcoded paths (use $HOME, detect OS)
- [ ] No hardcoded names (use config or fallback)
- [ ] Validation on all inputs
- [ ] Helpful errors for common issues
```

### 在创建新技能时：
1. 列出设备之间的差异
2. 使配置参数可配置或自动检测
3. 使用错误的配置进行测试
4. 编写故障排除指南

---

## 快速参考卡

**编写代码前：**
1. 设备之间有哪些差异？
2. 如何证明工具能够正常工作？
3. 工具出问题时会发生什么？

**强制性的开发模式：**
- 明确而非隐含的配置方式
- 使用前进行数据验证
- 提供回退机制
- 提供有用的错误信息

**测试阶段：**
- 使用正确的配置 → 工具应能正常工作
- 使用错误的配置 → 工具应能回退或给出有用的错误信息
- 数据缺失 → 提供清晰的故障诊断信息

**文档阶段：**
- 数据流图
- 常见的配置差异及处理方法
- 故障排除指南

---

## 成功标准

一个工具被认为是**便携式的**，当它满足以下条件时：

1. **在不同设备上无需修改即可正常工作**
2. **能自动识别常见的配置差异**
3. **在出现故障时能优雅地失败，并提供可操作的错误信息**
4. **通过查看错误输出即可进行调试**
5. **文档中涵盖了“如果我的配置不同会怎样”的情况**

**测试方法：**将工具交给使用不同配置的人进行测试。如果他们需要询问你问题，说明该工具还不够便携。

---

## 方法论的起源

这一方法论源于2026年1月23日的OAuth复习调试会议：
- 脚本错误地读取了keychain中的数据（未指定账户）
- 假设只存在一个账户条目（实际上存在多个）
- 未进行数据验证（导致使用空数据）
- 无回退机制（导致账户名称不同时程序失败）

Patrick的做法是：
- 要求提供准确的数据（条目数量、包含令牌的条目）
- 要求提供使用前后的数据对比
- 考虑到不同设备之间的配置差异

**关键启示：**问题并不出在代码逻辑上，而在于开发者的假设。

---

## 适用场景

**适用于以下情况：**
- 构建读取系统配置的工具
- 处理keychain、凭据和环境变量
- 创建可在多台机器上运行的脚本
- 将技能发布到ClawdHub（供他人使用）

**实施步骤：**
1. 在实现之前回答上述三个问题
2. 在实现过程中遵循强制性的开发模式
3. 在测试之前执行准备清单中的步骤
4. 测试完成后记录配置差异和故障排除方法

**记住：**你的设备只是众多可能情况中的一种。应为通用情况进行开发。