---
name: clean-code
model: standard
category: testing
description: 实用的编码规范，用于编写清晰、易于维护的代码——包括命名规则、函数设计、代码结构、常见错误模式（反模式）以及代码编写前的安全检查机制。这些规范适用于新代码的编写、现有代码的重构、代码质量的审查，以及编码标准的建立。
version: 2.0
---

# 清晰的代码

> 代码应当**简洁、直接且以解决问题为核心**。优秀的代码就像写得很好的散文一样：每个变量名都清晰地表达了其用途，每个函数都只完成一项任务，每个抽象层都恰到好处。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install clean-code
```

---

## 核心原则

| 原则 | 规则 | 实际测试 |
|-----------|------|----------------|
| **SRP**（单一职责原则） | 每个函数/类只完成一项任务 | “我能否不使用‘and’来描述这个函数的功能？” |
| **DRY**（避免重复） | 避免重复代码，重用已有逻辑 | “我之前写过类似的代码吗？” |
| **KISS**（保持简单） | 选择最简单且有效的解决方案 | “有没有更简单的方法来实现这个功能？” |
| **YAGNI**（不要过早添加功能） | 不要添加目前不需要的功能 | “现在有人需要这个功能吗？” |
| **Boy Scout**（事后维护） | 使代码比你编写时更整洁 | “我的修改后，代码是否变得更清晰了？” |

---

## 命名规则

良好的命名是代码最重要的文档。一个恰当的名称可以省去注释的必要。

| 元素 | 命名规范 | 不良命名 | 良好命名 |
|---------|------------|-----|------|
| **变量** | 明确表达用途 | `n`, `d`, `tmp` | `userCount`, `elapsed`, `activeUsers` |
| **函数** | 动词 + 名词 | `user()`, `calc()` | `getUserById()`, `calculateTotal()` |
| **布尔值** | 使用疑问句形式 | `active`, `flag` | `isActive`, `hasPermission`, `canEdit` |
| **常量** | 使用大写命名 | `max`, `timeout` | `MAX_RETRY_COUNT`, `REQUEST_TIMEOUT_MS` |
| **类** | 使用单数名词 | `Manager`, `Data` | `UserRepository`, `OrderService` |
| **枚举** | 使用PascalCase命名法 | `'pending'` | `Status.Pending` |

> **规则：** 如果某个名称需要注释来解释其含义，那就重新命名它。

### 命名反模式

| 反模式 | 问题 | 解决方案 |
|--------------|---------|-----|
| 难以理解的缩写（如 `usrMgr`, `cfg`） | 六个月后就无法阅读 | 直接写出完整的名称；IDE的自动补全功能可以辅助长名称的输入 |
| 通用名称（如 `data`, `info`, `item`, `handler`） | 无法体现代码的用途 | 使用与领域相关的具体名称 |
| 名称与实际功能不符（例如 `getUserList` 实际上只返回一个用户） | 会误导读者 | 确保名称与功能一致，或者修改代码以实现预期的行为 |
| 匈牙利命名法（如 `strName`, `nCount`, `IUser`） | 类型信息已由类型系统提供 | 使用类型系统来显示类型；名称应描述功能 |

---

## 函数规则

| 规则 | 指导原则 | 原因 |
|------|-----------|-----|
| **简洁性** | 函数长度不超过20行，理想情况下为5-10行 | 便于记忆和理解 |
| **单一功能** | 每个函数只完成一项任务 | 便于测试和命名 |
| **单一抽象层次** | 每个函数只包含一个抽象层次 | 代码从上到下易于阅读 |
| **参数数量** | 最多3个参数，最好为0-2个 | 便于正确调用 |
| **无副作用** | 不要意外修改输入参数 | 行为应可预测 |

### 保护性条件语句

使用提前返回来简化嵌套的条件判断。避免超过两层嵌套。

```typescript
// BAD — 5 levels deep
function processOrder(order: Order) {
  if (order) {
    if (order.items.length > 0) {
      if (order.customer) {
        if (order.customer.isVerified) {
          return submitOrder(order);
        }
      }
    }
  }
  throw new Error('Invalid order');
}

// GOOD — guard clauses flatten the structure
function processOrder(order: Order) {
  if (!order) throw new Error('No order');
  if (!order.items.length) throw new Error('No items');
  if (!order.customer) throw new Error('No customer');
  if (!order.customer.isVerified) throw new Error('Customer not verified');

  return submitOrder(order);
}
```

### 参数对象

当一个函数需要超过3个参数时，可以使用参数对象来传递这些参数。

```typescript
// BAD — too many parameters, order matters
createUser('John', 'Doe', 'john@example.com', 'secret', 'admin', 'Engineering');

// GOOD — self-documenting options object
createUser({
  firstName: 'John',
  lastName: 'Doe',
  email: 'john@example.com',
  password: 'secret',
  role: 'admin',
  department: 'Engineering',
});
```

---

## 代码结构模式

| 模式 | 适用场景 | 好处 |
|---------|--------------|---------|
| **保护性条件语句** | 在函数开头处理特殊情况 | 使代码结构更扁平、更易阅读 |
| **扁平结构优于嵌套结构** | 当嵌套层次超过2层时 | 减轻认知负担 |
| **组合式设计** | 复杂操作 | 将代码拆分为更小、更易测试的部分 |
| **相关代码的集中放置** | 将相关代码放在同一个文件中 | 更便于查找和修改 |
| **提取函数** | 使用注释分隔代码的不同部分 | 使代码具有自文档化功能 |

### 组合式设计优于“万能函数”

```typescript
// BAD — god function doing everything
async function processOrder(order: Order) {
  // Validate... (15 lines)
  // Calculate totals... (15 lines)
  // Process payment... (10 lines)
  // Send notifications... (10 lines)
  // Update inventory... (10 lines)
  return { success: true };
}

// GOOD — composed of small, focused functions
async function processOrder(order: Order) {
  validateOrder(order);
  const totals = calculateOrderTotals(order);
  const payment = await processPayment(order.customer, totals);
  await sendOrderConfirmation(order, payment);
  await updateInventory(order.items);
  return { success: true, orderId: payment.orderId };
}
```

## 返回类型的一致性

函数应返回一致的返回类型。对于多种可能的返回结果，可以使用枚举类型（discriminated unions）。

```typescript
// BAD — returns different types
function getUser(id: string) {
  const user = database.find(id);
  if (!user) return false;     // boolean
  if (user.isDeleted) return null; // null
  return user;                 // User
}

// GOOD — discriminated union
type GetUserResult =
  | { status: 'found'; user: User }
  | { status: 'not_found' }
  | { status: 'deleted' };

function getUser(id: string): GetUserResult {
  const user = database.find(id);
  if (!user) return { status: 'not_found' };
  if (user.isDeleted) return { status: 'deleted' };
  return { status: 'found', user };
}
```

---

## 常见错误及解决方法

| 错误类型 | 问题 | 解决方案 |
|--------------|---------|-----|
| 每行都加注释 | 过多的注释会掩盖代码的逻辑 | 删除不必要的注释；只注释代码的逻辑原因 |
| 为单行代码编写辅助函数 | 不必要的间接调用 | 将代码直接内联 |
| 为两个对象创建单独的工厂函数 | 过度设计 | 直接创建对象 |
| `utils.ts` 文件中只包含一个函数 | 无用的工具文件 | 将代码放在实际使用的位置 |
| 深层嵌套 | 代码结构难以理解 | 使用保护性条件语句和提前返回 |
| 使用“魔法数字” | 代码含义不明确 | 使用有意义的常量来替代 |
| “万能函数” | 代码难以测试和阅读 | 根据功能将代码拆分为更小的部分 |
| 被注释掉的代码 | 会导致混淆 | 删除这些代码；版本控制系统会记录代码的变更历史 |
| 未完成的待办事项堆积如山 | 任务永远无法完成 | 将待办事项记录在问题跟踪系统中，而不是代码中 |
| 过早进行抽象 | 不恰当的抽象反而会降低代码的可读性和可维护性 | 等待出现3个或更多重复的情况后再进行抽象 |
| 代码复制粘贴 | 会导致代码重复和错误 | 提取共用的逻辑 |
| 依赖异常来控制流程 | 代码运行缓慢且难以理解 | 使用明确的条件判断 |
| 严格类型化的代码 | 容易出现类型错误 | 使用枚举或联合类型 |
| 复杂的回调链 | 代码结构混乱 | 使用`async/await`来简化流程 |

## 修改前的安全检查

在修改任何文件之前，回答以下问题以避免引发连锁故障：

| 问题 | 原因 |
|----------|-----|
| **这个文件依赖于哪些文件？** | 修改接口可能会导致依赖文件出错 |
| **这个文件又依赖于哪些文件？** | 可能需要更新这些文件的接口或代码 |
| **有哪些测试覆盖了这个文件？** | 修改后可能需要重新运行相关测试 |
| **这是一个共享组件吗？** | 如果被多个模块使用，修改可能会影响更多地方 |

```
File to edit: UserService.ts
├── Who imports this? → UserController.ts, AuthController.ts
├── Do they need changes too? → Check function signatures
└── What tests cover this? → UserService.test.ts
```

> **规则：** 在修改一个文件时，同时修改所有依赖该文件的文件。切勿留下未修复的依赖关系或遗漏的更新。

---

## 完成前的自我检查

在标记任务完成之前，验证以下内容：

| 检查项 | 问题 |
|-------|----------|
| **目标是否达成？** | 我是否完成了任务要求的所有内容？ |
| **是否修改了所有相关文件？** | 是否修改了所有必要的文件，包括依赖文件？ |
| **代码是否能正常运行？** | 修改后的代码能否编译并通过测试？ |
| **是否有错误？** | 代码是否通过了代码检查工具（如lint和类型检查）？ |
| **有没有遗漏什么？** | 是否有遗漏的特殊情况或依赖文件？ |

---

## 绝对不要做的事情

1. **绝不要添加重复解释代码的注释**——如果代码本身需要注释来说明其功能，那就重新命名相关变量或函数。
2. **绝不要为少于3种使用场景创建抽象层**——过早的抽象反而会降低代码的可读性和可维护性。
3. **绝不要在代码库中保留被注释掉的代码**——版本控制系统可以记录代码的历史变更。
4. **绝不要编写超过20行的函数**——如果一个函数的功能可以拆分为多个小函数，就应该拆分它们。
5. **绝不要使用超过两层的嵌套结构**——使用保护性条件语句、提前返回或提取函数来避免复杂结构。
6. **绝不要使用“魔法数字”**——使用有明确含义的常量来替代。
7. **在修改代码之前，绝不要不检查其依赖关系**——未修复的依赖关系和遗漏的更新是多文件修改中最常见的错误来源。
8. **绝不要在未修复错误的情况下标记任务为完成**——在修复所有问题后再标记任务为完成。

---

## 参考资料

关于清晰代码的详细指南：

| 参考资料 | 说明 |
|-----------|-------------|
| [反模式](references/anti-patterns.md) | 21种常见的代码错误及相应的良好/不良代码示例，涵盖命名、函数设计、代码结构和注释等方面 |
| [代码异味](references/code-smells.md) | 经典的代码异味列表，包括代码臃肿、滥用面向对象设计、难以维护的代码结构等问题 |
| [重构指南](references/refactoring-catalog.md) | 必备的重构模式，包含重构前的代码示例和具体步骤 |