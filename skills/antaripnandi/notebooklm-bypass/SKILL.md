---
name: notebooklm
description: 支持通过编程方式控制 NotebookLM，并具备自动恢复功能（在遇到认证错误时能够自动重试）。
---
# NotebookLM CLI

## 命令
```bash
notebooklm list                    # 列出所有笔记本及其ID
notebooklm create "名称"                # 创建笔记本（返回笔记本ID）
notebooklm source add "<url_or_file>" -n <ID>      # 将URL、PDF或YouTube视频添加到笔记本中
notebooklm source add "<url>" -n <ID> --wait       # 添加视频并等待处理完成
notebooklm source list -n <ID>              # 列出笔记本中的所有资源
notebooklm ask "问题" -n <ID>                # 向AI查询资源相关内容
```

## 规则：
1. **不允许使用播放列表**：必须手动提取每个YouTube视频的URL，并逐一添加到笔记本中。
2. **每个笔记本最多只能包含50个资源**。
3. **在脚本中添加资源时，请使用`--wait`选项以确保处理过程顺利完成**。
4. **身份验证恢复**：如果`notebooklm`因“身份验证过期”而失败，必须先获得用户的明确许可才能恢复操作。建议运行`python {WORKSPACE_DIR}/skills/notebooklm-bypass/scripts/auto_playwright.py`脚本。只有在用户同意的情况下，才能执行该脚本。该脚本会获取新的cookies，并自动将其设置到Windows系统环境变量中。完成后，可以重新尝试执行相关命令。