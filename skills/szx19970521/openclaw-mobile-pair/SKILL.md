---
name: openclaw-mobile-pair
description: 一键生成 OpenClaw 手机控制中心连接码（自动读取本机 gateway token）
user-invocable: true
---
# OpenClaw 移动配对功能

使用此功能为 OpenClaw 控制应用的用户生成移动配对码。

## 工作流程

1. 仅在用户未提供 `BFF` URL 时请求该 URL。
2. 运行 `scripts/generate-mobile-pairing.ps1` 命令以生成配对码。
3. 返回以下信息：
   - 配对码
   - 输出文件的路径
   - 移动用户的下一步操作建议

## 命令模板

```powershell
powershell -ExecutionPolicy Bypass -File scripts/generate-mobile-pairing.ps1 -BffBaseUrl "<https://api.yourdomain.com/>" -CopyToClipboard
```

## 响应方式

- 保持响应简洁明了，便于用户操作。
- 如果生成失败，请说明具体原因及解决方法。