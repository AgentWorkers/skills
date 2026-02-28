---

**名称：OpenClaw**  
**描述：** OpenClaw 是一个命令行界面（CLI）封装工具，提供了对 OpenClaw 功能的统一访问接口，包括通道管理、模型操作、代理管理、节点控制、浏览器功能、内存管理、安全设置以及自动化任务等。

---

# OpenClaw 功能概述  
OpenClaw 是一个 CLI 工具，同时附带了相应的文档。它本身并不包含 OpenClaw 的运行时源代码。该工具封装了 `openclaw` CLI 的命令，并提供了与官方文档（`https://docs.openclaw.ai`）一致的本地参考文档。

## 先决条件  
- `openclaw` CLI 必须已添加到系统的 `PATH` 环境变量中。  
- 推荐安装 Node.js（用于处理相关流程）以及 Playwright（用于浏览器自动化）和 Tailscale（用于远程节点管理，可选）。

## 快速参考  
| 功能需求 | 对应文档文件 |  
|------|------|  
| 查找命令 | `references/cli-full.md`（通过关键词搜索） |  
| 安全策略 | `references/security-policy.md` |  
| 配置语法 | `references/config-schema.md` |  
| 部署/更新 | `references/deployment.md` |  
| 平台说明 | `references/nodes-platforms.md` |  
| 文档链接 | `references/hubs.md` |  

## 全局参数  
`--dev` `--profile <name>` `--no-color` `--json` `-V`  

## 安全模型  
默认安全策略为“最小权限原则”：高风险操作需要逐条获得明确批准。  

### 低风险操作（默认权限）  
- 查看状态  
- 列出节点信息  
- 检查节点健康状况  
- 查看日志  
- 读取配置文件  
- 搜索文档  
- 搜索内存相关数据  

### 高风险操作（需设置 `OPENCLAW_WRAPPER_ALLOW_RISKY=1`）  
- 执行 Shell 命令  
- 调用/运行远程节点  
- 操作摄像头/屏幕/位置信息  
- 进行浏览器自动化操作  
- 修改 cron 任务  
- 安装插件/钩子  
- 配置设备连接  
- 应用敏感信息  
- 重新创建沙箱环境  
- 设置 Webhook  
- 配置 DNS 服务  

**使用方式：**  
`bash scripts/openclaw.sh <命令> [参数]`  

**权限控制机制：**  
- 插件相关的操作仅限于安装/启用；  
- 敏感信息操作仅限于应用；  
- 沙箱环境仅限于重新创建。  

## 其他说明：**  
- OpenClaw 不包含 OpenClaw 的运行时源代码。  
- 该工具不负责系统包的安装或管理。  
- 也不负责网络配置或 VPN 的管理。  
- 该工具不支持自主执行具有高权限的操作。  

---

**最后更新时间：** 2026-02-27  
**来源：** `https://docs.openclaw.ai`