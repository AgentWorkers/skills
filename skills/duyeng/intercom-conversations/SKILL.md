# Clawhub 技能：对讲机通话记录（读取）

Clawhub 会加载此 Node 模块，并调用 `default(input)` 函数。

## 所需环境变量

- `INTERCOM_ACCESS_TOKEN`（必需）

## 安装

```bash
npm install
```

## 输入参数

### 列出通话记录
```json
{ "action": "conversations.list", "per_page": 50, "starting_after": "cursor" }
```

### 查找特定通话记录
```json
{ "action": "conversations.find", "conversation_id": "123", "display_as": "plaintext" }
```

### 搜索通话记录
```json
{ "action": "conversations.search", "query": { "operator": "AND", "value": [] }, "pagination": { "per_page": 50 } }
```

## 输出结果

所有成功的响应都会包含 `ok: true`，并显示相应的 `action` 内容。

- `list`/`search` 返回：`{ ok, action, conversations, next_starting_after }`
- `find` 返回：`{ ok, action, conversation }`

错误信息：`{ ok: false, error, supported_actions? }`

## 合同规范 / 元数据

- 开源 API 规范：`openapi.yaml`
- 技能注册表元数据：`clawhub.skill.json`