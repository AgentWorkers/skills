---
name: padel
description: 通过 paddle CLI 检查帕德尔球场的可用性并管理预订。
metadata: {"moltbot":{"nix":{"plugin":"github:joshp123/padel-cli","systems":["aarch64-darwin","x86_64-linux"]},"config":{"requiredEnv":["PADEL_AUTH_FILE"],"stateDirs":[".config/padel"],"example":"config = { env = { PADEL_AUTH_FILE = \"/run/agenix/padel-auth\"; }; stateDirs = [ \".config/padel\" ]; };"},"cliHelp":"Padel CLI for availability\n\nUsage:\n  padel [command]\n\nAvailable Commands:\n  auth         Manage authentication\n  availability Show availability for a club on a date\n  book         Book a court\n  bookings     Manage bookings history\n  search       Search for available courts\n  venues       Manage saved venues\n\nFlags:\n  -h, --help   help for padel\n  --json       Output JSON\n\nUse \"padel [command] --help\" for more information about a command.\n"}}
---

# 帕德尔球（Padel）预订技能

## 命令行界面（CLI）

```bash
padel  # On PATH (moltbot plugin bundle)
```

## 场地选择

请按照优先级使用已配置的场地列表。如果未配置任何场地，请提供场地名称或位置。

## 命令

### 查看下一个预订信息
```bash
padel bookings list 2>&1 | head -3
```

### 查询场地可用性
```bash
padel search --venues VENUE1,VENUE2 --date YYYY-MM-DD --time 09:00-12:00
```

## 回复指南

- 回复内容应简洁明了。
- 使用 🎾 表情符号。
- 回复结尾应包含明确的行动建议。

## 权限控制

只有经过授权的预订人员才能确认预订。如果请求者没有相应权限，请让授权用户进行确认。