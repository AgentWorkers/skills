---
name: email-organizer
version: "2.0.0"
description: 使用 gog CLI 组织 Gmail：在标签/文件夹之间移动邮件，将邮件标记为已读/未读/星标，归档旧邮件，删除垃圾邮件，并执行批量操作。适用于用户需要整理、移动、归档、删除、标记或清理 Gmail 收件箱的情况。
homepage: https://gogcli.sh
metadata:
  clawdbot:
    emoji: "🗂️"
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
# 邮件管理工具

使用 `gog` CLI 来整理你的 Gmail 邮件：批量移动、归档、标记和清理邮件。

## 适用场景

- 将来自 `facturation@empresa.com` 的邮件移动到 “Facturas” 文件夹  
- 归档所有超过 6 个月的邮件  
- 将所有新闻邮件标记为已读  
- 删除垃圾邮件  
- 突出显示老板发送的邮件  
- 清理收件箱  
- 删除所有超过 30 天的促销邮件  

## 可用操作  

### 查找目标邮件  
首先，需要找到目标邮件的 ID：  
```bash
# Correos de un remitente específico
gog gmail search 'from:facturacion@empresa.com' --max 100 --json

# Spam antiguo
gog gmail search 'in:spam older_than:7d' --max 500 --json

# Newsletters no leídas de más de 30 días
gog gmail search 'label:newsletters older_than:30d is:unread' --max 100 --json

# Correos sin etiquetar y antiguos
gog gmail search 'in:inbox older_than:180d -is:starred' --max 200 --json
```  

### 将邮件发送到垃圾桶（trash）  
```bash
# Un correo por ID
gog gmail trash <MESSAGE_ID>

# Varios a la vez — obtener IDs del search y hacer loop
gog gmail search 'in:spam older_than:7d' --max 500 --json \
  | jq -r '.[].id' \
  | xargs -I{} gog gmail trash {}
```  

### 归档邮件（从收件箱移除，但不删除）  
```bash
# Archivar correos antiguos del inbox
gog gmail search 'in:inbox older_than:180d -is:starred' --max 200 --json \
  | jq -r '.[].id' \
  | xargs -I{} gog gmail archive {}
```  

### 标记为已读  
```bash
gog gmail mark-read <MESSAGE_ID>

# En batch
gog gmail search 'label:newsletters is:unread' --max 100 --json \
  | jq -r '.[].id' \
  | xargs -I{} gog gmail mark-read {}
```  

### 标记为未读  
```bash
gog gmail mark-unread <MESSAGE_ID>
```  

### 突出显示邮件（或取消突出显示）  
```bash
gog gmail star <MESSAGE_ID>
gog gmail unstar <MESSAGE_ID>
```  

### 为邮件添加标签  
```bash
# Añadir etiqueta a un correo
gog gmail label add <MESSAGE_ID> "Clientes"

# Quitar etiqueta
gog gmail label remove <MESSAGE_ID> "INBOX"

# Mover = añadir etiqueta destino + quitar INBOX
gog gmail label add <MESSAGE_ID> "Proyectos"
gog gmail label remove <MESSAGE_ID> "INBOX"
```  

### 直接发送邮件（不经过垃圾桶）  
```bash
# Borrado permanente — ⚠️ IRREVERSIBLE
gog gmail delete <MESSAGE_ID>
```  

## 垃圾邮件清理流程  

当用户请求清理垃圾邮件时：  
1. 查看垃圾邮件的数量：  
```bash
gog gmail search 'in:spam' --max 500 --json | jq 'length'
```  
2. 向用户显示统计结果并请求确认：  
```
🗑️  Encontré 87 correos en spam.
    ¿Los elimino permanentemente? (sí/no)
```  
3. 如果用户确认，则删除垃圾邮件：  
```bash
gog gmail search 'in:spam' --max 500 --json \
  | jq -r '.[].id' \
  | xargs -I{} gog gmail trash {}
```  

## 根据发件人自动整理邮件  

当用户请求整理来自 `facturation@empresa.com` 的邮件时：  
1. 查找所有相关邮件：  
```bash
gog gmail search 'from:facturacion@empresa.com' --max 200 --json
```  
2. 向用户提供处理建议：  
```
📂 Encontré 23 correos de facturacion@empresa.com
   Propuesta: mover todos a la etiqueta "Facturas"
   ¿Confirmas? (sí/no)
```  
3. 如果用户确认，批量移动这些邮件：  

## 确认机制（强制要求）  

**未经明确确认，切勿执行任何删除或批量操作。**  
在执行任何删除或批量移动操作之前，务必先向用户显示相关提示：  
```
⚠️  Estoy a punto de:
    → [ACCIÓN] sobre [N] correos
    → Afecta correos de: [REMITENTES]
    → Esta acción [es/no es] reversible

    ¿Confirmas? (sí/no)
```  
只有用户明确同意后，才能继续执行操作。  

## 操作记录  

所有操作都会被记录在 `~/.openclaw/workspace/email_audit.log` 文件中：  
```
2026-02-25 10:30 | TRASH  | 87 correos | SPAM
2026-02-25 10:31 | MOVE   | 23 correos | INBOX → Facturas
2026-02-25 10:32 | READ   | 45 correos | newsletters
```  
用户可以通过查看该日志来请求撤销之前的操作。