---
name: email-reader
version: "2.0.0"
description: 使用 gog CLI 从 Gmail（所有文件夹/标签）中读取电子邮件。当用户需要查看邮件、阅读收件箱内容、显示未读邮件、列出文件夹、搜索邮件或从任何 Gmail 标签中获取邮件时，可以使用此工具。
homepage: https://gogcli.sh
metadata:
  clawdbot:
    emoji: "📥"
    requires:
      bins: ["gog"]
      env:
        - name: GOG_ACCOUNT
          description: "Tu dirección de Gmail, ej: tu@gmail.com"
    install:
      - id: brew
        kind: brew
        formula: steipete/tap/gogcli
        bins: ["gog"]
        label: "Install gog CLI (brew)"
---
# 电子邮件阅读器

使用 `gog` CLI 读取 Gmail 中的邮件。需要先配置 `gog auth`。如果尚未配置，请先执行设置步骤。

## 初始设置（仅执行一次）

```bash
gog auth credentials /ruta/a/client_secret.json
gog auth add $GOG_ACCOUNT --services gmail
gog auth list   # verificar que quedó bien
```

## 使用场景

- “查看我的邮件”
- “我有哪些新邮件？”
- “显示今天的未读邮件”
- “阅读 Juan 的邮件”
- “查找关于 Q1 提案的邮件”
- “我有多少垃圾邮件？”
- “显示 [主题] 的邮件列表”
- “阅读 ‘客户’ 文件夹中的邮件”

## 主要命令

### 阅读收件箱（最近收到的邮件）
```bash
gog gmail search 'in:inbox newer_than:1d' --max 20 --json
gog gmail search 'in:inbox is:unread' --max 50 --json
gog gmail search 'in:inbox newer_than:7d' --max 100 --json
```

### 阅读垃圾邮件
```bash
gog gmail search 'in:spam newer_than:30d' --max 50 --json
```

### 阅读特定文件夹/标签中的邮件
```bash
# Etiquetas de sistema
gog gmail search 'in:sent newer_than:7d' --max 20 --json
gog gmail search 'in:drafts' --max 20 --json
gog gmail search 'in:trash newer_than:30d' --max 20 --json
gog gmail search 'is:starred' --max 20 --json

# Etiquetas personalizadas (carpetas del usuario)
gog gmail search 'label:Clientes newer_than:30d' --max 20 --json
gog gmail search 'label:Proyectos' --max 20 --json
gog gmail search 'label:Facturas newer_than:90d' --max 20 --json
```

### 查找邮件
```bash
# Por remitente
gog gmail search 'from:juan@empresa.com newer_than:30d' --max 20 --json

# Por asunto
gog gmail search 'subject:propuesta' --max 10 --json

# Por contenido
gog gmail search 'propuesta presupuesto 2026' --max 10 --json

# Combinado
gog gmail search 'from:ceo@empresa.com is:unread newer_than:7d' --max 10 --json

# Con adjuntos
gog gmail search 'has:attachment in:inbox newer_than:7d' --max 10 --json
```

### 有用的时间过滤条件
| 过滤条件 | 含义 |
|--------|-------------|
| `newer_than:1d` | 最近一天 |
| `newer_than:7d` | 最近一周 |
| `newer_than:30d` | 最近一个月 |
| `older_than:180d` | 超过 6 个月 |
| `after:2026/01/01` | 从指定日期开始 |

## 结果展示

在获取到 JSON 数据后，向用户清晰地展示结果：

```
📥 INBOX — 8 correos nuevos (3 no leídos)

  ⭐ [hoy 09:14] ceo@empresa.com
     "Reunión urgente esta tarde"

  📧 [hoy 08:30] juan@empresa.com
     "Re: Propuesta Q1 2026"

  📰 [ayer 18:00] newsletter@medium.com
     "Top 10 AI tools this week"
  ...

¿Quieres que analice estos correos o que responda alguno?
```

## 多个账户

如果用户拥有多个 Gmail 账户：
```bash
# Listar cuentas configuradas
gog auth list

# Leer de una cuenta específica
gog gmail search 'in:inbox is:unread' --account otra@gmail.com --max 20 --json

# Cambiar cuenta por defecto
export GOG_ACCOUNT=otra@gmail.com
```

## 重要提示：
- 始终使用 `--json` 选项以获取结构化的数据
- 在自动运行或定时任务中使用 `--no-input` 选项以避免交互式提示
- `--max` 选项可用于限制结果数量；如需更多结果可增加该参数
- Gmail 的搜索语法与 gmail.com 的搜索语法相同