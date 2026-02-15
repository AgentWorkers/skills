---
name: comfyui-request
description: 向 ComfyUI 发送一个工作流请求，并返回图像结果。
metadata: {"clawdbot":{"emoji":"🧩","requires":{"bins":["node","curl"]},"entry":"bin/cli.js"}}
---

# comfyui-request

## 功能
向正在运行的 ComfyUI 实例发送工作流请求，并返回生成的图像 URL 或 Base64 数据。

## 配置参数
- `COMFYUI_HOST`: ComfyUI 服务器的主机/IP 地址（默认值：`192.168.179.111`）。
- `COMFYUI_PORT`: ComfyUI 服务器的端口号（默认值：`28188`）。
- `COMFYUI_USER`: 可选的基本认证用户名。
- `COMFYUI_PASS`: 可选的基本认证密码。

这些配置参数可以通过环境变量或技能目录中的 `.env` 文件进行设置。

## 使用方法
```json
{
  "action": "run",
  "workflow": { ... }   // JSON workflow object
}
```

该技能会向 `http://{host}:{port}/run` 发送 POST 请求，并返回响应的 JSON 数据。

## 示例
```json
{
  "action": "run",
  "workflow": {
    "nodes": [ ... ],
    "edges": [ ... ]
  }
}
```

## 注意事项
该技能要求 ComfyUI 服务器提供 `/run` 端点，并返回一个包含 `image` 字段的 JSON 对象，该字段的值应为图像的 URL 或 Base64 字符串。