---
name: dialogflow-cx-nlu
description: 通过 REST API 在 Google Dialogflow CX 中管理意图（intents）和实体类型（entity types）。该 API 用于创建、更新和管理自然语言理解组件（natural language understanding components），支持 v3beta1 版本。
---
# Dialogflow CX 自然语言理解（NLU）

通过 REST API 在 Google Dialogflow CX 中管理意图（Intents）和实体类型（Entity Types），以实现自然语言理解功能。

## 先决条件

- 已启用 Dialogflow CX API 的 Google Cloud 项目
- 具有 Dialogflow API 访问权限的服务账户或 OAuth 凭据
- 已通过 `gcloud` CLI 进行身份验证，或持有有效的 bearer token

## 身份验证

### 方法 1：使用 `gcloud` CLI（推荐）
```bash
gcloud auth application-default login
TOKEN=$(gcloud auth print-access-token)
```

### 方法 2：使用服务账户
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
TOKEN=$(gcloud auth application-default print-access-token)
```

## API 基本地址
```bash
https://dialogflow.googleapis.com/v3beta1
```

区域端点示例：
- `https://{region}-dialogflow.googleapis.com`（例如：`us-central1`、`europe-west1`）

## 常用操作

### 列出意图（List Intents）
```bash
curl -X GET \
  "https://dialogflow.googleapis.com/v3beta1/projects/${PROJECT_ID}/locations/${LOCATION}/agents/${AGENT_ID}/intents" \
  -H "Authorization: Bearer ${TOKEN}"
```

### 创建意图（Create Intent）
```bash
curl -X POST \
  "https://dialogflow.googleapis.com/v3beta1/projects/${PROJECT_ID}/locations/${LOCATION}/agents/${AGENT_ID}/intents" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "Book Flight",
    "trainingPhrases": [
      {
        "parts": [{"text": "I want to book a flight"}],
        "repeatCount": 1
      }
    ]
  }
```

### 列出实体类型（List Entity Types）
```bash
curl -X GET \
  "https://dialogflow.googleapis.com/v3beta1/projects/${PROJECT_ID}/locations/${LOCATION}/agents/${AGENT_ID}/entityTypes" \
  -H "Authorization: Bearer ${TOKEN}"
```

### 创建实体类型（Create Entity Type）
```bash
curl -X POST \
  "https://dialogflow.googleapis.com/v3beta1/projects/${PROJECT_ID}/locations/${LOCATION}/agents/${AGENT_ID}/entityTypes" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "Cities",
    "kind": "KIND_LIST",
    "entities": [
      {"value": "New York"},
      {"value": "Los Angeles"
    ]
  }
```

## 关键资源

| 资源          | 描述                                      |
|----------------|-------------------------------------------|
| **Intents**       | 对用户输入进行分类并提取参数                        |
| **Entity Types**    | 定义结构化数据提取规则                            |

## 快速参考

- 详细 API 参考：[references/intents.md](references/intents.md)  
- 实体类型参考：[references/entities.md](references/entities.md)

## 脚本

- `scripts/nlu.py`：用于处理意图和实体类型操作的 CLI 脚本

### 使用方法

```bash
python scripts/nlu.py list-intents --agent AGENT_NAME
python scripts/nlu.py create-intent --agent AGENT_NAME --intent "Book Flight" --phrases "book a flight, I want to fly"
python scripts/nlu.py list-entities --agent AGENT_NAME
python scripts/nlu.py create-entity --agent AGENT_NAME --name "Cities" --values "New York, Los Angeles"
```

## 提示

- 使用能够覆盖用户表达意图多种方式的训练短语（training phrases）。
- 实体类型可以是系统提供的（内置的），也可以是自定义的。
- 对于具有同义词的实体，使用 `KIND_MAP`；对于简单的列表，使用 `KIND_LIST`。