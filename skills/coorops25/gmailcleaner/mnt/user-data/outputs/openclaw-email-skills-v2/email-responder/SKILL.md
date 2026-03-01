---
name: email-responder
version: "2.0.0"
description: 使用 gog CLI 和 AI 功能来起草和发送 Gmail 回复。能够生成包含完整对话上下文的智能回复，管理回复模板，并跟踪未回复的消息。适用于用户需要回复、草拟、撰写、发送或跟进电子邮件时的场景。
homepage: https://gogcli.sh
metadata:
  clawdbot:
    emoji: "✍️"
    requires:
      bins: ["gog"]
      env:
        - name: GOG_ACCOUNT
          description: "Tu dirección de Gmail"
        - name: ANTHROPIC_API_KEY
          description: "API Key de Anthropic para generar respuestas"
    install:
      - id: brew
        kind: brew
        formula: steipete/tap/gogcli
        bins: ["gog"]
        label: "Install gog CLI (brew)"
---
# 邮件回复工具

使用 `gog` 和人工智能（AI）来编辑和发送邮件回复。

## 何时使用此功能

- “回复胡安关于提案的邮件”
- “为重要邮件生成回复”
- “发送你生成的草稿”
- “给 maria@empresa.com 发送关于周五会议的邮件”
- “哪些已发送的邮件没有收到回复？”
- “为5天前客户发送的邮件生成跟进邮件”
- “回复所有人，感谢他们的来信”

## 回复流程

### 第1步 — 确定要回复的邮件
根据发件人、主题或日期查找邮件：
```bash
gog gmail search 'from:juan@empresa.com subject:propuesta' --max 5 --json --no-input
```

### 第2步 — 获取完整的邮件对话记录
```bash
# Buscar todos los mensajes del mismo hilo
gog gmail search 'subject:"Re: Propuesta Q1 2026"' --max 20 --json --no-input
```
回复内容需要与整个邮件对话记录保持一致，而不仅仅是最后一条消息。

### 第3步 — 使用AI生成草稿
利用邮件对话记录作为生成回复的上下文：
```
Eres un asistente de email profesional.
Redacta una respuesta para el correo indicado.
- Tono: profesional y cercano
- Longitud: máximo 150 palabras salvo que sea necesario más
- No incluyas asunto ni encabezados, solo el cuerpo
- Firma con el nombre del usuario

Historial del hilo (del más antiguo al más reciente):
[HILO_COMPLETO]

Correo al que debes responder (el último):
De: juan@empresa.com
Asunto: Propuesta Q1 2026
Mensaje: [CUERPO]

Genera la respuesta:
```

### 第4步 — 显示草稿并获取确认
```
✍️  Borrador generado:
────────────────────────────────────────
Para: juan@empresa.com
Asunto: Re: Propuesta Q1 2026

Hola Juan,

Gracias por compartir la propuesta. He revisado los puntos
principales y me parece una dirección muy interesante.

¿Podríamos agendar una llamada esta semana para discutir
el presupuesto en detalle?

Quedo atento.
[Nombre]
────────────────────────────────────────

¿Qué hago?
  [1] Enviar ahora
  [2] Editar primero
  [3] Guardar como borrador en Gmail
  [4] Descartar
```

### 第5a步 — 发送邮件
⚠️ **发送前务必请求确认。绝无例外。**
```bash
gog gmail send \
  --to "juan@empresa.com" \
  --subject "Re: Propuesta Q1 2026" \
  --body "Hola Juan,\n\nGracias por compartir..." \
  --no-input
```

### 第5b步 — 发送新邮件（非回复邮件）
```bash
gog gmail send \
  --to "maria@empresa.com" \
  --subject "Reunión del viernes" \
  --body "Hola María,\n\nTe escribo para confirmar..." \
  --no-input
```

### 使用抄送（CC）或密送（BCC）：
```bash
gog gmail send \
  --to "maria@empresa.com" \
  --cc "equipo@empresa.com" \
  --subject "Reunión del viernes" \
  --body "..." \
  --no-input
```

## 检测未回复的邮件（跟进）
查找在X天内未收到回复的已发送邮件：
```bash
# Correos enviados hace más de 5 días
gog gmail search 'in:sent older_than:5d newer_than:30d' --max 50 --json --no-input
```

将这些邮件与已收到的回复进行对比，找出未回复的邮件，并提供生成跟进邮件的选项：
```
📬 Correos sin respuesta (más de 5 días):

1. Para: cliente@empresa.com
   Asunto: "Cotización proyecto web"
   Enviado: hace 7 días
   ¿Genero un follow-up?

2. Para: proveedor@tech.com
   Asunto: "Solicitud de demo"
   Enviado: hace 12 días
   ¿Genero un follow-up?
```

## 快速回复模板

针对常见情况的预定义模板：

**确认收到邮件**：
```
Hola [NOMBRE], gracias por tu mensaje. Lo revisaré y te responderé
a la brevedad. Saludos, [FIRMA]
```

**确认会议安排**：
```
Hola [NOMBRE], confirmo mi asistencia a la reunión del [FECHA]
a las [HORA]. Hasta entonces. Saludos, [FIRMA]
```

**请求更多信息**：
```
Hola [NOMBRE], gracias por contactarme. Para poder ayudarte mejor,
¿podrías compartirme más detalles sobre [TEMA]? Quedo atento. [FIRMA]
```

**表示不在办公**：
```
Gracias por tu mensaje. Estoy fuera de la oficina hasta el [FECHA].
Responderé a mi regreso. Para urgencias: [CONTACTO]. [FIRMA]
```

用户可以输入：“使用确认收到邮件的模板来回复这3封重要邮件”，然后代理会根据具体情况进行个性化处理并发送每封邮件。

## 重要规则
`send_requiresconfirmation: true` — **始终启用此设置。**
绝不要在用户查看和批准之前发送邮件。