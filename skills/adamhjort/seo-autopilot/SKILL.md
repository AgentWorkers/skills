---
name: seo-autopilot
description: 为 boll-koll.se 或 hyresbyte.se 运行本地 SEO 自动化工具，并返回 PR 链接及相应的总结。
allowed-tools:
  - exec
metadata:
  triggers:
    - "seo"
    - "seo boll-koll.se"
    - "seo hyresbyte.se"
  allowed_sites:
    - boll-koll.se
    - hyresbyte.se
  command:
    - scripts/run.sh
license: MIT
---

# seo-autopilot

## 使用方法（通过 WhatsApp 或聊天工具）
- 输入 `seo` 命令
- 输入 `seo boll-koll.se` 命令
- 输入 `seo hyresbyte.se` 命令

默认访问的网站：`boll-koll.se`

## 安全性设置
仅允许访问 `boll-koll.se` 和 `hyresbyte.se` 网站。  
严禁执行任意命令，仅允许执行以下操作：  
`scripts/run.sh <site>`

## 动作流程：
1. 从接收到的消息中解析目标网站地址，默认为 `boll-koll.se`。
2. 如果目标网站不在允许访问的列表中，系统将拒绝请求。
3. 执行 `scripts/run.sh <site>` 命令。
4. 从标准输出（stdout）中提取与 PR 相关的 URL（以 “PR:” 开头的行）。
5. 如果仓库中存在 `SEO_REPORT.md` 文件，将在回复中包含该文件中的前三条检测结果。