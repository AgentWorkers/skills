---
name: hybrid-db-health
description: 验证并排查 OpenClaw 代理所使用的混合数据库系统（Pulse 任务数据库 + RAG Pinecone 堆栈）的问题。当需要检查系统设置、连接状态或对代理执行数据库健康测试时，请使用此功能。
---
# 混合数据库健康检查

对本工作空间中的两个数据库系统进行快速、可靠的健康检查：

当与 `shared-pinecone-rag` 结合使用时，可以将这一组合视为一个 **持久内存技能栈**（用于数据检索和健康状态监控）。

1. **Pulse 操作数据库/同步层** 位于 `agents/pulse` 中。
2. **RAG Pinecone 层** 位于 `rag-pinecone-starter` 中。

## 运行手册

1. 运行捆绑的脚本：

```bash
bash scripts/check_hybrid_db.sh
```

2. 解释检查结果：
- `PASS`：子系统已配置且能够正常响应。
- `WARN`：子系统存在但未完全配置。
- `FAIL`：子系统检查执行失败。

3. 用通俗的语言向用户报告结果：
- Pulse 数据库的状态。
- RAG 数据库的状态。
- 如果出现 `WARN` 或 `FAIL`，请提供具体的下一步修复步骤。

## 手动检查（如果脚本不可用）

### Pulse 数据库

```bash
cd /home/Mike/.openclaw/workspace/agents/pulse
python3 openclaw_sync.py --check
```

预期输出：`数据库连接正常`

### RAG Pinecone

```bash
cd /home/Mike/.openclaw/workspace/rag-pinecone-starter
[ -f .env ] && grep -E '^(OPENAI_API_KEY|PINECONE_API_KEY)=' .env
```

如果任一系统的状态显示为“空白”，则报告为“尚未连接”。

可选的实时连接测试（需要相关密钥和依赖项）：

```bash
source .venv/bin/activate
python query.py "connectivity test"
```

## 输出格式

返回简洁的状态信息，例如：
- Pulse 数据库：PASS/FAIL
- RAG Pinecone：PASS/WARN/FAIL
- 下一步操作：以项目符号列出。