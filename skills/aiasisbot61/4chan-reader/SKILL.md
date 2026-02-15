---
name: 4chan-reader
description: **功能描述：**  
浏览 4chan 的各个板块（如 /a/、/vg/、/v/ 等），并将其中的帖子讨论内容提取到结构化的文本文件中。该工具适用于需要从 4chan 板块获取目录信息或特定帖子内容（包括帖子文本及文件元数据）的场景。
---

# 4chan 阅读器

此技能允许您将 4chan 论坛中的帖子整理并提取为结构化文本。

## 工作流程

### 1. 查看论坛目录
要查看某个论坛上的活跃帖子及其回复数量：
```bash
python3 scripts/chan_extractor.py catalog <board>
```
输出格式：`ThreadID|PostCount|TeaserText`

### 2. 提取帖子内容
要阅读特定帖子（可选择保存）：
```bash
python3 scripts/chan_extractor.py thread <board> <thread_id> [output_root_dir] [word_limit]
```
- `output_root_dir`（可选）：如果提供，将内容保存到 `<output_root_dir>/<board>_<timestamp>/<thread_id>.txt` 文件中。
- `word_limit`（可选）：限制每行帖子内容的字数。

## 详细信息
- **脚本**：所有操作均使用 [chan extractor.py](scripts/chan extractor.py) 脚本完成。