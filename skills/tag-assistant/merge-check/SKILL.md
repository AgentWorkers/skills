---
name: merge-check
description: 分析 GitHub 提交的合并请求（Pull Request, PR）的合并可行性——根据技术、架构、流程、社区参与度以及合规性等因素来预测该请求是否会被合并。适用于需要审查 PR、判断 PR 是否会被合并、评估 PR 质量或预测其被接受情况的场景。支持通过 `owner/repo#number` 或 URL 查找任意 GitHub PR。
---
# 合并检查

通过分析GitHub PR与一套全面的拒绝向量分类体系，来预测该PR是否会被合并。这并非一个通用的代码质量工具——它回答的是：“这个PR会被维护者合并吗？”

## 快速入门

1. 运行数据收集脚本：
   ```bash
   bash skills/merge-check/scripts/merge-check.sh owner/repo#123
   # or
   bash skills/merge-check/scripts/merge-check.sh https://github.com/owner/repo/pull/123
   ```
2. 解析JSON输出结果
3. 根据以下维度进行分析
4. 生成合并可行性报告

## 分析维度

收集数据后，需要从所有这些维度进行分析。详细的信息请参考`skills/merge-check/references/rejection-taxonomy.md`文件中的拒绝向量框架。

### 1. 技术指标（自动化检查）
- **持续集成（CI）状态**：所有检查都通过了吗？是否有任何失败或待处理的检查？
- **构建状态**：代码能否成功编译/构建？
- **代码覆盖率**：是否存在代码覆盖率下降的情况？

### 2. PR的基本质量
- **代码量**（最具预测性的单一因素）：
  - 🟢 修改的代码行数 < 400行 — 理想状态，易于审核
  - 🟡 400–1000行 — 存在风险，可能导致审核者疲劳
  - 🔴 > 1000行 — 危险区域，很可能被延迟处理或被拒绝
- **代码文件分布**：代码集中在某个区域，还是分散在多个目录中？
- **功能单一性**：PR只实现了一个功能，还是包含多种功能？
- **标题和描述**：是否清晰、具体？还是模糊/空洞？
- **关联问题**：是否引用了相关问题？（表明PR的意图性）
- **提交信息的质量**：提交信息是否简洁明了？提交次数是否合理？是否已经准备好合并？

### 3. 架构适配性
- **代码风格一致性**：是否符合仓库的编码规范？（语言、目录结构、命名规则）
- **依赖关系**：是否引入了新的依赖项？（可能带来问题）
- **范围蔓延**：PR是否超出了其最初设定的功能范围？
- **文件类型**：是否与仓库的技术栈相匹配？

### 4. 审核状态
- **已获得的批准数**：目前获得了多少个批准？还需要多少个？
- **未解决的问题**：是否存在未解决的请求或问题？（强烈的拒绝信号）
- **审核者分配**：是否已经分配了所需的审核者？
- **审核评论的倾向**：评论是积极的、中立的，还是负面的？
- **代码所有者**：PR是否涉及需要代码所有者审核的文件？他们是否已经开始审核？

### 5. 流程合规性
- **草稿状态**：草稿状态的PR不会被合并
- **特殊标签**：如“WIP”（进行中）、“do-not-merge”（禁止合并）、“needs-work”（需要改进）等
- **PR模板**：是否使用了正确的模板？（未使用模板可能是一个警告信号）
- **CLA/DCO**：如果仓库有相关要求，是否签署了CLA/DCO协议？

### 6. 社交/元数据指标
- **作者的合并历史**：该作者最近在这个仓库中提交的PR中有多少被合并了？
- **PR的活跃度**：PR已经开放了多久？（超过2周可能引起关注，超过30天可能被忽略）
- **最近的活动情况**：是否有新的评论或更新？还是完全没有动静？
- **首次贡献者**：新贡献者的PR被拒绝的概率更高

## 输出格式

生成一份结构化的报告：

### 合并可行性评分
- 🟢 **高**（>80%的可能性被合并）——没有阻碍因素，审核结果积极，CI状态正常
- 🟡 **中等**（40–80%）——存在一些问题，但可以解决
- 🔴 **低**（<40%）——存在重大阻碍因素

### 报告内容
1. **合并可行性评分**：🟢/🟡/🔴，并附上百分比估计
2. **风险因素**：按严重程度排序的具体问题列表
3. **优势**：PR中有哪些有利因素
4. **建议**：为提高合并可行性可采取的措施（如果评分还不是🟢）
5. **结论**：简短的总结

### 示例输出
```
## PR Mergeability Report: owner/repo#123

**Score: 🟡 Medium (~55%)**

### Risk Factors
- ⚠️ 847 lines changed — approaching reviewer fatigue threshold
- ⚠️ Changes requested by @maintainer not yet addressed
- ⚠️ Touches 12 files across 6 directories — scattered scope
- ℹ️ No linked issue

### Strengths
- ✅ All 14 CI checks passing
- ✅ Clear title and detailed description
- ✅ Author has 73% merge rate in this repo (8/11 recent PRs)
- ✅ Active discussion — last update 2 hours ago

### Recommendations
1. Address @maintainer's review comments before requesting re-review
2. Consider splitting into smaller PRs (config changes vs logic changes)
3. Link the relevant issue for traceability

### Verdict
Solid PR with passing CI and an active author, but stalled on unaddressed review feedback — resolving those comments is the critical path to merge.
```

## 脚本参考

脚本`scripts/merge-check.sh`通过`gh` CLI收集所有数据，并输出一个包含以下键的JSON对象：

| 键 | 内容 |
|-----|----------|
| `pr` | 完整的PR元数据（标题、正文、作者、状态、草稿状态、标签、审核者） |
| `files` | 变更文件的列表及对应的补丁信息 |
| `diff_stats` | 总的添加、删除和修改的文件数量 |
| `checks` | 主提交对应的CI检查结果 |
| `reviews` | 所有的审核记录（已批准、需要修改、有评论的审核） |
| `review_comments` | 审核者的评论 |
| `issue_comments` | PR相关的讨论评论 |
| `commits` | 提交记录及对应的提交信息 |
| `repo` | 仓库的元数据（语言、代码量、默认设置） |
| `author_history` | 作者最近提交的PR及其合并情况 |
| `has_codeowners` | 是否涉及需要代码所有者审核的文件 |
| `has_contributing` | 是否有贡献者参与审核 |

## 错误处理

当个别API调用失败时（例如遇到速率限制或404错误），脚本会输出“error”字段。请分析可用的数据，并在报告中注明任何缺失的信息。