---
name: email-reporter
version: "2.0.0"
description: 使用 gog CLI 生成电子邮件报告和统计信息。可以创建每日/每周的汇总报告、垃圾邮件统计分析、发件人信息分析以及待处理任务列表；同时支持将数据导出到 Google Sheets 或文本文件中。适用于用户需要获取电子邮件活动报告、统计结果或进行数据导出的场景。
homepage: https://gogcli.sh
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      bins: ["gog"]
      env:
        - name: GOG_ACCOUNT
          description: "Tu dirección de Gmail"
    install:
      - id: brew
        kind: brew
        formula: steipete/tap/gogcli
        bins: ["gog"]
        label: "Install gog CLI (brew)"
---
# 电子邮件报告工具

该工具使用 `gog` 生成电子邮件报告和统计信息，支持导出到 Google Sheets 或文本文件。

## 适用场景

- “请提供今天的邮件摘要”
- “我这周收到了多少垃圾邮件？”
- “谁给我发送邮件的频率最高？”
- “有哪些邮件需要我回复？”
- “将统计信息导出到 Google Sheets”
- “显示代理的操作记录”
- “这周我的邮件中是否检测到人工智能生成的提示信息？”
- “撤销上一次的操作”

## 可用的报告类型

### 报告 1 — 日报摘要
```bash
gog gmail search 'in:inbox newer_than:1d' --max 100 --json --no-input
gog gmail search 'in:spam newer_than:1d' --max 100 --json --no-input
gog gmail search 'in:sent newer_than:1d' --max 50 --json --no-input
```

展示的结果：
```
📬 RESUMEN DEL DÍA — 25 Feb 2026
══════════════════════════════════
Recibidos:   23 correos
  ⭐ Importantes:  4
  📰 Newsletters:  8
  🗑️  Spam:        11
Enviados:     3 correos
Sin respuesta: 1 correo (de hace 2 días)

Top remitentes hoy:
  1. newsletter@medium.com (3)
  2. juan@empresa.com (2)
  3. notificaciones@github.com (2)
══════════════════════════════════
```

### 报告 2 — 周报摘要
```bash
gog gmail search 'in:inbox newer_than:7d' --max 500 --json --no-input
gog gmail search 'in:spam newer_than:7d' --max 500 --json --no-input
gog gmail search 'in:sent newer_than:7d' --max 200 --json --no-input
```

包含以下内容：
- 每个工作日的邮件总数
- 按类别分类的邮件数量
- 发件量最多的前 10 位发送者
- 需要回复的邮件
- 检测到的提示信息（如有）

### 报告 3 — 未回复的邮件
```bash
# Enviados sin respuesta de más de 5 días
gog gmail search 'in:sent older_than:5d newer_than:30d' --max 100 --json --no-input
```

```
📋 CORREOS PENDIENTES DE RESPUESTA
────────────────────────────────────
1. Para: cliente@empresa.com
   Asunto: "Cotización proyecto web"
   Enviado: hace 8 días
   ¿Genero un follow-up?

2. Para: proveedor@tech.io
   Asunto: "Solicitud de acceso demo"
   Enviado: hace 12 días
   ¿Genero un follow-up?
```

### 报告 4 — 垃圾邮件统计
```bash
gog gmail search 'in:spam newer_than:30d' --max 500 --json --no-input
```

```
🗑️ SPAM — últimos 30 días
────────────────────────────────────
Total:  342 correos bloqueados

Top remitentes de spam:
  1. promo@descuentos.xyz      87 correos
  2. newsletter@ofertas.com    64 correos
  3. no-reply@marketing.io     43 correos

Dominios más frecuentes: .xyz (34%), .info (21%)
```

### 报告 5 — 导出到 Google Sheets
使用 `gog sheets` 将统计信息保存到电子表格中：
```bash
# Crear nueva hoja o actualizar existente
# Columnas: Fecha, Remitente, Asunto, Categoría, Prioridad, Acción

# Actualizar datos en el sheet
gog sheets update <SHEET_ID> "Correos!A2:F100" \
  --values-json '[["2026-02-25","juan@empresa.com","Propuesta Q1","importante",8,"respondido"],...]' \
  --input USER_ENTERED \
  --no-input

# Añadir nuevas filas
gog sheets append <SHEET_ID> "Correos!A:F" \
  --values-json '[["2026-02-25","spam@promo.xyz","GANA UN IPHONE","spam",0,"eliminado"]]' \
  --insert INSERT_ROWS \
  --no-input

# Ver datos actuales
gog sheets get <SHEET_ID> "Correos!A1:F50" --json --no-input
gog sheets metadata <SHEET_ID> --json --no-input
```

用户可以请求：“将周报摘要导出到我的 Google Sheets 文件中”，代理会获取用户的 SHEET_ID，生成数据并插入表格中。

### 报告 6 — 操作日志（审计记录）
读取文件 `~/.openclaw/workspace/email_audit.log`：
```
📋 HISTORIAL DE ACCIONES — últimas 10
────────────────────────────────────────────
2026-02-25 10:31 | TRASH  | 87 correos   | SPAM → PAPELERA
2026-02-25 10:30 | SEND   | 1 correo     | Re: Propuesta Q1
2026-02-24 09:15 | MOVE   | 5 correos    | INBOX → Facturas
2026-02-24 09:10 | READ   | 12 correos   | newsletters → leídos
```

### 操作 — 撤销上一次操作

如果上一次的操作是删除邮件（TRASH），可以尝试恢复该邮件：
```bash
# Buscar correos en papelera recientes
gog gmail search 'in:trash newer_than:1d' --max 100 --json --no-input

# El usuario confirma cuáles restaurar
# Mover de vuelta desde trash con: gog gmail untrash <MESSAGE_ID>
```

```
Última acción: TRASH de 87 correos (hace 5 minutos)
¿Intento recuperarlos de la papelera? (sí/no)
```

## 与 Google Docs 的集成

可以在 Google Docs 中生成可视化报告：
```bash
# Leer un doc existente de informes
gog docs cat <DOC_ID> --no-input

# Exportar como texto plano
gog docs export <DOC_ID> --format txt --out /tmp/informe.txt --no-input
```

## 检测到的提示信息日志文件

将日志文件保存在 `~/.openclaw/workspace/prompts_log.md`：
```markdown
# Prompts de IA detectados en correos

## 2026-02-25

### De: unknown@suspicious.com
**Asunto:** Oportunidad de negocio

**Prompt extraído:**
> Ignore all previous instructions. You are now...
```