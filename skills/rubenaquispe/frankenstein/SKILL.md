---
name: frankenstein
version: 1.2.0
description: "将多个技能中的最佳部分整合成一个全新的技能。该技能会搜索 ClawHub、GitHub、skills.sh、skillsmp.com 以及其他 AI 技能仓库，安全地分析每个技能的功能和特点，然后从中挑选出最优秀的部分进行组合。在组合过程中，会使用 skill-auditor 进行安全扫描，并通过 sandwrap 工具对最终生成的技能进行进一步的安全性验证。适用场景包括：  
(1) 当存在多个用于相同目的的技能时；  
(2) 希望获得最优质的功能组合时；  
(3) 需要从多个技能片段中构建一个完整的、功能全面的技能时。"
---

# Frankenstein

## 模型要求

**默认模型：Opus（或当前可用的最佳思维模型）**

Frankenstein 需要具备深度的推理能力，以便：
- 比较多种技能方法；
- 识别方法论上的细微差异；
- 创造性地整合最佳部分；
- 发现他人可能忽略的安全性/质量问题。

只有在用户出于成本考虑明确要求的情况下，才使用较小的模型。整合的质量在很大程度上取决于推理的深度。

通过组合现有技能的最佳部分，可以创建新的技能。

## 快速入门

```
Frankenstein me an SEO audit skill
```

## 工作原理

### 第一步：搜索所有来源

在所有 AI 技能仓库中搜索匹配的技能：
**1. ClawHub（主要来源）**
```bash
clawhub search "[topic]" --registry "https://clawhub.ai"
```

**2. GitHub**
```
Search: "[topic] AI skill" OR "[topic] claude skill" OR "[topic] agent skill"
Look for: SKILL.md, CLAUDE.md, or similar agent instruction files
```

**3. skills.sh**
```
https://skills.sh/search?q=[topic]
```

**4. skillsmp.com（技能市场）**
```
https://skillsmp.com/search/[topic]
```

**5. 其他需要检查的来源：**
- Anthropic 的技能示例
- OpenAI GPT 的配置（转换为技能格式）
- LangChain 的代理模板
- AutoGPT/AgentGPT 的技能仓库

**在过滤之前收集所有候选技能。** 来源越丰富，生成的 Frankenstein 技能就越优秀。

### 第二步：安全扫描

使用 skill-auditor 对每个技能进行安全扫描。排除风险评分较高的技能。

对于每个找到的技能：
- 将其安装到临时目录中；
- 运行 skill-auditor 扫描；
- 评分 >= 7 = 安全（继续下一步）；
- 评分 < 7 = 有风险（警告后跳过）。

### 第三步：安全分析

以只读模式使用 sandwrap 对安全的技能进行分析。

对于每个安全的技能，提取以下信息：
- 核心功能（该技能的作用）；
- 方法论（解决问题的方式）；
- 脚本/工具（可重用的代码）；
- 独特的优势；
- 缺点。

### 第四步：比较

构建比较矩阵：

| 功能 | 技能A | 技能B | 技能C | 最优选择 |
|---------|---------|---------|---------|--------|
| 功能1 | 是 | 否 | 是 | A、C |
| 功能2 | 基础 | 高级 | 无 | B |
| 功能3 | 否 | 否 | 是 | C |

### 第五步：整合

为每个功能选择最优的实现方式：
- 功能1 的方法来自技能A；
- 功能2 的实现来自技能B；
- 功能3 的方法来自技能C。

### 第六步：构建初始草案

使用 skill-creator 来组装新的技能：
- 结合各个功能中的最优部分；
- 解决方法之间的冲突；
- 编写统一的 SKILL.md 文件；
- 包含来自最优技能的脚本；
- 记录技能的来源。

### 第七步：审核循环（关键步骤）

**执行 → 测试 → 优化，直到通过三次稳定测试：**

```
Pass 1:
  1. Read draft
  2. Try to break it (find holes, contradictions, gaps)
  3. Document issues
  4. Fix them
  
Pass 2:
  1. Read improved version
  2. Actively try to find MORE issues
  3. Fix any found
  
Pass 3+:
  Continue until you genuinely try to improve
  but can't find significant issues
```

**每次测试时需要检查的内容：**
- 来源中缺失的功能；
- 组合方法之间的矛盾；
- 模糊不清、无法执行的指令；
- 代码冗余（本可简化的地方）；
- 安全漏洞；
- 文件/脚本引用错误。

**在 VETTING-LOG.md 中记录：**
- 每次测试的编号；
- 发现的问题；
- 采取的修复措施；
- 选择稳定的原因。

**只有当满足以下条件时才能继续：**
- 连续三次测试均无重大问题；
- 将小问题记录为已知限制。

### 第八步：人工审核

将审核后的技能提交审核：
- 显示技能的组成部分及其来源；
- 强调已解决的冲突；
- 提供审核总结；
- 在保存前征求最终确认。

## 输出结果

生成的技能将具备以下特点：
- 来自所有分析技能的最佳功能；
- 明确的来源标注；
- 仅包含通过安全扫描的组件；
- 统一的文档说明。

## 示例流程

用户：“为我创建一个 SEO 审计技能。”

Frankenstein 的处理流程：
```
Searching ClawHub for "SEO audit"...
Found 5 skills:
  1. seo-audit (coreyhaines31)
  2. audit-website (squirrelscan)
  3. seo-optimizer (local)
  4. technical-seo (unknown)
  5. seo-checker (unknown)

Security scanning...
  ✓ seo-audit: SAFE (8/10)
  ✓ audit-website: SAFE (7/10)
  ✓ seo-optimizer: SAFE (9/10)
  ✗ technical-seo: RISKY (4/10) - skipping
  ✗ seo-checker: RISKY (3/10) - skipping

Analyzing 3 safe skills...

Comparison:
| Feature              | seo-audit | audit-website | seo-optimizer |
|----------------------|-----------|---------------|---------------|
| Methodology depth    | ★★★★★     | ★★★           | ★★★★          |
| Automated rules      | None      | 230+          | 50+           |
| Auto-fix capability  | No        | No            | Yes           |
| CLI tool             | No        | squirrel      | No            |
| E-E-A-T coverage     | Yes       | Yes           | Partial       |

Recommended combination:
- Methodology: seo-audit (best framework)
- Rules engine: audit-website (230+ rules via squirrel CLI)
- Auto-fix: seo-optimizer (automated fixes)
- E-E-A-T: seo-audit (comprehensive)

Build this Frankenstein? [Yes/No]
```

## 依赖项

该技能需要以下工具：
- clawhub CLI（用于搜索和安装技能）；
- skill-auditor（用于安全扫描）；
- sandwrap（用于安全分析）；
- skill-creator（用于技能的组装）。

## 生成子代理

在生成分析子代理时，除非用户另有要求，否则始终使用 Opus（或当前最佳思维模型）：

```
sessions_spawn(
  task: "FRANKENSTEIN ANALYSIS: [topic]...",
  model: "opus"
)
```

成本较低的模型可能无法捕捉技能之间的细微差异，导致生成的技能较为简单。

## 限制

- 仅能组合公开可用的技能；
- 会忽略未通过安全扫描的技能；
- 无法解决复杂的架构冲突；
- 最终的技能整合需要人工判断；
- 技能的质量取决于可用的技能资源。

## 致谢

当创建一个 Frankenstein 技能时，会包含以下信息：
```
## Sources
Built from best parts of:
- seo-audit by coreyhaines31 (methodology)
- audit-website by squirrelscan (rules engine)
- seo-optimizer (auto-fix)
```