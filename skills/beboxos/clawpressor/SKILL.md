---
name: clawpressor
description: **压缩 OpenClaw 会话上下文以减少令牌使用量并延长会话时长**  
该功能利用自然语言处理（NLP）技术（具体为 Sumy）智能地压缩对话历史记录，同时保留关键信息。当出现以下情况时，系统会自动触发该功能：  
1. 会话上下文接近限制（约 300KB）；  
2. 由于会话内容过多导致会话运行变慢；  
3. 过高的令牌消耗增加了 API 使用成本；  
4. 需要在不强制重启的情况下延长会话时长。  

通过压缩会话上下文，可以：  
- 减少令牌的使用量；  
- 提高系统性能；  
- 降低 API 使用成本。
---

# ClawPressor – 会话上下文压缩工具

该工具能够智能地压缩 OpenClaw 会话文件，从而将令牌使用量减少 85% 至 96%。

**作者：** JARVIS（AI 编码器） | **管理方：** BeBoX  
**许可证：** MIT | **版本：** 1.0.0  

## 快速入门  

```bash
# Preview compression without changes
python3 scripts/compress.py --dry-run

# Apply compression
python3 scripts/compress.py --apply

# Restore from backup
python3 scripts/compress.py --restore
```  

## 使用场景  

| 情况 | 应对措施 |
|---------|---------|
| 上下文占用空间达到 30-40% | 尽快计划进行压缩 |
| 上下文占用空间达到 50% | **紧急** — OpenClaw 会自动触发压缩 |
| 会话文件大小超过 300KB | 压缩以提升性能 |
| 响应速度缓慢 | 可能是由于上下文数据过大导致的 |
| API 使用成本较高 | 定期压缩以节省令牌资源 |

## 工作原理  

1. **保留最新上下文**：保留最近 5 条消息，以便快速获取当前上下文信息。  
2. **总结旧消息**：使用 LexRank 算法提取关键信息。  
3. **用压缩后的摘要替换旧消息**：用一条包含摘要的系统消息替换原有消息。  
4. **创建备份**：将原始会话文件保存为 `.backup` 文件。  

## 先决条件  

```bash
pip install sumy
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords')"
```  

## 命令参考  

```bash
# Find and compress latest session (dry-run)
python3 scripts/compress.py

# Compress specific session
python3 scripts/compress.py --session /path/to/session.jsonl --apply

# Keep more recent messages (default: 5)
python3 scripts/compress.py --keep 10 --apply

# Restore if something went wrong
python3 scripts/compress.py --restore

# View compression statistics
python3 scripts/compress.py --stats
```  

## 测试结果  

| 指标 | 压缩前 | 压缩后 | 改善幅度 |
|--------|--------|-------|------|
| 消息数量 | 168 条 | 6 条 | **减少 96%** |
| 文件大小 | 347 KB | 12 KB | **减少 96%** |
| 上下文令牌数量 | 约 50,000 个 | 约 8,000 个 | **减少 84%** |
| 会话持续时间 | 约 30 分钟 | 约 2-3 小时 | **延长 400%** |

## 与工作流程的集成  

**在 HEARTBEAT.md 文件中的集成方式：**  
```markdown
## Context Maintenance (1x/jour)
- Check session size: `ls -lh ~/.openclaw/agents/main/sessions/*.jsonl`
- If > 200KB: `python3 skills/clawpressor/scripts/compress.py --apply`
```  

**手动检查方法：**  
```bash
# See current session stats
ls -lh ~/.openclaw/agents/main/sessions/*.jsonl | head -1
```  

## 安全性说明：**  
- 压缩前会自动创建备份文件。  
- 使用 `--restore` 命令可恢复原始会话数据。  
- 最新消息始终会被完整保留。  
- 摘要信息会以系统消息的形式存储，可供模型使用。  

## 故障排除：**  
| 问题 | 解决方案 |  
|---------|---------|  
| “Sumy 未安装” | 运行 `pip install sumy` 并下载 NLTK 库。 |
| 未找到会话文件 | 确认 `~/.openclaw/agents/main/sessions/` 目录是否存在。 |
| 备份文件丢失 | 可能是文件被覆盖，无法恢复数据。 |
| 摘要质量较差 | 增加 `--keep` 参数的值以保留更多上下文信息。 |

## 致谢：**  
- **编码工作：** JARVIS（AI 辅助工具）  
- **项目管理：** BeBoX  
- **技术实现：** 通过 Sumy（基于 LexRank 算法的自然语言处理技术）实现压缩功能。  

## 相关文档：**  
- 请参阅 `memory/openclaw-context-optimization.md` 以了解完整优化策略。  
- 与 `SOUL_MIN/USER_MIN` 文件结合使用可进一步提升效率。