# 特性开关与渐进式发布

## 特性开关的实现

```typescript
// Simple feature flag service
const flags = new Map<string, boolean>()

export const featureFlags = {
  isEnabled(key: string): boolean {
    return flags.get(key) ?? false
  },
  
  enable(key: string) {
    flags.set(key, true)
  },
  
  disable(key: string) {
    flags.set(key, false)
  },
}

// Usage
if (featureFlags.isEnabled('new-checkout')) {
  return <NewCheckout />
}
return <OldCheckout />
```

## A/B 测试

```typescript
// Simple A/B bucket
function getBucket(userId: string, experiment: string): 'a' | 'b' {
  const hash = hash(`${userId}:${experiment}`)
  return hash % 2 === 0 ? 'a' : 'b'
}

// Usage
const bucket = getBucket(userId, 'checkout-button-color')
if (bucket === 'a') {
  return <Button color="blue" />
}
return <Button color="green" />
```

## 禁用机制

```typescript
// Emergency disable
app.get('/feature/:key', (req, res) => {
  if (req.query.disable === 'true') {
    featureFlags.disable(req.params.key)
    return res.json({ status: 'disabled' })
  }
  return res.json({ enabled: featureFlags.isEnabled(req.params.key) })
})
```

## 检查清单：
- [ ] 选择特性开关工具（LaunchDarkly、Unleash 或自定义工具）
- [ ] 实现特性开关的评估机制
- [ ] 添加用户定位功能
- [ ] 设置 A/B 测试方案
- [ ] 创建禁用机制
- [ ] 规划特性开关的发布比例