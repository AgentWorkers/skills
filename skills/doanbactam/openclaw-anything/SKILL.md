---  
**名称：OpenClaw**  
**描述：** OpenClaw 是一个命令行界面（CLI）包装器，用于管理 OpenClaw 的各种功能，包括网关、通道、模型、自动化流程以及操作工作流。同时，它还提供了相应的文档支持。  

---

# OpenClaw 技能包  
这是一个用于通过终端操作 OpenClaw 的本地技能包。  
该仓库本身不会安装任何平台依赖项，它仅对 `openclaw` CLI 进行封装，并提供与 `https://docs.openclaw.ai` 对齐的本地参考文档。  

## 功能范围  
- 安装与入门流程  
- 网关的生命周期管理及健康检查  
- 通道连接管理  
- 模型列表、身份验证及别名设置  
- 定时自动化任务及浏览器工具  
- 插件管理  
- 部署相关操作（Docker、Nix、更新、回滚）  

## 先决条件  
**必需条件：**  
- `openclaw` CLI 已添加到系统的 `PATH` 环境变量中。  

**常见的外部先决条件（取决于具体功能）：**  
- Node.js 及 npm（用于官方文档中的安装/更新操作）  
- Playwright 系统依赖项（用于浏览器工具）  
- 平台特定的工具（例如 macOS 的 iMessage 通道管理工具 `imsg`）  
- 如果需要远程访问节点，则需配置私有网络（如 Tailscale）。  

**OpenClaw 运行时使用的环境变量：**  
- `OPENCLAW_CONFIG_PATH`  
- `OPENCLAW_STATE_DIR`  
- `OPENCLAW_HOME`  

## 安全限制  
**默认安全策略：** 最小权限原则。  

**允许的操作：**  
- 仅限读取状态信息及进行诊断性操作（`status`、`doctor`、`version`、`gateway status`、`gateway health`）  
- 配置检查及非破坏性的操作检查  

**高风险操作（需用户明确授权）：**  
- 随意执行 shell 命令（上游运行时中的 `exec` 工具）  
- 提升系统权限  
- 生成或委托执行子代理  
- 从不受信任的来源安装插件  
- 创建/修改 Cron 任务  
- 对远程网站进行浏览器自动化操作  
- 设备配对及访问传感器（摄像头、音频、位置信息）  

**高风险操作的启用选项：**  
- 对于涉及高风险操作的命令，需要设置 `OPENCLAWWRAPPER_ALLOW_RISKY=1`。  

## 本仓库的注意事项：**  
- 本仓库不是 OpenClaw 的运行时源代码。  
- 本仓库不会自动配置系统软件包。  
- 本仓库不负责管理主机网络、VPN 或移动操作系统的权限设置。  
- 本仓库不支持自主执行具有高权限的操作。  

## 统一命令工具  
**主要包装脚本：** `bash scripts/openclaw.sh [command] [args]`  

### 命令映射  
该包装器将用户输入的命令映射到 OpenClaw 的官方命令：  
- `install|setup|doctor|status|reset|version|tui|dashboard`  
  - 直接传递给 `openclaw` 执行。  
- `service ...`  
  - `openclaw gateway service ...`  
- `channel login <name>`  
  - `openclaw channels login --channel <name>`  
- `channel list`  
  - `openclaw channels list`  
- `channel logout <name>`  
  - `openclaw channels logout --channel <name>`  
- `channel pairing`  
  - `openclaw pairing`（需启用高风险操作）  
- `model auth ...`  
  - `openclaw models auth ...`  
- `model alias ...`  
  - `openclaw models aliases ...`  
- `model scan|list|set ...`  
  - `openclaw models ...`  
- `cron ...`  
  - `openclaw cron ...`（需启用高风险操作）  
- `browser ...`  
  - `openclaw browser ...`（需启用高风险操作）  
- `plugin ...`  
  - `openclaw plugins ...`（需启用高风险操作）  
- `msg ...`  
  - `openclaw message send ...`  
- `prose ...`  
  - 启用 `open-prose` 插件（需启用高风险操作）  

## 文档说明：**  
- `references/security-policy.md`：安全策略与审批流程  
- `references/prerequisites.md`：依赖项及功能限制  
- `references/cli-full.md`：所有 CLI 命令的详细说明  
- `references/config-schema.md`：配置与环境变量的参考信息  
- `references/nodes-platforms.md`：关于不同平台及 Node.js 的使用说明  
- `references/deployment.md`：Docker、Nix、更新及回滚操作指南  
- `references/advanced-tools.md`：插件、浏览器工具及网关辅助功能  
- `references/hubs.md`：相关文档的链接集合  

## 维护信息：**  
- 最后一次文档更新时间：2026-02-17  
- 官方文档来源：`https://docs.openclaw.ai`