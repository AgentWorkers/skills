---
name: claw-compactor
description: "Claw Compactor v6.0 — 通过基于规则的压缩、字典编码、会话数据压缩以及渐进式上下文加载技术，实现超过50%的压缩效率提升。"
---

# 🦞 Claw Compactor

![Claw Compactor Banner](assets/banner.png)

*“精简你的数据，保留关键信息。”*

**将你的AI代理的令牌消耗量减少一半。** 通过使用5层压缩技术，一个命令即可压缩你的整个工作空间——包括内存文件、会话记录和子代理上下文。该压缩过程是确定性的，且大部分情况下是无损的。无需使用大型语言模型（LLM）。

## 特点
- **5层压缩机制**：依次执行，以实现最大程度的节省
- **零LLM成本**：所有压缩操作均基于规则且具有确定性
- **无损压缩**：支持字典压缩、RLE压缩和基于规则的压缩
- **会话记录压缩率高达97%**：通过提取关键信息实现
- **分层摘要**（L0/L1/L2）：支持渐进式上下文加载
- **支持中文/日文/韩文**：完全兼容中文、日文和韩文
- **一个命令即可完成所有操作**：`full`命令会按最优顺序执行所有步骤

## 5层压缩机制

| 编号 | 压缩层 | 方法 | 节省比例 | 是否无损 |
| --- | --- | --- | --- | --- |
| 1 | 规则引擎 | 删除重复行、去除Markdown填充内容、合并章节 | 4-8% | ✅ |
| 2 | 字典编码 | 自动学习的编码规则、`$XX`替换 | 4-5% | ✅ |
| 3 | 观察压缩 | 会话数据（JSONL格式）→ 结构化摘要 | 约97% | ❌* |
| 4 | RLE压缩 | 路径简化（`$WS`）、IP前缀压缩、枚举压缩 | 1-2% | ✅ |
| 5 | 压缩上下文协议 | 使用超简/中等/简化的表示方式 | 20-60% | ❌* |

*有损压缩技术会保留所有数据和决策内容；仅去除冗余的格式信息。*

## 快速入门

```bash
git clone https://github.com/aeromomo/claw-compactor.git
cd claw-compactor

# See how much you'd save (non-destructive)
python3 scripts/mem_compress.py /path/to/workspace benchmark

# Compress everything
python3 scripts/mem_compress.py /path/to/workspace full
```

**系统要求：** Python 3.9及以上版本。可选：安装`pip install tiktoken`以获取精确的令牌计数（如未安装则使用启发式方法）。**

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│                      mem_compress.py                        │
│                   (unified entry point)                     │
└──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬────┘
       │      │      │      │      │      │      │      │
       ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼
  estimate compress  dict  dedup observe tiers  audit optimize
       └──────┴──────┴──┬───┴──────┴──────┴──────┴──────┘
                        ▼
                  ┌────────────────┐
                  │     lib/       │
                  │ tokens.py      │ ← tiktoken or heuristic
                  │ markdown.py    │ ← section parsing
                  │ dedup.py       │ ← shingle hashing
                  │ dictionary.py  │ ← codebook compression
                  │ rle.py         │ ← path/IP/enum encoding
                  │ tokenizer_     │
                  │   optimizer.py │ ← format optimization
                  │ config.py      │ ← JSON config
                  │ exceptions.py  │ ← error types
                  └────────────────┘
```

## 命令说明

所有命令的格式为：`python3 scripts/mem_compress.py <workspace> <command> [options]`

| 命令 | 功能 | 平均节省比例 |
| --- | --- | --- |
| `full` | 完整执行所有压缩步骤 | 总节省比例超过50% |
| `benchmark` | 预览压缩效果 | — |
| `compress` | 基于规则的压缩 | 4-8% |
| `dict` | 使用自动编码规则的字典压缩 | 4-5% |
| `observe` | 将会话记录转换为结构化摘要 | 约97% |
| `tiers` | 生成L0/L1/L2分层摘要 | 在子代理加载时节省88-95% |
| `dedup` | 检查并删除重复文件 | 节省比例因文件而异 |
| `estimate` | 输出令牌计数报告 | — |
| `audit` | 检查工作空间状态 | — |
| `optimize` | 优化文件格式 | 1-3% |

### 全局选项
- `--json` | 生成机器可读的JSON格式输出 |
- `--dry-run` | 预览压缩效果（不保存更改） |
- `--since YYYY-MM-DD` | 按日期筛选会话记录 |
- `--auto-merge` | 自动合并重复文件 |

## 实际应用中的节省效果

| 工作空间状态 | 平均节省比例 | 备注 |
| --- | --- | --- |
| 会话记录（使用`observe`命令压缩） | 约97% | 从庞大的JSONL文件转换为简洁的摘要文件 |
| 新创建的工作空间 | 50-70% | 首次运行时效果显著 |
| 定期维护的工作空间 | 10-20% | 每周运行时节省效果 |
| 已经优化的工作空间 | 3-12% | 由于文件已经较为整洁，节省效果逐渐降低 |

## 缓存优化

在压缩前启用**提示缓存**功能，可进一步节省90%的令牌成本：

```json
{
  "models": {
    "model-name": {
      "cacheRetention": "long"
    }
  }
}
```

压缩操作减少令牌数量，缓存机制进一步降低每令牌的成本。综合来看：50%的压缩效果加上90%的缓存折扣，可实现**95%的实际成本降低**。

## 自动化调度

建议每周或根据需要自动执行压缩任务：

```markdown
## Memory Maintenance (weekly)
- python3 skills/claw-compactor/scripts/mem_compress.py <workspace> benchmark
- If savings > 5%: run full pipeline
- If pending transcripts: run observe
```

**示例Cron脚本：**  
```
0 3 * * 0 cd /path/to/skills/claw-compactor && python3 scripts/mem_compress.py /path/to/workspace full
```

## 配置文件

可选的配置文件：`claw-compactor-config.json`，位于工作空间根目录：

```json
{
  "chars_per_token": 4,
  "level0_max_tokens": 200,
  "level1_max_tokens": 500,
  "dedup_similarity_threshold": 0.6,
  "dedup_shingle_size": 3
}
```

所有配置字段均为可选；如果未提供，则使用默认值。

## 生成文件

| 文件名 | 用途 |
| --- | --- |
| `memory/.codebook.json` | 存储字典编码规则 | 必须与内存文件一起保存 |
| `memory/.observed-sessions.json` | 记录已处理的会话记录 |
| `memory/observations/` | 存储压缩后的会话摘要 |
| `memory/MEMORY-L0.md` | 第0层摘要（约200个令牌） |

## 常见问题解答

**Q：压缩会丢失数据吗？**  
A：规则引擎、字典编码、RLE压缩和分词器优化都是无损的；只有观察压缩和压缩上下文协议（CCP）是有损的，但会保留所有数据和决策内容。

**Q：字典解压缩是如何工作的？**  
A：`decompress_text(text, codebook)`函数会将所有`$XX`替换后的内容恢复原样。请确保`memory/.codebook.json`文件存在且格式正确。

**Q：可以单独执行某些步骤吗？**  
A：可以。每个命令都是独立的：`compress`、`dict`、`observe`、`tiers`、`dedup`、`optimize`。

**Q：如果未安装`tiktoken`怎么办？**  
A：系统会回退到基于中文/日文/韩文字符的启发式算法（字符数量约减少4倍）。虽然精度略低，但结果仍较为准确。

**Q：该工具支持中文/日文/Unicode吗？**  
A：支持。完全兼容中文、日文和韩文，包括对字符的识别和标点符号的规范化处理。

## 故障排除

- 如果出现`FileNotFoundError`：请确认路径指向工作空间根目录（包含`memory/`或`MEMORY.md`文件）。
- 如果字典解压缩失败：请检查`memory/.codebook.json`文件是否存在且格式正确。
- 如果`benchmark`命令显示“零节省”：说明工作空间已经过优化，无需进一步处理。
- 如果`observe`命令找不到会话记录：请检查会话目录中是否有`.jsonl`文件。
- 如果令牌计数结果不正确：请安装`tiktoken`：`pip3 install tiktoken`。

## 致谢

- 本工具的灵感来源于[claude-mem](https://github.com/thedotmack/claude-mem)，由Bot777为[OpenClaw](https://openclaw.ai)开发。

## 许可证

MIT许可证