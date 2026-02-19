---
name: whatsapp-validate
description: 检查电话号码是否存在于本地 Baileys 会话缓存中。
---
# WhatsApp验证技能

该技能用于验证电话号码是否已被连接的WhatsApp账户访问过。

## 使用方法

```
exec({ cmd: "node <skill_dir>/scripts/validate.js COMMAND [ARGS]" })
```

## 命令说明

### 验证单个号码
```
exec({ cmd: "node <skill_dir>/scripts/validate.js check \"5511999999999\"" })
```

### 批量验证
```
exec({ cmd: "node <skill_dir>/scripts/validate.js batch \"5511999999999,5511888888888\"" })
```

### 列出已知号码
```
exec({ cmd: "node <skill_dir>/scripts/validate.js list 50" })
```

## 注意

该技能仅检查本地缓存。如果某个号码未在缓存中，仍有可能存在对应的WhatsApp账户——只是该账户尚未与机器人进行过交互而已。