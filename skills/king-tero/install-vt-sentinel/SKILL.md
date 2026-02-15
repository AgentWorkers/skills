---
name: install-vt-sentinel
description: >-
  Install VT Sentinel security plugin. Use when the user asks to install,
  set up, or enable VT Sentinel, VirusTotal scanning, malware protection,
  or file security scanning. Single command installation, zero configuration.
user-invocable: true
metadata:
  openclaw:
    emoji: "\U0001F6E1\uFE0F"
    requires:
      anyBins:
        - npm
        - pnpm
        - yarn
        - bun
---

# 安装 VT Sentinel 插件

## 第一步：检查是否已安装

```
exec { "command": "openclaw plugins list 2>/dev/null | grep -q vt-sentinel && echo INSTALLED || echo NOT_INSTALLED" }
```

如果显示“已安装”（INSTALLED），则说明 VT Sentinel 已经处于激活状态，可以直接跳过后续所有步骤。

## 第二步：安装插件

```
exec { "command": "openclaw plugins install openclaw-plugin-vt-sentinel" }
```

此命令会下载 npm 包，自动注册插件，并加载相关功能及钩子。无需进行任何手动配置。

## 第三步：重启网关

插件只有在网关重启后才会生效。请在安装完成后立即执行重启操作：

```
exec { "command": "openclaw gateway restart" }
```

## 第四步：验证插件是否正确加载

重启后，请确认插件是否已成功加载：

```
exec { "command": "openclaw plugins list 2>/dev/null | grep vt-sentinel" }
```

## 第五步：通知用户

请告知用户以下信息：
1. VT Sentinel 已成功安装并处于激活状态。
2. **无需 API 密钥**——该插件会自动使用 VirusTotal 的 AI API 进行检测（无需任何额外配置）。
3. （可选）用户可以通过以下方式添加自己的 VirusTotal API 密钥以提升检测速率：
   - 在 `openclaw plugins config openclaw-plugin-vt-sentinel apiKey <key>` 中设置；
   - 或者在 `openclaw.json` 文件的 `plugins.entries.openclaw-plugin-vt-sentinel.config.apiKey` 中配置。

VT Sentinel 提供以下功能：
- `vt_scan_file`：全文件扫描（包含病毒检测和 AI 代码分析）
- `vt_check_hash`：快速哈希值查询
- `vt_upload_consent`：对敏感文件的上传进行权限控制
- 自动扫描新下载或创建的文件
- 活动阻止恶意文件的执行及危险命令模式的运行

## 故障排除

如果 `openclaw plugins install` 命令执行失败，请检查网络连接是否正常：`exec { "command": "npm ping" }`
- 或者尝试手动执行 `npm install` 命令：`exec { "command": "openclaw plugins install openclaw-plugin-vt-sentinel --verbose" }`

## 注意事项：
- **严禁** 手动修改 `openclaw.json` 文件——`openclaw plugins install` 会自动处理所有配置任务。
- 如果用户报告插件被阻止，请检查其 `openclaw.json` 文件中的 `plugins.deny` 配置项。