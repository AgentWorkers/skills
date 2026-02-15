---
name: gsuite-sdk
description: 使用 gSuite-sdk 与 Google Workspace API（Gmail、Calendar、Drive、Sheets）进行交互。
metadata:
  openclaw:
    requires:
      env:
        - GOOGLE_CREDENTIALS_FILE
    primaryEnv: GOOGLE_CREDENTIALS_FILE
    install:
      - kind: pip
        package: gsuite-sdk
        bins: [gsuite]
    homepage: https://github.com/PabloAlaniz/google-suite
---

# Google Suite 技能

本技能用于使用 `gsuite-sdk` 与 Google Workspace API（Gmail、Calendar、Drive、 Sheets）进行交互。

## 安装

```bash
pip install gsuite-sdk
```

（可选的额外组件：）
```bash
pip install gsuite-sdk[cloudrun]  # Para Secret Manager
pip install gsuite-sdk[all]       # Todas las dependencias
```

## 认证

### 首次使用（需要浏览器）

用户需要从 Google Cloud Console 获取 `credentials.json` 文件，然后进行认证：

```bash
# Via CLI
gsuite auth login

# O via Python (abre navegador)
from gsuite_core import GoogleAuth
auth = GoogleAuth()
auth.authenticate()
```

请参阅 [GETTING_CREDENTIALS.md](../docs/GETTING_CREDENTIALS.md) 以获取完整指南。

### 之后的会话

认证成功后，令牌会保存在本地并自动更新：

```python
from gsuite_core import GoogleAuth

auth = GoogleAuth()
if auth.is_authenticated():
    # Listo para usar
    pass
else:
    # Necesita autenticarse (abre navegador)
    auth.authenticate()
```

## Gmail

### 阅读邮件

```python
from gsuite_core import GoogleAuth
from gsuite_gmail import Gmail, query

auth = GoogleAuth()
gmail = Gmail(auth)

# Mensajes no leídos
for msg in gmail.get_unread(max_results=10):
    print(f"De: {msg.sender}")
    print(f"Asunto: {msg.subject}")
    print(f"Fecha: {msg.date}")
    print(f"Preview: {msg.body[:200]}...")
    print("---")

# Buscar con query builder
mensajes = gmail.search(
    query.from_("notifications@github.com") & 
    query.newer_than(days=7)
)

# Marcar como leído
msg.mark_as_read()
```

### 发送邮件

```python
gmail.send(
    to=["destinatario@example.com"],
    subject="Asunto del email",
    body="Contenido del mensaje",
)

# Con adjuntos
gmail.send(
    to=["user@example.com"],
    subject="Reporte",
    body="Adjunto el reporte.",
    attachments=["reporte.pdf"],
)
```

## Calendar

### 阅读事件

```python
from gsuite_core import GoogleAuth
from gsuite_calendar import Calendar

auth = GoogleAuth()
calendar = Calendar(auth)

# Eventos de hoy
for event in calendar.get_today():
    print(f"{event.start.strftime('%H:%M')} - {event.summary}")

# Próximos 7 días
for event in calendar.get_upcoming(days=7):
    print(f"{event.start}: {event.summary}")
    if event.location:
        print(f"  📍 {event.location}")

# Rango específico
from datetime import datetime
events = calendar.get_events(
    time_min=datetime(2026, 2, 1),
    time_max=datetime(2026, 2, 28),
)
```

### 创建事件

```python
from datetime import datetime

calendar.create_event(
    summary="Reunión de equipo",
    start=datetime(2026, 2, 15, 10, 0),
    end=datetime(2026, 2, 15, 11, 0),
    location="Sala de conferencias",
)

# Con asistentes
calendar.create_event(
    summary="Sync semanal",
    start=datetime(2026, 2, 15, 14, 0),
    end=datetime(2026, 2, 15, 15, 0),
    attendees=["alice@company.com", "bob@company.com"],
    send_notifications=True,
)
```

## Drive

### 列出和下载文件

```python
from gsuite_core import GoogleAuth
from gsuite_drive import Drive

auth = GoogleAuth()
drive = Drive(auth)

# Listar archivos recientes
for file in drive.list_files(max_results=20):
    print(f"{file.name} ({file.mime_type})")

# Buscar
files = drive.list_files(query="name contains 'reporte'")

# Descargar
file = drive.get("file_id_aqui")
file.download("/tmp/archivo.pdf")
```

### 上传文件

```python
# Subir archivo
uploaded = drive.upload("documento.pdf")
print(f"Link: {uploaded.web_view_link}")

# Subir a carpeta específica
uploaded = drive.upload("data.xlsx", parent_id="folder_id")

# Crear carpeta
folder = drive.create_folder("Reportes 2026")
drive.upload("q1.pdf", parent_id=folder.id)
```

## Sheets

### 读取数据

```python
from gsuite_core import GoogleAuth
from gsuite_sheets import Sheets

auth = GoogleAuth()
sheets = Sheets(auth)

# Abrir spreadsheet
spreadsheet = sheets.open("SPREADSHEET_ID")

# Leer worksheet
ws = spreadsheet.worksheet("Sheet1")
data = ws.get("A1:D10")  # Lista de listas

# Como diccionarios (primera fila = headers)
records = ws.get_all_records()
# [{"Nombre": "Alice", "Edad": 30}, ...]
```

### 编写数据

```python
# Actualizar celda
ws.update("A1", "Nuevo valor")

# Actualizar rango
ws.update("A1:C2", [
    ["Nombre", "Edad", "Ciudad"],
    ["Alice", 30, "NYC"],
])

# Agregar filas al final
ws.append([
    ["Bob", 25, "LA"],
    ["Charlie", 35, "Chicago"],
])
```

## CLI

如果您已安装了 `gsuite-cli`：

```bash
# Autenticación
gsuite auth login
gsuite auth status

# Gmail
gsuite gmail list --unread
gsuite gmail send --to user@example.com --subject "Hola" --body "Mundo"

# Calendar
gsuite calendar today
gsuite calendar list --days 7

# Drive
gsuite drive list
gsuite drive upload archivo.pdf

# Sheets
gsuite sheets read SPREADSHEET_ID --range "A1:C10"
```

## 代理注意事项：

1. **首次认证需要浏览器**：用户必须首次手动完成 OAuth 认证。
2. **令牌持久化**：认证成功后，令牌会保存在 `tokens.db` 文件中，并自动更新。
3. **权限范围**：默认情况下，该技能会请求访问 Gmail、Calendar、Drive 和 Sheets 的权限。您可以使用 `--scopes` 参数来限制权限范围。
4. **常见错误**：
   - `CredentialsNotFoundError`：`credentials.json` 文件缺失。
   - `TokenRefreshError`：令牌过期，无法更新（需要重新认证）。
   - `NotFoundError`：资源不存在或没有相应的权限。