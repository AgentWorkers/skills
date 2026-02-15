---
name: policy-lawyer
description: 请参考工作空间策略手册（workspace policy playbook），通过搜索整理好的策略文档或查阅其各个章节来回答“关于语气、数据使用和协作方面的规则是什么？”这个问题。
---

# Policy Lawyer

## 概述

`policy-lawyer` 是基于 `references/policies.md` 中整理好的政策文档集开发的。通过命令行工具（`scripts/policy_lawyer.py`），您可以执行以下操作：

- `--list-topics`：列出所有的政策主题。
- `--topic <名称>`：显示与指定主题匹配的政策内容（不区分大小写）。
- `--keyword <关键词>`：在所有政策文档中搜索指定的关键词。
- `--policy-file <路径>`：在比较不同工作区的内容时，指定要使用的政策文档文件。

当您需要在起草公告前回顾社区标准，或者遇到需要引用权威政策内容的问题时，可以使用这个工具。

## 命令行用法

- `python3 skills/policy-lawyer/scripts/policy_lawyer.py --list-topics`：打印政策文档中所有以 `## <章节名称>` 开头的章节内容。
- `--topic "Tone"`：直接输出关于“语气”（tone）的指导原则，以便在需要提醒他人注意语气规范时直接引用。
- `--keyword security`（或其他关键词）：在所有政策文档中查找包含该关键词的段落，快速了解该主题的相关规定。
- 如果您想查看另一个工作区的政策文档，可以输入 `--policy-file /path/to/repo/references/policies.md`。

## 示例命令

```bash
python3 skills/policy-lawyer/scripts/policy_lawyer.py --topic Tone
python3 skills/policy-lawyer/scripts/policy_lawyer.py --keyword data --policy-file ../other-workspace/references/policies.md
```

第一个命令会打印出关于“语气”（tone）的指导原则；第二个命令会在另一个工作区的政策文档中搜索“data”这个词，并显示所有匹配的段落。

## 参考文档

- `references/policies.md`：包含关于语气（tone）、数据（data）、协作（collaboration）和安全规则（security rules）的整理好的政策文档集。

## 资源

- **GitHub仓库：** https://github.com/CrimsonDevil333333/policy-lawyer
- **ClawHub：** https://www.clawhub.ai/skills/policy-lawyer