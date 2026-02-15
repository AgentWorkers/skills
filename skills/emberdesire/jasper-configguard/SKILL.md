---
name: jasper-configguard
version: 1.0.0
description: OpenClaw的安全配置更改功能支持自动回滚机制：在应用配置更新前会进行备份，重启后会对系统状态进行检查；如果配置更新失败，系统会自动恢复到之前的配置状态。可用命令包括：`patch`（应用配置更新）、`restore`（恢复到备份配置）、`list`（列出所有配置项）、`diff`（显示配置差异）、`validate`（验证配置合法性）、`doctor`（检查系统健康状况）。
---

# Jasper ConfigGuard v1.0.0

这是一个用于 OpenClaw 的安全配置管理工具，支持自动回滚功能，确保您的网关配置不会出错。

## 设置

```bash
npm install -g jasper-configguard
```

## 使用方法

### 安全地应用配置更改

```bash
jasper-configguard patch '{"gateway":{"bind":"tailnet"}}'
```

该工具将执行以下操作：
1. 备份当前的配置文件
2. 应用配置更改（采用深度合并方式）
3. 重启网关
4. 等待网关的健康检查结果
5. 如果网关出现故障，会自动回滚到之前的配置状态

### 预览配置更改

```bash
jasper-configguard patch --dry-run '{"agents":{"defaults":{"model":{"primary":"opus"}}}}'
```

### 从备份中恢复配置

```bash
jasper-configguard restore
```

### 查看所有备份记录

```bash
jasper-configguard list
```

### 检查网关状态

```bash
jasper-configguard doctor
```

## 代理集成

您可以通过代理程序安全地修改 OpenClaw 的配置：

```bash
# Safe model switch
jasper-configguard patch '{"agents":{"defaults":{"model":{"primary":"anthropic/claude-opus-4-5"}}}}'

# Enable a plugin safely
jasper-configguard patch '{"plugins":{"entries":{"my-plugin":{"enabled":true}}}}'

# If something breaks, restore
jasper-configguard restore
```

## API

```javascript
const { ConfigGuard } = require('jasper-configguard');
const guard = new ConfigGuard();

// Safe patch
const result = await guard.patch({ gateway: { bind: 'tailnet' } });
if (!result.success) console.log('Rolled back:', result.error);

// Dry run
const preview = guard.dryRun({ agents: { defaults: { model: { primary: 'opus' } } } });
console.log(preview.diff);
```