---
name: obsidian-official-cli-headless
description: >
  **安装并配置官方的 Obsidian CLI 以适应无头 Linux 服务器环境**  
  您可以使用非 root 用户权限、Xvfb 虚拟显示技术、基于 ACL 的文件访问控制（vault access），以及 `obs wrapper` 命令来安装和配置 Obsidian CLI。以下是具体步骤：  
  - **安装 Obsidian CLI**：  
    使用非 root 用户权限通过包管理器（如 `apt-get` 或 `yum`）安装 Obsidian CLI。  
  - **配置 Xvfb 虚拟显示**：  
    确保 Xvfb 已正确安装，并配置一个虚拟显示窗口。这通常需要编辑 `/etc/X11/xvfb.conf` 文件，设置 `Display` 参数以创建一个新的虚拟显示器。例如：  
    ```
    Display=0
    Session=0
    Screen=0
    UseScreen=0
    Window=0
    Depth=16
    Resolution=1024x768
    XScreenName=Obsidian
    SessionType=ScreenSaver
    Background=black
    XScreenResolution=1024x768
    WindowBorder=0
    WindowTitle=Obsidian
    WindowColor=black
    WindowBackground=black
    WindowXPos=0
    WindowYPos=0
    WindowSize=1024x768
    WindowMaximize=0
    WindowMinimize=0
    WindowClose=0
    WindowIcon=obsidian
    WindowIconPosition=0
    WindowFont=Arial
    WindowFontSize=12
    WindowFontColor=white
    WindowFontStyle=bold
    WindowFontWeight=4
    WindowFontItalic=0
    WindowFontUnderline=0
    WindowFontAntiAlias=1
    WindowFontScale=1.0
    WindowFontPath=/usr/share/obsidian/bin/obsidian
    ```
  - **配置文件访问控制（ACL）**：  
    为了确保只有授权用户才能访问 Obsidian 文件，您需要使用 ACL 来限制文件和目录的访问权限。这通常需要使用 `setfacl` 命令。例如：  
    ```
    setfacl -R -R /path/to/obsidian
    ```
  - **使用 `obs wrapper` 命令**：  
    `obs wrapper` 是一个用于启动 Obsidian CLI 的脚本，它可以在没有图形界面的环境下运行 Obsidian。您可以通过运行 `obs wrapper` 来启动 Obsidian 应用程序。  
  **适用场景**：  
  - 当您希望在类似 Debian/Ubuntu 的系统中使用官方 Obsidian CLI（而非 `notesmd-cli`），且没有常规桌面会话时。  
  - 当 root 用户权限或图形界面限制导致无法使用原生 CLI 时。  
  **注意**：  
  - 请确保您的系统满足上述配置要求，并了解相关软件的版本兼容性。
---
# Obsidian 官方无头 CLI（Headless CLI）

请将官方 Obsidian CLI 视为一个**以桌面应用为优先的适配方案**，而不仅仅是一个普通的命令行工具（CLI）安装过程。

## 核心规则

- 仅将此技能用于**官方** Obsidian CLI。
- 假设无头 Linux 环境需要一个非 root 用户权限的用户账户、`Xvfb` 显示器软件以及一个用于启动 CLI 的封装脚本（wrapper）。
- 当数据存储库（vault）位于 `/root` 目录下时，优先使用访问控制列表（ACL）而非更改文件所有者权限。
- 建议只配置一个目标数据存储库。
- 避免用户使用 `su - obsidian` 来执行操作，并通过暴露 `/usr/local/bin/obs` 文件来提供详细的 CLI 功能信息。

## 快速操作流程

1. 确认数据存储库的路径。除非用户指定了其他路径，否则默认路径为 `/root/obsidian-vault`。
2. 以 root 权限运行 `scripts/install_official_obsidian.sh` 命令。
3. 以 root 权限运行 `scripts/configure_official_cli.sh <vault_path>` 命令来配置 CLI。
4. 运行 `scripts/verify_official_cli.sh [vault_path]` 命令来验证 CLI 的配置是否正确。
5. 报告封装脚本的路径、当前激活的数据存储库路径、已验证的 CLI 命令以及任何存在的限制或问题。

## 该技能包含的内容

- 官方 Obsidian 的 `.deb` 安装包
- 用于无头环境运行的必要依赖程序
- 专门为 Obsidian CLI 创建的用户账户
- 通过 `~/.config/obsidian/obsidian.json` 文件启用官方 CLI 功能
- 通过 ACL 来控制对数据存储库的访问权限
- 包含 `/usr/local/bin/obs` 这一用于启动 CLI 的封装脚本
- 对 `help`、`vault`、`daily:path`、`daily:append`、`daily:read` 和 `search` 等 CLI 命令的验证

## 不应做的事情

- 不要将此技能用于 `notesmd-cli` 或仅支持 Markdown 格式的简单工作流程。
- 除非用户明确要求，否则不要扩展到插件开发、同步设置、主题定制或完整的桌面环境配置等方面。
- 不要过度放宽用户权限。

## 封装脚本（Wrapper）的设计原则

封装脚本应能够确保以下功能正常运行：

```bash
su - obsidian -c 'cd <vault> && xvfb-run -a /usr/bin/obsidian --disable-gpu ...'
```

这是在无头环境下稳定的运行模式。

## 验证命令

至少需要执行以下验证命令：

```bash
obs help
obs vault
obs daily:path
obs daily:append content="skill verification"
obs daily:read
obs search query="skill verification"
```

## 参考资料

- 当需要了解非 root 用户权限、`Xvfb` 显示器软件、ACL 的使用方式或封装脚本设计原理时，请阅读 `references/architecture.md`。
- 如果安装过程完成但 CLI 行为仍然存在问题，请参阅 `references/troubleshooting.md`。

## 报告格式

报告内容应简洁明了，包括以下信息：
- 安装的 Obsidian CLI 版本
- 使用的封装脚本路径
- 当前激活的数据存储库路径
- 已验证的 CLI 命令列表
- 仍然存在的使用限制或注意事项