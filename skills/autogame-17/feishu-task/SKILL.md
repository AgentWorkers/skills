# feishu-task

用于管理 Feishu（Lark）中的任务。适用于多人协作和优先级工作项的管理。

## 使用方法

### 创建任务
创建任务并将其分配给用户。
```bash
node skills/feishu-task/create.js --summary "Task Title" --desc "Details" --due "2026-02-04 10:00" --assignees "ou_1,ou_2"
```

### 列出任务
列出最近的任务以查看状态。
```bash
node skills/feishu-task/list.js --limit 10
```

## 协议说明
- **适用场景**：多人协作、高优先级任务跟踪或工作流程中的依赖关系管理。
- **与日历的区别**：任务支持“已完成”状态标记以及多个任务分配者；而日历主要用于时间安排。

---

（注：由于提供的 `SKILL.md` 文件内容较为简短，部分功能说明（如创建任务的代码示例）在翻译时可能无法完整呈现。在实际应用中，这些代码示例通常会包含具体的 API 调用或命令格式。）