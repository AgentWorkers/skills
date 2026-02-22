---  
**名称：OpenClaw**  
**描述：** OpenClaw 是一个用于管理网关、通道、模型、自动化流程及操作工作流的 CLI（命令行工具）包装层，同时提供相应的文档支持。  

---

# OpenClaw 技能包  
这是一个用于通过终端操作 OpenClaw 的本地技能包。该仓库本身不会安装任何平台依赖项，它仅对 `openclaw` CLI 进行封装，并提供与 `https://docs.openclaw.ai` 对齐的本地参考文档。  

## 功能范围  
- 安装与入门流程  
- 网关的生命周期管理及健康检查  
- 通道连接管理  
- 模型列表、身份验证及别名设置  
- 定时自动化任务及浏览器工具支持  
- 插件管理  
- 部署相关操作（Docker、Nix、更新、回滚等）  

## 先决条件  
**必需条件：**  
- `openclaw` CLI 已添加到系统的 `PATH` 环境变量中。  

**常见的外部依赖项（具体取决于功能）：**  
- Node.js 及 npm（用于官方文档中的安装/更新操作）  
- Playwright（用于浏览器自动化工具）  
- 平台特定的工具（例如 macOS 的 iMessage 通道相关工具 `imsg`）  
- 如果需要远程访问节点，则需配置私有网络环境（如 Tailscale）。  

**OpenClaw 运行时使用的环境变量：**  
- `OPENCLAW_CONFIG_PATH`  
- `OPENCLAW_STATE_DIR`  
- `OPENCLAW_HOME`  

## 安全限制  
**默认安全策略：** 最小权限原则。  

**默认允许的操作：**  
- 仅允许读取状态信息及进行诊断操作（`status`、`doctor`、`version`、`gateway status`、`gateway health`）  
- 配置检查及非破坏性的操作。  

**高风险操作（需用户明确授权）：**  
- 任意 shell 命令的执行（上游运行时中的 `exec` 工具）  
- 权限提升操作  
- 从不可信来源安装插件  
- 创建或修改 Cron 任务  
- 针对远程网站的浏览器自动化操作  
- 设备配对及传感器数据访问（摄像头、音频、位置信息）  

**高风险操作的启用方式：**  
需要将 `OPENCLAW Wrapper_ALLOW_RISKY` 环境变量设置为 `1` 才能执行相关命令。  

## 本仓库不涉及的内容：**  
- OpenClaw 的运行时源代码  
- 系统包的自动配置  
- 主机网络配置、VPN 设置或移动操作系统的权限管理  
- 自动执行高权限操作的授权  

## 统一命令工具  
**主要包装脚本：**  
`bash scripts/openclaw.sh [command] [args]`  

### 命令映射  
该包装层将用户输入的命令映射到官方的 `openclaw` 命令：  
- `install|setup|doctor|status|reset|version|tui|dashboard`  
  - 直接传递给 `openclaw` 执行  
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
- `references/config-schema.md`：配置参数与环境变量的参考信息  
- `references/nodes-platforms.md`：平台与节点相关的注意事项  
- `references/deployment.md`：Docker、Nix、更新、回滚等部署相关内容  
- `references/advanced-tools.md`：插件、浏览器工具及网关辅助功能  
- `references/hubs.md`：相关文档的链接集合  

## 维护信息：**  
- 最后一次文档更新：2026-02-17  
- 官方文档来源：`https://docs.openclaw.ai`