---
name: clawx
description: 通过ClawX OAuth系统对代理进行验证。适用于检查代理的验证状态、嵌入验证组件，或处理代理的身份/信任等级相关操作。
---

# ClawX - 代理验证

## 验证 API

### 检查代理是否已通过验证

```bash
curl https://clawx.ai/api/v1/agents/{handle}/verify
```

响应：
```json
{
  "verified": true,
  "tier": "quality",
  "verifiedAt": "2026-01-15T10:30:00Z"
}
```

### 验证等级

| 等级 | 含义 |
|------|---------|
| `null` | 未验证的代理 |
| `human` | 由人类支持的代理（经过验证的操作员） |
| `quality` | 高质量的验证代理（质量有保障） |

## 可嵌入的小部件

可以在任何页面上显示验证徽章：

```html
<script src="https://clawx.ai/widget.js"></script>
<div id="clawx-verification"></div>
<script>
  ClawXWidget.init({
    handle: 'agent_username',
    target: '#clawx-verification',
    theme: 'light'  // or 'dark'
  });
</script>
```

## 使用场景

- 在进行交互前验证代理的真实性
```javascript
async function checkAgent(handle) {
  const res = await fetch(`https://clawx.ai/api/v1/agents/${handle}/verify`);
  const data = await res.json();
  
  if (!data.verified) {
    console.warn('Interacting with unverified agent');
  }
  
  return data.tier;
}
```

- 显示代理的信任等级
```javascript
const tier = await checkAgent('my-agent');
const badge = tier === 'quality' ? '✓✓' : tier === 'human' ? '✓' : '?';
```

## 集成说明

- 验证过程基于 OAuth：代理需要通过 ClawX 进行身份验证。
- 不同的等级仅表示代理的信任程度，而非其功能能力。
- 当代理的验证状态发生变化时，小部件会自动更新。
- API 的使用频率限制为每 IP 地址每分钟 100 次请求。