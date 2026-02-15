---
name: post-at
description: 管理奥地利邮政（post.at）的配送服务：查询包裹信息、查看配送状态、设置配送地址偏好。
homepage: https://github.com/krausefx/post-at-cli
metadata: {"clawdbot":{"emoji":"📦","requires":{"bins":["node"]}}}
---

# post-at CLI

这是一个非官方的命令行工具（CLI），用于查看和管理奥地利邮政（Österreichische Post）的包裹投递信息。该工具使用与网站相同的交互流程，因此需要您自己的账户凭据。

**凭据：**  
`POST_AT_USERNAME` 和 `POST_AT_PASSWORD` 环境变量（或 `--username` / `--password` 选项）。

## 快速参考

### 登录  
（会缓存一个短期的会话令牌，该令牌会自动过期）：  
```bash
post-at login
# Output: Logged in as you@example.com
```

### 列出投递信息  
- 即将投递的包裹（默认显示）：  
```bash
post-at deliveries
# Shows: tracking number, ETA, sender, status
```  
- 所有已投递的包裹：  
```bash
post-at deliveries --all
```  
（输出格式为 JSON）：  
```bash
post-at deliveries --json
```  
（可限制显示结果的数量）：  
```bash
post-at deliveries --limit 10
```

### 查看包裹详情  
- 根据具体的追踪号码获取包裹详情：  
```bash
post-at delivery 1042348411302810212306
# Output: tracking, expected delivery, sender, status, picture URL
```  
（输出格式为 JSON）：  
```bash
post-at delivery <tracking-number> --json
```

### 投递地点选择（Wunschplatz）  
- 列出可用的投递地点选项：  
```bash
post-at routing place-options
```  
- 常见选项：  
  - `Vor_Haustüre`（在住宅门前）  
  - `Vor_Wohnungstüre`（在公寓门前）  
  - `AufOderUnter_Briefkasten`（放在/在邮箱下方）  
  - `Hinter_Zaun`（在围栏后面）  
  - `In_Garage`（在车库内）  
  - `Auf_Terrasse`（在阳台上）  
  - `Im_Carport`（在车棚内）  
  - `In_Flexbox`（在储物箱内）  
  - `sonstige`（其他指定地点）  

### 设置投递地点  
- 使用预设的快捷方式：  
```bash
post-at routing place <tracking-number> \
  --preset vor-der-wohnungstuer \
  --description "Please leave at the door"
```  
- 直接使用地址：  
```bash
post-at routing place <tracking-number> \
  --key Vor_Wohnungstüre \
  --description "Bitte vor die Wohnungstür"
```  
- 使用标签进行指定：  
```bash
post-at routing place <tracking-number> \
  --place "Vor der Wohnungstüre" \
  --description "Custom instructions"
```

## 示例用法  

- 查看今天/明天的投递信息：  
```bash
post-at deliveries
```  
- 获取包含包裹照片的完整详情：  
```bash
post-at delivery <tracking-number>
```  
- 将所有即将投递的包裹设置为“门前”（Vor der Haustüre）：  
```bash
# First list deliveries
post-at deliveries --json > /tmp/deliveries.json

# Then set place for each (requires scripting)
# Example for a specific one:
post-at routing place 1042348411302810212306 \
  --preset vor-der-wohnungstuer \
  --description "Leave at apartment door"
```

## 注意事项：  
- 会话令牌会在一段时间后过期，需要重新登录。  
- 并非所有包裹都支持用户指定的投递地点。  
- 并非所有包裹的图片链接都可用。  
- 如需进行程序化处理，请使用 `--json` 选项输出数据。