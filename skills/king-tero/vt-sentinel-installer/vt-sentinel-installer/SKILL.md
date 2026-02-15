---
name: install-vt-sentinel
description: >-
  Install or upgrade VT Sentinel security plugin. Use when the user asks to install,
  set up, enable, update, or upgrade VT Sentinel, VirusTotal scanning, malware protection,
  or file security scanning. Handles fresh installs and upgrades from any previous version.
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

# 安装/升级 VT Sentinel 插件

## 第一步：检查当前状态

```
exec { "command": "openclaw plugins list 2>/dev/null | grep vt-sentinel" }
```

确定操作系统平台：

```
exec { "command": "uname -s 2>/dev/null || echo Windows" }
```

可能有以下三种结果：
- **未安装** → 转到第二步（全新安装）
- **已安装，但版本较旧** → 转到第三步（升级）
- **已安装，且版本为 v0.8.0 或更高** → 告知用户插件已是最新版本，跳过后续步骤

要检查已安装的插件版本：
```
exec { "command": "node -e \"const p=require(process.env.HOME+'/.openclaw/extensions/openclaw-plugin-vt-sentinel/package.json');console.log(p.version)\" 2>/dev/null || echo unknown" }
```

在 Windows 上，请使用 `%USERPROFILE%` 而不是 `$HOME`。

## 第二步：全新安装

```
exec { "command": "openclaw plugins install openclaw-plugin-vt-sentinel" }
```

此步骤会下载 npm 包，自动注册插件，并加载相关功能。无需手动配置。直接进入第四步。

## 第三步：从旧版本升级

`openclaw plugins install` 命令不支持原地升级（会提示“插件已存在”错误）。升级步骤如下：

### 3a. 删除旧插件目录（保留所有用户数据）

在 Linux/macOS 上：
```
exec { "command": "rm -rf ~/.openclaw/extensions/openclaw-plugin-vt-sentinel" }
```

在 Windows 上：
```
exec { "command": "rmdir /s /q %USERPROFILE%\\.openclaw\\extensions\\openclaw-plugin-vt-sentinel" }
```

**用户数据是安全的**——这些数据存储在插件目录之外，不会被删除：
- `~/.openclaw/vt-sentinel-state.json`（配置覆盖信息、启动标志）
- `~/.openclaw/vt-sentinel-uploads.log`（审计日志）
- `~/.openclaw/vt-sentinel-detections.log`（审计日志）
- `~/.openclaw/vtai-agent-credentials.json`（VTAI API 凭据）

### 3b. 清除旧的插件安装记录（保留用户配置）

删除旧插件目录后，`openclaw.json` 中的 `plugins.installs` 部分仍会引用旧插件的路径，从而导致验证错误。只需删除旧的安装记录，用户配置（如 API 密钥等）会保留：
在 Linux/macOS 上：
```
exec { "command": "node -e \"const fs=require('fs'),p=process.env.HOME+'/.openclaw/openclaw.json';try{const P=(()=>{try{return require('json5').parse}catch{return JSON.parse}})();const c=P(fs.readFileSync(p,'utf8'));if(c.plugins?.installs)delete c.plugins.installs['openclaw-plugin-vt-sentinel'];fs.writeFileSync(p,JSON.stringify(c,null,2));console.log('Config cleaned')}catch(e){console.log('No config to clean: '+e.message)}\"" }
```

在 Windows 上：
```
exec { "command": "node -e \"const fs=require('fs'),p=process.env.USERPROFILE+'\\\\.openclaw\\\\openclaw.json';try{const P=(()=>{try{return require('json5').parse}catch{return JSON.parse}})();const c=P(fs.readFileSync(p,'utf8'));if(c.plugins?.installs)delete c.plugins.installs['openclaw-plugin-vt-sentinel'];fs.writeFileSync(p,JSON.stringify(c,null,2));console.log('Config cleaned')}catch(e){console.log('No config to clean: '+e.message)}\"" }
```

### 3c. 安装新版本

```
exec { "command": "openclaw plugins install openclaw-plugin-vt-sentinel" }
```

如果在 Windows 上安装失败（出现 `spawn EINVAL` 错误），请使用手动方法：
```
exec { "command": "cd %TEMP% && npm pack openclaw-plugin-vt-sentinel && mkdir %USERPROFILE%\\.openclaw\\extensions\\openclaw-plugin-vt-sentinel && tar xzf openclaw-plugin-vt-sentinel-0.7.0.tgz -C %USERPROFILE%\\.openclaw\\extensions\\openclaw-plugin-vt-sentinel --strip-components=1 && cd %USERPROFILE%\\.openclaw\\extensions\\openclaw-plugin-vt-sentinel && npm install --omit=dev" }
```

## 第四步：重启网关

插件只有在网关重启后才会生效。根据操作系统平台，执行相应的重启命令：

- Linux：
```
exec { "command": "systemctl --user restart openclaw-gateway.service" }
```

- macOS：
```
exec { "command": "openclaw gateway restart" }
```

- Windows：
```
exec { "command": "openclaw gateway restart" }
```

## 第五步：验证插件是否正确安装

重启后，确认插件已成功加载，并且能够使用以下 7 个功能：
```
exec { "command": "openclaw plugins list 2>/dev/null | grep vt-sentinel" }
```

## 第六步：通知用户

告知用户：
1. VT Sentinel 已成功安装并处于激活状态（如果进行了升级，请说明是从哪个版本升级的）。
2. **无需 API 密钥**——插件会自动注册到 VirusTotal 的 AI API（无需任何配置）。
3. 用户可以选择通过 `openclaw plugins config openclaw-plugin-vt-sentinel apiKey <key>` 添加自己的 VirusTotal API 密钥，以获得更高的请求速率限制。

VT Sentinel 提供以下功能：
- `vt_scan_file`：全文件扫描（包含反病毒检测和 AI 代码分析）
- `vt_check_hash`：快速哈希查询
- `vt_upload_consent`：允许用户上传敏感文件
- `vt_sentinel_status`：查看当前配置、监控目录和保护状态
- `vt_sentinel_configure`：运行时修改设置（预设、通知级别、阻止模式）
- `vt_sentinel_reset_policy`：重置为默认设置
- `vt_sentinel_help`：快速入门指南和隐私政策
- 自动扫描下载或创建的文件
- 活动阻止恶意文件的执行和危险命令模式

## 故障排除

如果 `openclaw plugins install` 命令失败：
- 检查网络连接：`exec { "command": "npm ping" }`
- 尝试使用详细输出模式：`exec { "command": "openclaw plugins install openclaw-plugin-vt-sentinel --verbose" }`
- 在 Windows 上，如果出现 `spawn EINVAL` 错误，请使用第三步中的手动方法。

## 注意事项：
- **切勿手动修改 `openclaw.json`**——`openclaw plugins install` 会自动处理所有配置。
- 如果用户报告插件被阻止，请检查其 `openclaw.json` 文件中的 `plugins.deny` 配置项。