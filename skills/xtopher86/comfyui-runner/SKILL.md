---
name: comfyui-runner
description: ComfyUI实例的启动/停止/状态控制
metadata: {"clawdbot":{"emoji":"🧩","requires":{"bins":["node","curl"]},"entry":"bin/cli.js"}}
---

# comfyui-runner

## 功能
用于启动、停止以及检查本地 ComfyUI 实例的状态。

## 配置参数
- `COMFYUI_HOST`: ComfyUI 服务器的主机/IP 地址（默认值：`192.168.179.111`）。
- `COMFYUI_PORT`: ComfyUI 服务器的端口号（默认值：`28188`）。
- `COMFYUI_USER`: 基本认证所需的用户名（可选）。
- `COMFYUI_PASS`: 基本认证所需的密码（可选）。

这些配置参数可以通过环境变量或技能目录下的 `.env` 文件来设置。

## 使用方法
```json
{
  "action": "run" | "stop" | "status"
}
```

- `run`：如果 ComfyUI 服务器尚未运行，则启动该服务器。
- `stop`：停止 ComfyUI 服务器。
- `status`：返回服务器是否可访问的状态。

## 示例
```json
{"action": "status"}
```

## 注意事项
本技能假定 ComfyUI 可执行文件位于系统的 PATH 环境变量中，或者与技能文件位于同一目录下。它使用 `curl` 命令来检测 `/health` 端点的响应情况。