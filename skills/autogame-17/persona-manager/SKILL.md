# 人物管理器（Persona Manager）

**管理代理人物（创建、列出、读取、更新）**

## 功能
- 列出所有可用的人物（`memory/personas/`）
- 根据模板创建新的人物（`template.md`）
- 读取现有的人物文件（markdown/json格式）
- 删除人物

## 使用方法

```bash
# List all personas
node skills/persona-manager/index.js list

# Create a new persona
node skills/persona-manager/index.js create my_persona

# Read a persona file
node skills/persona-manager/index.js read my_persona

# Delete a persona
node skills/persona-manager/index.js delete my_persona
```

## 人物格式
`memory/personas/` 目录下的 Markdown 文件会被 `skills/persona-engine` 模块解析并使用。文件的结构应遵循该模板。

## 依赖项
- `node:fs`  
- `node:path`  
- 不需要额外的 npm 包。