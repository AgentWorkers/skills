---
name: gws-groupssettings
version: 1.0.0
description: "管理 Google 群组的设置。"
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    cliHelp: "gws groupssettings --help"
---
# groupssettings (v1)

> **前提条件：** 需要阅读 `../gws-shared/SKILL.md` 以了解认证信息、全局标志和安全规则。如果这些内容缺失，请运行 `gws generate-skills` 命令来生成它们。

```bash
gws groupssettings <resource> <method> [flags]
```

## API 资源

### groups

  - `get` — 根据 ID 获取一个资源。
  - `patch` — 更新现有资源。该方法支持补丁（patch）语法。
  - `update` — 更新现有资源。

## 查找命令

在调用任何 API 方法之前，请先查看其文档：

```bash
# Browse resources and methods
gws groupssettings --help

# Inspect a method's required params, types, and defaults
gws schema groupssettings.<resource>.<method>
```

使用 `gws schema` 的输出来构建你的 `--params` 和 `--json` 标志。