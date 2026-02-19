---
name: whatsapp-utils
description: 电话号码格式化、缓存检查、联系人导出以及消息ID生成
---
# WhatsApp 工具集（WhatsApp Utilities）

一系列用于 WhatsApp 自动化的实用工具。

## 使用方法

```
exec({ cmd: "node <skill_dir>/scripts/utils.js COMMAND [ARGS]" })
```

## 命令

### 格式化电话号码
```
exec({ cmd: "node <skill_dir>/scripts/utils.js format \"(11) 99999-9999\"" })
```

### 清理电话号码
```
exec({ cmd: "node <skill_dir>/scripts/utils.js clean \"+55 (11) 99999-9999\"" })
```

### 查看缓存信息
```
exec({ cmd: "node <skill_dir>/scripts/utils.js cache-info" })
```

### 导出联系人
```
exec({ cmd: "node <skill_dir>/scripts/utils.js export-contacts" })
```

### 生成消息 ID
```
exec({ cmd: "node <skill_dir>/scripts/utils.js gen-id" })
```