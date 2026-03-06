---
name: aibrary-reading-list
description: "[图书馆] 生成一个精心策划的主题阅读列表，其中包含多本书籍，并按照合理的阅读顺序进行排列。适用于用户需要某个主题的系统化书单、请求阅读清单、希望通过多本书籍深入探索某个领域，或希望在某个领域建立专业知识的场景。这与 aibrary-book-recommend（单本书推荐）和 aibrary-book-search（查找特定书籍）的功能不同。"
---
# 阅读清单 — Aibrary

我们精心策划、按主题分类的阅读清单，旨在帮助用户系统地提升专业技能。这些清单的制定基于Aibrary的知识整理方法。

## 用户输入

用户需要指定以下信息：
- **主题/领域**：他们希望探索的领域（必填）
- **难度偏好**：初级、中级、高级或混合难度（可选，默认为混合难度）
- **书籍数量**：所需书籍的数量（可选，默认为7-10本）
- **其他限制条件**：时间范围、语言要求或领域内的特定关注点（可选）

## 工作流程

1. **明确阅读范围**：明确该主题涵盖的内容以及不包含的内容。如果主题过于宽泛，会为用户推荐2-3个具体的子主题供其选择。
2. **挑选书籍**：选择能够全面覆盖该主题的书籍：
   - 包括奠定核心概念的基础性著作
   - 包括反映当前思想的前沿著作
   - 包括不同的观点以促进批判性思维
   - 确保没有遗漏该主题的任何重要方面
3. **安排阅读顺序**：按逻辑顺序排列书籍：
   - **先打基础**：概念性和入门性著作
   **深入理解**：更专业和高级的著作
   **综合学习**：能够将不同观点联系起来的著作
   - 标记书籍为“必读”或“推荐阅读”
4. **提供阅读指导**：解释每本书与下一本书之间的联系，以及读者在每个阶段能学到什么。
5. **使用用户指定的语言**：确保所有内容都使用用户输入的语言进行呈现。

## 输出格式

```
# Reading List: [Theme Name]

[1-2 sentence overview of what this reading list covers and who it's for]

**Total books**: [Count] | **Estimated total reading time**: [Hours] | **Difficulty**: [Level range]

---

## Stage 1: Foundation
*[What the reader gains from this stage]*

### 1. [Book Title] ⭐ Essential
**Author**: [Name] | **Year**: [Year]
[One sentence on what this book contributes to the theme]

### 2. [Book Title]
**Author**: [Name] | **Year**: [Year]
[One sentence on what this book contributes to the theme]

**Stage 1 → Stage 2 bridge**: [How the foundation prepares the reader for deeper exploration]

---

## Stage 2: Depth
*[What the reader gains from this stage]*

### 3. [Book Title] ⭐ Essential
...

---

## Stage 3: Synthesis
*[What the reader gains from this stage]*

...

---

## Quick-Start Option
*If you only have time for 3 books, read these*:
1. [Book] — [Why]
2. [Book] — [Why]
3. [Book] — [Why]
```

### 示例输出

**用户输入**：“给我一个关于系统思维的阅读清单”

---

# 阅读清单：系统思维

本阅读清单帮助您从理解系统基础开始，逐步掌握如何在复杂的实际场景中应用系统思维。适合领导者、工程师以及任何希望把握全局的人士。

**总书籍数量**：8本 | **预计总阅读时间**：约50小时 | **难度**：初级 → 高级

---

## 第一阶段：基础
*建立理解系统的思维模型*

### 1. 《系统思维》 ⭐ 必读
**作者**：多娜拉·梅多斯 | **出版年份**：2008年
这是一本关于系统思维的权威入门书，内容清晰易懂，且对于探讨反馈循环等概念非常实用。

### 2. 《第五项修炼》
**作者**：彼得·圣吉 | **出版年份**：2006年（修订版）
本书将系统思维的理念引入组织学习，对于在团队和商业环境中应用系统思维至关重要。

**从第一阶段到第二阶段的过渡**：掌握了基础知识后，您可以进一步了解系统思维如何应用于特定领域和复杂问题。

---

## 快速入门选项
*如果您只有时间阅读3本书，可以参考以下推荐**：
1. 《系统思维》——系统思维的基础知识
2. 《第五项修炼》——系统思维在实践中的应用
3. 《见树又见林》——系统思维的可视化工具

---

## 制作阅读清单的指导原则：

- 阅读清单应具有连贯性——书籍之间应相互关联，而不仅仅是简单的集合
- 为时间有限的读者提供“快速入门选项”
- 清晰区分必读书和推荐书
- 在不同阶段之间提供解释性内容
- 平衡经典著作与前沿作品
- 如果主题过于宽泛，主动缩小范围或提供子主题选项