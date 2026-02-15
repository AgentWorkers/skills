# Gateway Manager

## 描述
该组件负责处理来自 Feishu 的管理菜单事件，以管理 OpenClaw Gateway 服务。支持远程重启、状态监控和系统诊断功能。

## 命令
- **Restart Gateway** (`restart_gateway`): 重启 OpenClaw Gateway 服务（仅限主节点）。
- **Status** (`status_gateway`): 返回 Gateway 的当前状态（活跃/非活跃）。
- **System Info** (`system_info`): 显示服务器指标（内存、运行时间、节点版本）。
- **Test Button** (`test_menu_button`): 触发测试响应（Cute Mode 模式）。

## 安全性
- 关键操作（如重启）仅限于在 `USER.md` 中定义的授权主节点才能执行。
- 对未经授权的访问尝试会提供反馈。

## 配置
- 自动查找 `USER.md` 文件以进行身份验证。
- 使用 `feishu-card` 功能提供详细的反馈信息。