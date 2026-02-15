---
name: lastpass-cli
description: 通过 `lpass` CLI 安全地从 LastPass 保管库中获取凭证。
version: 0.1.0
tags: [security, passwords, lastpass]
---

# LastPass CLI 技能

## 描述

此技能允许代理通过 `lpass` CLI 从本地的 LastPass 保管库中检索凭证。它主要用于将凭证导入自动化流程中，而非用于交互式的保管库管理。

## 工具

- `lastpass_get_secret`：使用本地的 `lpass` CLI 检索指定 LastPass 条目的特定字段（密码、用户名或备注）。

## 适用场景

- 当您需要获取存储在 LastPass 中的某个账户的密码、用户名或备注时。
- 在执行部署、API 调用或需要使用凭证的登录操作时。

## 工具：lastpass_get_secret

### 使用方法

使用以下 JSON 对象调用此工具：

```json
{
  "name": "具体的 LastPass 条目名称",
  "field": "password | username | notes | raw"
}
```