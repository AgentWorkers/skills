---
name: glab-auth
description: **用途：**  
用于设置或管理 GitLab CLI（glab）的认证。涵盖登录、登出、状态查询、Docker 辅助工具以及相关的认证命令。
---

# glab auth

用于管理 glab 的认证状态。

## 使用场景

- 首次设置 GitLab CLI 的认证信息
- 更新或切换账户
- 检查认证状态
- 配置用于 GitLab 注册表的 Docker 认证辅助工具

## 快速入门

1) 登录：
```bash
glab auth login
```

2) 检查状态：
```bash
glab auth status
```

3) 注销：
```bash
glab auth logout
```

## 子命令

有关子命令的详细信息和使用说明，请参阅 [references/commands.md](references/commands.md)：
- `login`：登录
- `logout`：注销
- `status`：检查状态
- `configure-docker`：配置 Docker 认证
- `docker-helper`：配置 Docker 认证辅助工具
- `dpop-gen`：生成 DPOP 令牌