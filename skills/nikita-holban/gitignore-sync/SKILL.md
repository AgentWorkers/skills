---
name: gitignore-sync
description: Context-aware .gitignore generation backed by gitignore.io, not vibes. Make it boring again: accurate, idempotent, context-aware.
---

# Gitignore 同步

根据实际仓库的配置信息以及 gitignore.io 提供的规则，自动生成高置信度的 `.gitignore` 文件，然后通过受管理的代码块安全地更新这些规则，以确保手动设置的规则不会被修改。

## 执行规则

仅使用 `scripts/update-gitignore.py` 脚本来执行此操作。
请勿在临时命令中直接从 API 获取数据。
当选择了此功能时，切勿手动编写或修改 `.gitignore` 文件。

## 工作流程

1. 从用户输入的提示中推断出所需的模板。
2. 从仓库中的文件和文件夹中检测可能的模板。
3. 使用 `--prompt-text` 和/或 `--services` 参数运行 `scripts/update-gitignore.py` 脚本。
4. 脚本会从 `https://www.toptal.com/developers/gitignore/api/<templates>` 获取合并后的模板规则。
5. 脚本会将这些规则写入或更新到 `.gitignore` 文件中的受管理代码块中。
6. 保留 `.gitignore` 文件中非受管理的用户自定义规则。

## 运行方式

在目标仓库的根目录下运行以下命令：

```bash
python3 <skill-path>/scripts/update_gitignore.py \
  --prompt-text "create .gitignore for flutter firebase vscode" \
  --repo .
```

当用户明确指定了所需的服务时，使用相应的模板：

```bash
python3 <skill-path>/scripts/update_gitignore.py \
  --services flutter,firebase,visualstudiocode \
  --repo .
```

## 注意事项

- 如果可能的话，建议同时使用 `--prompt-text` 和 `--services` 参数。
- 手动自定义的规则应放在受管理代码块之外。
- 该脚本只会更新受管理的代码块，不会影响其他部分。
- 如果网络访问受限，可以使用 `--rules-file` 参数进行离线/本地测试。