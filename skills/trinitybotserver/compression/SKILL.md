# Trinity Compress（技能）

用于在迭代式AI开发循环中预先压缩提示信息。

**目标：** 在每次循环运行之前，通过压缩提示文件来减少输入的令牌数量。

- 支持Ralph风格的循环、代理/技能目录以及大多数基于令牌计费的工具。
- 以**本地脚本**的形式运行（无需调用任何模型）。
- 会生成`.bak`备份文件，并支持即时撤销操作。

## 该工具会安装到仓库中的内容：
- `trinity-compress.config.json` — 配置规则和目标文件
- `scripts/trinity-compress.sh` — 压缩脚本
- Makefile片段（可选）：`optimize-prompts`、`optimize-undo`等
- `.gitignore`片段：用于忽略`.bak`文件
- 安装脚本：
  - `scripts/install.ps1`（Windows系统）
  - `scripts/install.sh`（bash系统）

## 系统要求：
- bash 4.0或更高版本
- `jq`工具
- `bc`命令行工具

## 使用方法：
1) 将工具安装到你的仓库中（可以手动复制相关文件，或使用提供的安装脚本）
2) 运行以下命令：
   - `bash scripts/trinity-compress.sh balanced`
   - 或者通过Makefile中的相应目标命令来执行压缩操作

## 撤销操作：
- 可以恢复上一次运行时生成的所有`.bak`备份文件。

## 注意事项：
- 该工具不会修改代码块、URL、文件路径或变量名称。
- 高级压缩模式可能会降低代码的可读性；在提交代码之前请仔细检查压缩效果。