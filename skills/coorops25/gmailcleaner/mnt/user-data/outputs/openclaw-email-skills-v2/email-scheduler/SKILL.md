---
name: email-scheduler
version: "2.0.0"
description: 使用 OpenClaw 的 cron 作业和 gog CLI 的 heartbeat 功能，实现定期的 Gmail 管理自动化。可以设置定时检查邮件、清理垃圾邮件、发送优先级警报以及生成每周报告。适用于用户希望自动化处理邮件、设置重复任务或在后台定期运行邮件处理程序的场景。
homepage: https://gogcli.sh
metadata:
  clawdbot:
    emoji: "⏰"
    requires:
      bins: ["gog"]
      env:
        - name: GOG_ACCOUNT
          description: "Tu dirección de Gmail"
        - name: NOTIFY_CHANNEL
          description: "Canal de notificación (telegram/slack/whatsapp/imessage)"
    install:
      - id: brew
        kind: brew
        formula: steipete/tap/gogcli
        bins: ["gog"]
        label: "Install gog CLI (brew)"
---
# 邮件调度器

使用 OpenClaw 的 Cron 系统和 heartbeat 功能，结合 `gog` 作为后端，实现邮件管理的自动化。

## 何时使用此功能

- “每小时检查我的邮件，并在有重要邮件时通知我”
- “每天早上 8 点自动清理垃圾邮件”
- “每天早上发送邮件摘要给我”
- “自动启用邮件代理”
- “我启用了哪些邮件自动化任务？”
- “关闭自动检查功能”

## Cron 作业配置

将以下配置添加到 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "cron": {
    "jobs": [
      {
        "id": "email-morning-check",
        "schedule": "0 8 * * *",
        "description": "Revisión matutina de correos importantes",
        "message": "Busca correos no leídos del inbox de las últimas 12 horas con gog. Analiza su prioridad. Si hay alguno con prioridad 8 o más, notifícame con el remitente y asunto.",
        "enabled": true
      },
      {
        "id": "email-spam-cleanup",
        "schedule": "0 9 * * *",
        "description": "Limpieza diaria de spam a las 9am",
        "message": "Busca correos en spam con más de 7 días usando gog. Muéstrame cuántos hay y pídeme confirmación antes de eliminarlos.",
        "enabled": true
      },
      {
        "id": "email-priority-alert",
        "schedule": "*/30 9-20 * * 1-5",
        "description": "Alerta de correos críticos cada 30min (horario laboral)",
        "message": "Busca correos no leídos en inbox de los últimos 30 minutos con gog. Si alguno tiene asunto urgente o es de remitentes conocidos como mi jefe, notifícame inmediatamente.",
        "enabled": true
      },
      {
        "id": "email-weekly-report",
        "schedule": "0 9 * * MON",
        "description": "Informe semanal los lunes",
        "message": "Genera un resumen de los correos de la última semana: cuántos recibí, cuánto spam, remitentes más frecuentes, correos que aún no he respondido. Usa gog para obtener los datos.",
        "enabled": true
      },
      {
        "id": "email-followup-check",
        "schedule": "0 10 * * 2,4",
        "description": "Revisión de seguimientos martes y jueves",
        "message": "Busca correos que envié hace más de 5 días y no han recibido respuesta usando gog. Muéstrame la lista y pregúntame si quiero enviar seguimientos.",
        "enabled": false
      }
    ]
  }
}
```

### 启用/禁用作业
```bash
openclaw cron enable email-morning-check
openclaw cron disable email-spam-cleanup
openclaw cron list
openclaw cron run email-weekly-report   # ejecutar manualmente
```

## Heartbeat 配置

在 OpenClaw 的 `HEARTBEAT.md` 文件中进行配置：

```markdown
## Email Monitor

Cada 15 minutos, si hay correos nuevos en inbox:
1. Ejecuta: gog gmail search 'in:inbox is:unread newer_than:15m' --max 10 --json --no-input
2. Si hay resultados, analiza brevemente cada uno
3. Si alguno parece urgente (de remitentes conocidos, asunto con palabras
   como "urgente", "importante", "hoy", "ahora", "deadline"), notifícame
   inmediatamente con el resumen
4. No notificar si son solo newsletters o correos de sistema
5. En horario de silencio (22:00-07:00), solo notificar si prioridad = 10
```

## 通过频道发送通知

邮件代理会向在 `NOTIFY_CHANNEL` 中配置的频道发送警报。
OpenClaw 支持的频道：Telegram、Slack、WhatsApp、iMessage、Discord。

**紧急邮件警报格式：**
```
📧 CORREO URGENTE [Prioridad 9/10]
────────────────────────────────
De: ceo@empresa.com
Asunto: "Reunión urgente — responder antes de las 15h"
Recibido: hace 3 minutos

¿Quieres que redacte una respuesta?
```

**晨间邮件摘要格式：**
```
☀️ Buenos días — Resumen de correos
────────────────────────────────
📥 Inbox: 12 nuevos (3 no leídos)
⭐ Importantes: 2 correos
🗑️ Spam eliminado: 34 correos
📋 Sin respuesta: 1 correo (de hace 6 días)

Correos que requieren tu atención:
• ceo@empresa.com — "Decisión contrato"
• cliente@empresa.com — "Aprobación presupuesto"
```

## 静音时间设置

```json
{
  "email_scheduler": {
    "quiet_hours": {
      "enabled": true,
      "start": "22:00",
      "end": "07:00",
      "timezone": "America/Bogota"
    },
    "notify_priority_threshold": 7,
    "weekend_alerts": false
  }
}
```

## 快速启用流程

当用户选择“自动启用邮件代理”时：

1. 确认 `gog auth list` 显示账户处于激活状态
2. 提问用户：
   - 你希望何时接收晨间邮件摘要？
   - 每隔多少分钟检查一次紧急邮件？
   - 通过哪个渠道接收通知？（Telegram/Slack/WhatsApp）
3. 生成个性化的 Cron 配置
4. 确认：“✅ 邮件代理已启用。有重要邮件时，我们会通过 [CANAL] 通知你。”