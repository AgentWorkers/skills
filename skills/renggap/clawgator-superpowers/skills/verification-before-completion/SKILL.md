---
name: verification-before-completion
description: **使用场景：**  
在声称工作已完成、问题已修复或达到预期标准之前使用。在提交代码或创建 Pull Request（PR）之前，需要先运行验证命令并确认验证结果；任何关于工作成功的声明都必须有相应的证据支持。
---

# 完成前的验证

## 概述

在没有进行验证的情况下就声称工作已经完成，既不诚实也不高效。

**核心原则：** 在提出任何主张之前，必须先有证据。

**违反这一规则的字面意义，就等于违背了其精神。**

## 铁律

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

如果你还没有运行验证命令，那么你就不能声称工作已经通过验证。

## 验证流程

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## 常见的问题

| 主张内容 | 所需验证的内容 | 缺乏的验证内容 |
|---------|----------------|----------------|
| 测试通过 | 测试命令的输出：无错误 | 之前的测试结果（应显示“通过”） |
| 代码检查通过 | 代码检查工具的输出：无错误 | 仅进行了部分检查 |
| 构建成功 | 构建命令的退出状态为0 | 代码检查通过，日志显示正常 |
| 问题已修复 | 原始问题已解决 | 代码可能已被修改 |
| 回归测试通过 | 回归测试已完成 | 测试仅通过了一次 |
| 代理任务完成 | 版本控制系统（VCS）显示代码有更改 | 代理任务报告“成功” |
| 需求已满足 | 需求列表中的每一项都得到满足 | 所有测试都通过 |

## 危险信号（请立即停止）：

- 使用“应该”、“可能”、“似乎”等不确定的词语
- 在验证之前就表示满意（如“太棒了！”、“完美了！”、“完成了！”等）
- 即将提交代码、推送更改或创建拉取请求（PR）而未进行验证
- 相信代理任务的完成报告
- 仅依赖部分验证结果
- 认为“就这一次可以省略验证”
- 因疲劳而想快速完成工作
- **任何暗示工作已经完成但未进行验证的表述**

## 防止错误思维的方式

| 常见借口 | 真实情况 |
|---------|---------|
| “现在应该可以正常使用了” | 请运行验证命令 |
| “我有信心” | 信心≠证据 |
| “就这一次可以省略验证” | 没有例外情况 |
| “代码检查通过了” | 代码检查工具≠编译器 |
| “代理任务报告成功了” | 请独立验证结果 |
| “我累了” | 疲劳≠借口 |
| “部分检查就足够了” | 部分检查无法证明全部问题 |
| “用不同的词语表达，所以规则不适用” | 重要的是规则的精神，而非字面意思 |

## 关键验证步骤

**测试：**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**回归测试（测试驱动开发中的红绿循环）：**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**构建过程：**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**需求验证：**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**代理任务的验证：**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## 为什么这很重要

根据过去的24次失败案例来看：
- 如果你的团队成员不相信你的说法，信任就会破裂；
- 如果未定义的功能被发布到产品中，可能会导致程序崩溃；
- 如果遗漏了某些需求，功能将不完整；
- 如果在未完成验证的情况下就认为工作完成，会浪费时间，最终需要重新修改；
- 这违背了“诚实是核心价值观”的原则；如果你撒谎，最终会被替换。

## 何时需要执行验证

**在任何情况下都必须执行验证：**
- 在提出任何关于工作完成或成功的声明之前；
- 在表示满意之前；
- 在提交代码、创建拉取请求或完成任务之前；
- 在开始下一个任务之前；
- 在将任务委托给代理工具之前。

**该规则适用于：**
- 所有的明确表述；
- 所有的同义替换或意译表达；
- 任何暗示工作已完成或正确的表述；
- 任何可能暗示工作完成或正确的沟通内容。

## 总结

**验证工作没有捷径可走。**

请先运行验证命令，仔细阅读输出结果，然后再声称工作已经完成。

这是不可商量的。