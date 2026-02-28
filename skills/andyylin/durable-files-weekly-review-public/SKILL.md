---
name: durable-files-weekly-review-public
description: 在任何 OpenClaw 工作区中，每周对持久性指令文件（durable instruction files）进行一次令牌优化审计（token-optimization audit），生成 Markdown 报告，并提出需要审批的清理操作建议。此功能适用于希望在不进行自动删除的情况下，保持 AGENTS/USER/TOOLS/MEMORY 类型文档简洁性的用户。
---
# 持久性文件每周审查（已处理数据 / ClawHub）

使用此技能来审计持久性指令文件，并准备清理提案。

## 默认审查范围
针对工作区根目录下的以下文件进行审计：
- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `TOOLS.md`
- `MEMORY.md`
- `IDENTITY.md`
- `PRIORITIES.md`
- `SKILLS.md`
- `projects.md`

## 执行方式
```bash
python3 scripts/durable_files_review_generic.py --root .
```

（可选操作：）
```bash
python3 scripts/durable_files_review_generic.py --root /path/to/workspace --out knowledge/reports/durable-files
```

## 工作流程
1. 运行扫描工具。
2. 打开生成的报告。
3. 总结文件中包含大量标记（tokens）的文件以及过时的内容。
4. 提出分批清理的建议。
5. **任何删除操作均需获得用户的明确批准。**
6. 应用已批准的修改，并发布简洁的变更日志。

## 成功输出结果
- 包含日期和统计数据的Markdown报告
- 清理请求的审批队列已清空
- 确保不会在未经批准的情况下删除任何内容