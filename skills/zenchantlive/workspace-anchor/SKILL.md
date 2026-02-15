# ⚓ 工作区锚点（Workspace Anchor）

这是一个多智能体工作区感知与安全系统，能够通过基于环境的命名机制来发现、列出、切换和验证项目，从而防止智能体出现混乱或错误配置。

## 🤖 智能体指令（重要提示：Critical Instruction）
在使用此功能之前，必须确定用户环境的正确绝对路径。如果路径存在歧义，可以使用 `exec` 命令来查找 `.project-lock` 文件。

## 📝 命令行界面（CLI）命令
- `discover`：查找所有的 `.project-lock` 文件。
- `list`：以格式化的方式显示所有锚点的列表。
- `create <path>`：创建一个新的锚点。
- `switch <name>`：切换到指定的工作区上下文。
- `validate <path>`：检查路径是否位于当前锚点范围内。