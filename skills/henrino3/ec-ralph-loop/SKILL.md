# Ralph Loop 技能

这是一个自主运行的 AI 编码循环，它会不断重复执行 Codex/Claude Code，直到所有用户故事（PRD）都完成。

**来源：** https://github.com/snarktank/ralph （8,600 多个星标）

## 概念

Ralph 解决了“上下文溢出”问题：大型任务会超出单个上下文窗口的处理能力，从而导致代码质量下降。Ralph 的工作流程如下：
1. 将任务分解为 `prd.json` 文件中的小用户故事。
2. 为每个用户故事创建一个新的编码代理实例。
3. 每个代理实例负责实现一个用户故事，运行测试，如果测试通过则提交代码。
4. 将该用户故事的状态标记为 `passes: true`。
5. 重复此过程，直到所有用户故事都通过测试。

Ralph 的状态信息通过以下方式保存：git 历史记录、`progress.txt` 文件和 `prd.json` 文件（而非具体的上下文数据）。

## 快速入门

```bash
# 1. Create a PRD for your feature
~/agent-workspace/skills/ralph/scripts/create-prd.sh "Feature description"

# 2. Convert PRD to prd.json
~/agent-workspace/skills/ralph/scripts/convert-prd.sh tasks/prd-feature.md

# 3. Run Ralph loop
~/agent-workspace/skills/ralph/scripts/run-ralph.sh [project_dir] [max_iterations]
```

## 相关文件

| 文件名 | 用途 |
|------|---------|
| `prd.json` | 包含用户故事及其完成状态（`passes: true/false`） |
| `progress.txt` | 记录每次迭代中的学习成果 |
| `AGENTS.md` | 每次迭代后更新的模式和注意事项 |

## `prd.json` 的格式

```json
{
  "branchName": "ralph/feature-name",
  "userStories": [
    {
      "id": "1",
      "title": "Add database column",
      "description": "Add email_verified column to users table",
      "acceptanceCriteria": [
        "Migration exists",
        "Column is boolean, default false",
        "Tests pass"
      ],
      "priority": 1,
      "passes": false
    }
  ]
}
```

## 适合处理的用户故事规模

✅ 适合处理的用户故事（可在一个上下文窗口内完成）：
- 添加数据库列及迁移操作
- 为现有页面添加 UI 组件
- 用新逻辑更新服务器功能
- 为列表添加筛选下拉菜单

❌ 不适合处理的用户故事（需要拆分）：
- “构建整个仪表板”
- “添加身份验证功能”
- “重构 API”

## 与 Codex CLI 的集成

Ralph 可以通过 Codex CLI (`codex exec`) 或 Claude Code 来执行代码实现。

```bash
# Default: uses Codex CLI
./run-ralph.sh ~/Code/myproject 10

# Or specify Claude Code
./run-ralph.sh ~/Code/myproject 10 --tool claude
```

## 工作流程

1. **创建 PRD** → 编写详细的 Markdown 需求文档。
2. **将需求转换为 `prd.json` 格式** → 形成结构化的用户故事列表。
3. **运行 Ralph** → 进入循环，直到所有用户故事都通过测试。
4. **审查代码** → 检查提交的内容并合并相关分支。

## 示例流程

```bash
# Henry asks: "Implement RLS for all 154 tables"

# 1. Create PRD
~/agent-workspace/skills/ralph/scripts/create-prd.sh "Implement Row Level Security for all database tables"

# 2. Convert (generates 154 user stories)
~/agent-workspace/skills/ralph/scripts/convert-prd.sh tasks/prd-rls-migration.md

# 3. Run overnight
nohup ~/agent-workspace/skills/ralph/scripts/run-ralph.sh ~/Code/myproject 154 > ralph.log 2>&1 &

# 4. Check progress
cat ~/Code/myproject/scripts/ralph/prd.json | jq '.userStories[] | {id, title, passes}'
```

## 停止条件

- 所有用户故事的状态均为 `passes: true` → 输出 `<promise>COMPLETE</promise>`。
- 达到最大迭代次数。
- 手动停止循环（使用 Ctrl+C）。

## 使用技巧

1. **用户故事应尽可能简短**，确保能在一个上下文窗口内完成。
2. **编写高质量的测试用例**，因为 Ralph 依赖测试结果来验证代码的正确性。
3. **定期更新 `AGENTS.md` 文件**，记录开发过程中的常见问题和解决方案。
4. **对于 UI 相关的用户故事**，务必添加“在浏览器中验证”的测试要求。

## 参考资料

- [Ralph 的 GitHub 仓库](https://github.com/snarktank/ralph)
- [Geoffrey Huntley 的相关文章](https://ghuntley.com/ralph/)
- [Ryan Carson 的讨论帖](https://x.com/ryancarson/status/2008548371712135632)