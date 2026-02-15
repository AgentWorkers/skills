---
name: ha-integration-patterns
description: Home Assistant的自定义集成模式与架构决策：在为Home Assistant构建集成模块、自定义组件或API桥接器时需要参考这些内容。涵盖了服务响应数据、HTTP视图、存储API以及集成架构的相关知识。
---

# Home Assistant 集成模式

## 服务响应数据模式

### 问题
默认情况下，Home Assistant（HA）中的服务采用“一次使用即忽略”的设计，返回空数组 `[]`。

### 解决方案（HA 2023.7+）
使用 `supports_response` 参数注册服务：

```python
from homeassistant.helpers.service import SupportsResponse

hass.services.async_register(
    domain, 
    "get_full_config", 
    handle_get_full_config,
    schema=GET_CONFIG_SCHEMA,
    supports_response=SupportsResponse.ONLY,  # ← KEY PARAMETER
)
```

调用服务时添加 `?return_response` 标志：
```bash
curl -X POST "$HA_URL/api/services/your_domain/get_full_config?return_response"
```

### 响应处理器
```python
async def handle_get_full_config(hass: HomeAssistant, call: ServiceCall):
    """Handle the service call and return data."""
    # ... your logic ...
    return {"entities": entity_data, "automations": automation_data}
```

---

## HTTP 视图与服务：何时使用哪种方式

| 使用场景 | 使用方式 | 不应使用的方式 |
|----------|-----|-----------|
| 返回复杂数据 | HTTP 视图 | 服务（不支持响应功能） |
| 执行一次性操作 | 服务 | HTTP 视图 |
| 触发自动化任务 | 服务 | HTTP 视图 |
| 查询状态/配置 | HTTP 视图 | 内部存储 API |

### HTTP 视图模式
用于数据检索的 API：
```python
from homeassistant.components.http import HomeAssistantView

class OpenClawConfigView(HomeAssistantView):
    """HTTP view for retrieving config."""
    url = "/api/openclaw/config"
    name = "api:openclaw:config"
    requires_auth = True

    async def get(self, request):
        hass = request.app["hass"]
        config = await get_config_data(hass)
        return json_response(config)

# Register in async_setup:
hass.http.register_view(OpenClawConfigView())
```

---

## 重要提示：避免使用内部 API
**切勿使用以“_”开头的 API**——这些 API 是私有的，并且会随版本更新而发生变化。**

❌ **错误示例：**
```python
storage_collection = hass.data["_storage_collection"]
```

✅ **正确示例：**
```python
# Use public APIs only
from homeassistant.helpers.storage import Store
store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
```

---

## 数据存储模式

### 存储少量数据（设置、缓存）
```python
from homeassistant.helpers.storage import Store

STORAGE_KEY = "your_domain.storage"
STORAGE_VERSION = 1

store = Store(hass, STORAGE_VERSION, STORAGE_KEY)

# Save
data = {"entities": modified_entities}
await store.async_save(data)

# Load
data = await store.async_load()
```

### 存储大量数据（历史记录、日志）
建议使用外部数据库或文件存储，而非 Home Assistant 的内置存储工具。

---

## 需关注的重大变更

| 变更内容 | 版本 | 迁移方式 |
|--------|---------|-----------|
| 会话代理功能 | 2025.x+ | 直接使用 `async_process` 方法 |
| 服务响应数据 | 2023.7+ | 添加 `supports_response` 参数 |
| 配置项迁移 | 2022.x+ | 使用 `async_migrate_entry` 方法 |

**请务必查看：** https://www.home-assistant.io/blog/ 以获取您所使用版本的相关信息。

---

## HACS 集成结构

```
custom_components/your_domain/
├── __init__.py          # async_setup_entry
├── config_flow.py       # UI configuration
├── manifest.json        # Dependencies, version
├── services.yaml        # Service definitions
└── storage_services.py  # Your storage logic
```

### 最简化的 `manifest.json` 文件示例
```json
{
  "domain": "your_domain",
  "name": "Your Integration",
  "codeowners": ["@yourusername"],
  "config_flow": true,
  "dependencies": [],
  "requirements": [],
  "version": "1.0.0"
}
```

---

## 测试检查清单
- [ ] 服务调用返回预期的数据（通过 `?return_response` 参数）
- [ ] 可使用认证令牌访问 HTTP 视图
- [ ] 未使用以“_”开头的 API
- [ ] 数据存储在重启后仍能保留
- [ ] 配置流程能够正确创建配置项
- [ ] 错误处理能够返回有意义的提示信息

---

## 文档资源
- 集成基础：`developers.home-assistant.io/docs/creating_integration_index`
- 服务调用：`developers.home-assistant.io/docs/dev_101_services`
- HTTP 视图：`developers.home-assistant.io/docs/api/webserver`
- 重大变更信息：`home-assistant.io/blog/`（按版本筛选）
- HACS 集成指南：`hacs.xyz/docs/publish/start`

---

## 经验教训
从尝试使用 HA-OpenClaw Bridge 的过程中我们了解到：
> “80% 的问题其实可以通过提前阅读 30-60 分钟的文档就能发现。我们当时直接开始编码，而没有先了解 Home Assistant 的实际工作原理。”

在开始开发之前，请务必使用 `skills/pre-coding-research/` 这一方法论来进行充分的准备工作。