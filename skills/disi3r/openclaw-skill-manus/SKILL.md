---
name: manus
description: Manus的自主AI代理，具备研究、开发、自动化以及媒体生成的能力。
homepage: https://manus.im
metadata: {"clawdbot":{"emoji":"🧠","requires":{"env":["MANUS_API_KEY"]},"primaryEnv":"MANUS_API_KEY"}}
---

# Manus AI 技能

这是一个具备互联网访问功能的自主 AI 代理，能够执行复杂任务、进行调研、开发软件、自动化工作流程以及生成多媒体内容。

## 配置

### API 密钥

API 密钥配置在环境变量 `MANUS_API_KEY` 中：

```bash
export MANUS_API_KEY="sk-..."
# O en ~/.clawdbot/clawdbot.json:
# "skills.manus.apiKey": "sk-..."
```

### 端点 (Endpoints)

| 端点 | 描述 |
|----------|-------------|
| `https://api.manus.ai/v1/tasks` | 创建和管理任务 |
| `https://api.manus.ai/v1/projects` | 项目管理 |
| `https://api.manus.ai/v1/files` | 上传文件 |
| `https://api.manus.ai/v1/webhooks` | 用于接收通知的 Webhook |

## 基本使用

### 创建简单任务

```bash
cd /home/disier/clawd/skills/manus/scripts
python3 run_task.py "Investiga las últimas noticias de IA"
```

### 集成连接器 (Integrated Connectors)

```bash
# Gmail
python3 run_task.py "Revisa mis correos de hoy en Gmail y resumenlos"

# Notion
python3 run_task.py "Crea una página en Notion con el resumen de esta reunión"

# Google Calendar
python3 run_task.py "Agenda una reunión para mañana a las 3pm"

# Slack
python3 run_task.py "Envía un resumen al canal de #updates en Slack"
```

## 可用脚本 (Available Scripts)

| 脚本 | 描述 |
|--------|-------------|
| `run_task.py` | 执行基本任务 |
| `create_project.py` | 创建项目 |
| `upload_file.py` | 上传文件 |
| `check_status.py` | 查询任务状态 |
| `get_result.py` | 获取任务结果 |
| `webhook_server.py` | Webhook 服务器 |

## 详细脚本 (Detailed Scripts)

### run_task.py - 执行基本任务

```bash
python3 run_task.py "TU_PROMPT_AQUI" [--timeout SEGUNDOS]
```

**示例:**

```bash
# Investigación
python3 run_task.py "Investiga las regulaciones de IA en la UE 2026"

# Desarrollo
python3 run_task.py "Crea una web app de todo list con React"

# Escritura
python3 run_task.py "Escribe un artículo sobre automatización de workflows"

# Automatización
python3 run_task.py "Reserva un vuelo de NYC a LA para el 15 de marzo"
```

### create_project.py - 创建项目

```bash
python3 create_project.py "Nombre del proyecto" "Descripción"
```

### upload_file.py - 上传文件

```bash
python3 upload_file.py /ruta/al/archivo.txt
```

**用途:**
- 用于上传数据文件或参考文档

### check_status.py - 查询任务状态

```bash
python3 check_status.py TASK_ID
```

**可能的状态:**
- `pending` - 待处理中
- `running` - 正在运行
- `completed` - 已完成
- `failed` - 失败

### get_result.py - 获取任务结果

```bash
python3 get_result.py TASK_ID
```

该脚本用于获取任务的完整结果。

## 连接器 (Connectors)

Manus 支持以下集成连接器:

### Gmail

```python
python3 run_task.py "Lee mis últimos 5 correos de Gmail y extrae los puntos importantes"
```

### Notion

```python
python3 run_task.py "Crea una base de datos en Notion para tracking de proyectos"
```

### Google 日历 (Google Calendar)

```python
python3 run_task.py "Lee mi agenda de hoy y muéstrame mis reuniones"
```

### Slack

```python
python3 run_task.py "Publica un mensaje en el canal #anuncios"
```

## 数据集成 (Data Integrations)

### Similarweb

```python
python3 run_task.py "Analiza el tráfico de disier.tech usando Similarweb"
```

## Webhook

### 接收通知

```bash
python3 webhook_server.py 8080
```

该服务器会在指定端口监听，并在任务完成后发送通知。

## 兼容 OpenAI

Manus 支持 OpenAI 的 SDK：

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-...",  # Tu API key de Manus
    base_url="https://api.manus.ai/v1"
)

response = client.chat.completions.create(
    model="manus-1.6-adaptive",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## 通过 Clawdbot 使用

### 在代理中使用 (Using with Clawdbot)

```markdown
Cuando necesites investigación profunda o desarrollo:
1. Usa el script run_task.py de la skill manus
2. Especifica el prompt claro
3. Espera el resultado
4. Integra la respuesta
```

### 完整示例

```bash
# Investigar y crear contenido
python3 run_task.py "Investiga 5 tendencias de tecnología para 2026 y escribe un artículo de 1000 palabras"

# Con archivo de contexto
python3 upload_file.py contexto.md
python3 run_task.py "Basándote en el archivo subido, crea una presentación"
```

## 最佳实践 (Best Practices)

### 有效的提示 (Effective Prompts)

**✅ 推荐的提示示例:**
- “研究欧盟的 AI 相关法规并总结关键点”
- “使用 React 和 OpenWeatherMap 创建一个天气 Web 应用”
- “分析某个账户最近的 10 条推文并生成报告”

**❌ 应避免的提示示例:**
- “做点有意义的事情”（过于模糊）
- “改进这个功能”（缺乏具体上下文）

### 文件处理

如需提供更多背景信息，请先上传相关文件：

```bash
python3 upload_file.py datos.csv
python3 run_task.py "Analiza este CSV y genera un reporte de ventas"
```

### 长期任务

对于耗时较长的任务，请注意:

```bash
python3 run_task.py "Investiga a profundidad el mercado de IA" --timeout 300
```

## 成本

任务执行会消耗信用点数。具体使用情况请参考相关说明:

```bash
curl "https://api.manus.ai/v1/usage" \
  -H "API_KEY: sk-..."
```

## 注意事项

- 任务在隔离的沙箱环境中运行
- 该代理具备完整的互联网访问权限
- 可以安装所需软件
- 能够维持经过身份验证的服务会话
- 任务执行时间因复杂度而异