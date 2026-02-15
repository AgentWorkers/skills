---
name: ralph-opencode-free-loop
description: 使用 OpenCode Zen 运行一个自主的 Open Ralph Wiggum 编码循环，该循环支持免费模型和自动回退机制。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔁",
        "homepage": "https://github.com/Th0rgal/open-ralph-wiggum",
        "requires": { "bins": ["opencode", "ralph", "git"] },
      },
  }
user-invocable: true
---

## 该技能的功能

该技能使用 `ralph` CLI 和 OpenCode 作为代理提供者，来运行一个自动化的编码循环。它会不断重复执行相同的编码指令，直到满足以下条件之一：

- 达到成功标准；
- 输出完成提示；
- 达到最大迭代次数。

该循环针对 **免费的 OpenCode Zen 模型** 进行了优化，并且包含了一个回退机制，以应对模型被限制使用、禁用或移除的情况。

---

## 适用场景

当你需要自动执行编码任务时，可以使用该技能，例如：

- 修复失败的测试；
- 实现新的功能；
- 重构代码库；
- 解决代码中的 lint 或类型错误；
- 运行构建和修复循环；
- 进行多轮迭代调试。

在运行 Ralph 之前，你必须确保自己处于一个 Git 仓库中。

---

## 免费模型的使用顺序

请始终按照以下顺序尝试使用免费模型：

1. `opencode/kimi-k2.5-free` ← 最佳的编码性能（限时免费）
2. `opencode/minimax-m2.1-free`
3. `opencode/glm-4.7-free`
4. `opencode/big-pickle` ← 免费的备用模型

如果某个模型因可用性或配额问题而无法使用，请立即尝试下一个模型，无需更改指令或循环参数。

### 回退触发条件

在遇到以下错误时，系统会自动回退：

- 模型被禁用；
- 模型找不到；
- 配额不足；
- 配额超出；
- 需要付费；
- 模型使用受到限制；
- 代理服务不可用。

---

## 运行循环的方法

### 第一次尝试（主要模型）

运行命令：

```bash
ralph "<任务指令>"
```

成功标准：

- 所有可验证的检查都通过；
- 构建成功；
- 测试通过。

完成提示：

```bash
<promise>已完成</promise>
```

```bash
--agent opencode \
--model opencode/kimi-k2.5-free \
--completion-promise "已完成" \
--max-iterations 20
```

---

### 第二次尝试（回退）

如果第一次尝试因模型问题失败，则尝试使用：

```bash
--model opencode/minimax-m2.1-free
```

---

### 第三次尝试（回退）

如果第二次尝试仍然失败，则尝试使用：

```bash
--model opencode/glm-4.7-free
```

---

### 第四次尝试（最终回退）

如果第三次尝试仍然失败，则尝试使用：

```bash
--model opencode/big-pickle
```

---

## 多步骤任务（适用于大型项目）

对于需要多个步骤的任务，运行命令：

```bash
ralph "<大型任务指令>"
```

```bash
--agent opencode \
--model opencode/kimi-k2.5-free \
--tasks \
--max-iterations 50
```

在这种情况下，免费模型的使用顺序仍然适用。

---

## 插件问题排查

如果 OpenCode 的插件干扰了循环的执行，可以尝试运行命令：

```bash
--no-plugins
```

---

## 检查可用 Zen 模型

如果免费模型的可用性发生变化，请访问：

https://opencode.ai/zen/v1/models

并根据需要更新回退模型顺序。

---

## 安全注意事项

- 请务必在 Git 仓库中运行该技能；
- 设置迭代次数上限，以防止循环无限运行；
- 确保指令中包含可验证的成功标准；
- 在合并自动生成的代码更改之前，请先审查差异。

---

## 使用示例

修复 TypeScript 中的错误：

```bash
ralph "修复仓库中的所有 TypeScript 错误。"
```

成功标准：

- `tsc` 命令执行成功；
- 构建过程成功。

完成提示：

```bash
<promise>已完成</promise>
```

```bash
--agent opencode \
--model opencode/kimi-k2.5-free \
--completion-promise "已完成" \
--max-iterations 20
```