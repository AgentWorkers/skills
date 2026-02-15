---
name: evaluate-presets
description: **使用场景：**  
在测试 Ralph 的帽子收藏预设时，验证预设配置的有效性；或在审计预设库时检查是否存在漏洞及用户体验（UX）方面的问题。
---

# 评估预设配置

## 概述

使用 shell 脚本系统地测试所有预设配置。直接通过 CLI 调用脚本进行测试，无需复杂的元编排。

## 使用场景

- 在对预设配置进行修改后进行测试
- 审查预设库的质量
- 验证新预设配置是否正常工作
- 在修改帽子路由逻辑后进行测试

## 快速入门

**评估单个预设配置：**
```bash
./tools/evaluate-preset.sh tdd-red-green claude
```

**评估所有预设配置：**
```bash
./tools/evaluate-all-presets.sh claude
```

**参数说明：**
- 第一个参数：预设名称（不包含 `.yml` 扩展名）
- 第二个参数：后端服务（`claude` 或 `kiro`，默认为 `claude`）

## Bash 工具配置

**重要提示：** 通过 Bash 工具调用这些脚本时，请使用以下配置：
- **评估单个预设配置：** 设置 `timeout: 600000`（最长 10 分钟）和 `run_in_background: true`
- **评估所有预设配置：** 设置 `timeout: 600000`（最长 10 分钟）和 `run_in_background: true`

由于预设配置的评估可能需要较长时间（尤其是全套测试），**请务必在后台运行** 并使用 `TaskOutput` 工具定期检查进度。

**示例调用方式：**
```
Bash tool with:
  command: "./tools/evaluate-preset.sh tdd-red-green claude"
  timeout: 600000
  run_in_background: true
```

启动脚本后，可以使用 `TaskOutput`（设置 `block: false`）来查看测试状态，无需等待测试完成。

## 脚本的功能

### `evaluate-preset.sh`

1. 从 `tools/preset-test-tasks.yml` 文件中加载测试任务（如果安装了 `yq` 工具）
2. 创建包含评估设置的合并配置文件
3. 使用 `--record-session` 选项运行 Ralph 脚本以捕获测试数据
4. 收集输出日志、退出代码和执行时间
5. 提取测试指标：迭代次数、激活的帽子数量、发布的事件数量

**输出结构：**
```
.eval/
├── logs/<preset>/<timestamp>/
│   ├── output.log          # Full stdout/stderr
│   ├── session.jsonl       # Recorded session
│   ├── metrics.json        # Extracted metrics
│   ├── environment.json    # Runtime environment
│   └── merged-config.yml   # Config used
└── logs/<preset>/latest -> <timestamp>
```

### `evaluate-all-presets.sh`

依次运行所有 12 个预设配置，并生成测试总结：
```
.eval/results/<suite-id>/
├── SUMMARY.md              # Markdown report
├── <preset>.json           # Per-preset metrics
└── latest -> <suite-id>
```

## 正在评估的预设配置

| 预设名称 | 测试任务 |
|--------|-----------|
| `tdd-red-green` | 添加 `is_palindrome()` 函数 |
| `adversarial-review` | 审查用户输入处理逻辑的安全性 |
| `socratic-learning` | 理解 `HatRegistry` 的工作原理 |
| `spec-driven` | 明确指定并实现 `StringUtils::truncate()` 函数 |
| `mob-programming` | 实现 `Stack` 数据结构 |
| `scientific-method` | 调试失败的模拟测试断言 |
| `code-archaeology` | 分析 `config.rs` 的代码历史 |
| `performance-optimization` | 分析帽子匹配的效率 |
| `api-design` | 设计 `Cache` 特性 |
| `documentation-first` | 文档化 `RateLimiter` 的实现 |
| `incident-response` | 处理持续集成（CI）中出现的测试失败问题 |
| `migration-safety` | 规划从版本 1 到版本 2 的配置迁移 |

## 解释测试结果

**`evaluate-preset.sh` 的退出代码：**
- `0` — 测试成功（完成所有测试循环）
- `124` — 超时（预设配置运行异常或耗时过长）
- 其他代码 — 测试失败（请查看 `output.log` 文件）

**`metrics.json` 文件中的测试指标：**
- `iterations` — 测试循环次数
- `hats_activated` — 被激活的帽子数量
- `events_published` — 发布的事件总数
- `completed` — 是否成功完成所有测试

## 帽子路由性能

**关键要求：** 确保每个帽子在每次测试中都能获得最新的上下文信息（遵循原则 #1：“最新的上下文是可靠性的保障”）。

### 合格的测试结果

每个预设配置应在**单独的测试循环** 中执行：
```
Iter 1: Ralph → publishes starting event → STOPS
Iter 2: Hat A → does work → publishes next event → STOPS
Iter 3: Hat B → does work → publishes next event → STOPS
Iter 4: Hat C → does work → LOOP_COMPLETE
```

### 需注意的问题（同一测试循环内多次切换帽子）

**问题现象：** 在同一测试循环内多次切换帽子：
```
Iter 2: Ralph does Blue Team + Red Team + Fixer work
        ^^^ All in one bloated context!
```

### 检查方法：

**1. 查看 `session.jsonl` 文件中的迭代次数和事件数量：**
```bash
# Count iterations
grep -c "_meta.loop_start\|ITERATION" .eval/logs/<preset>/latest/output.log

# Count events published
grep -c "bus.publish" .eval/logs/<preset>/latest/session.jsonl
```

**正常情况：** 迭代次数应接近事件数量（每次迭代对应一个事件）
**异常情况：** 迭代次数较少（2-3 次），但事件数量较多（所有事件都在同一循环内发生）

**2. 检查 `output.log` 文件中的帽子切换记录：**
```bash
grep -E "ITERATION|Now I need to perform|Let me put on|I'll switch to" \
    .eval/logs/<preset>/latest/output.log
```

**异常现象：** 在同一测试循环内多次切换帽子，且切换之间没有明显的分隔标志

**3. 检查 `session.jsonl` 文件中的事件时间戳：**
```bash
cat .eval/logs/<preset>/latest/session.jsonl | jq -r '.ts'
```

**异常现象：** 在同一测试循环内有多个事件具有相同的时间戳

### 路由性能问题的排查方法

| 问题类型 | 原因 | 应对措施 |
|---------|-----------|--------|
| 迭代次数与事件数量一致 | ✅ 测试正常 | 帽子路由功能正常 |
| 迭代次数远小于事件数量 | ⚠️ 同一循环内多次切换帽子 | 检查提示信息中是否包含停止指令 |
| 迭代次数远大于事件数量 | ⚠️ 代理未正确发布事件 | 检查代理是否正常工作 |
| 无事件记录 | ❌ 系统故障 | 无法从 JSONL 文件中读取事件数据 |

### 故障排查步骤

如果帽子路由功能出现故障，请检查以下内容：

1. **检查 `hatless_ralph.rs` 文件中的工作流程提示：**
   - 是否有“CRITICAL: STOP after publishing”的提示？
   - `DELEGATE` 部分是否明确说明了控制权的移交方式？

2. **检查帽子指令的传递机制：**
   - `HatInfo` 对象是否包含 `instructions` 字段？
   - 指令是否在 `## HATS` 部分中正确显示？

3. **检查事件上下文：**
   - `build_prompt(context)` 函数是否使用了正确的上下文参数？
   | 提示信息中是否包含 `## PENDING EVENTS` 部分？`

## 自动修复流程

评估完成后，将修复任务分配给相应的代理：

### 第一步：结果分类

阅读 `.eval/results/latest/SUMMARY.md` 文件，识别问题类型：
- `❌ FAIL` — 需要编写代码修复问题
- `⏱️ TIMEOUT` — 检查是否存在无限循环
- `⚠️ PARTIAL` — 检查是否存在边缘情况

### 第二步：创建修复任务

针对每个问题，生成相应的修复任务：
```
"Use /code-task-generator to create a task for fixing: [issue from evaluation]
Output to: tasks/preset-fixes/"
```

### 第三步：执行修复任务

为每个生成的修复任务分配相应的代理执行：
```
"Use /code-assist to implement: tasks/preset-fixes/[task-file].code-task.md
Mode: auto"
```

### 第四步：重新评估

完成修复后，重新运行所有预设配置的测试：
```bash
./tools/evaluate-preset.sh <fixed-preset> claude
```

## 先决条件

- **yq**（可选）：用于从 YAML 文件中加载测试任务。安装方法：`brew install yq`
- **Cargo**：必须能够构建 Ralph 应用程序

## 相关文件

- `tools/evaluate-preset.sh` — 单个预设配置的评估脚本
- `tools/evaluate-all-presets.sh` — 全部预设配置的评估脚本
- `tools/preset-test-tasks.yml` — 测试任务定义文件
- `tools/preset-evaluation-findings.md` — 手动测试结果文档
- `presets/` — 被评估的预设配置集合