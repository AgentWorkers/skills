---
name: discovery
description: 创建一份发现文档（Discovery Document），以收集并明确各项需求。
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: true
---
# 发现（Discovery）

创建一个发现文档，用于在制定实施计划之前收集和明确需求。

## 功能

1. 收集功能性需求和非功能性需求。
2. 记录约束条件和依赖关系。
3. 识别需要解答的未解决的问题。
4. 提出高层次的解决方案。
5. 记录风险和未知因素。

## 使用方法

```
/discovery <topic>
```

**参数：**
- `topic`（必填）：需要收集需求的特性或主题。

## 输出结果

生成文件：`flow/discovery/discovery_<topic>_v<version>.md`

## 文档结构

```markdown
# Discovery: [Topic]

## Context
Why this discovery is needed

## Requirements Gathered
### Functional Requirements
- [FR-1]: Description

### Non-Functional Requirements
- [NFR-1]: Description

### Constraints
- [C-1]: Description

## Open Questions
| # | Question | Status | Answer |
|---|----------|--------|--------|
| 1 | Question | Open   | -      |

## Technical Considerations
Architecture, dependencies, patterns

## Proposed Approach
High-level recommendation

## Risks and Unknowns
Identified risks with mitigation strategies

## Next Steps
Follow-up actions
```

## 示例

```
/discovery user authentication with OAuth
```

**生成文件：**`flow/discovery/discovery_user_authentication_with.oauth_v1.md`

## 重要规则

- **禁止编写代码**：发现阶段仅用于收集需求，不涉及实现细节。
- **提出问题**：使用互动式问题来澄清不明确的需求。
- **明确标注假设**：务必明确标注所有假设，以便后续验证。

## 下一步操作

在完成需求收集后，运行命令 `/create-plan @flow/discovery/discovery_<topic>_v1.md` 以制定实施计划。