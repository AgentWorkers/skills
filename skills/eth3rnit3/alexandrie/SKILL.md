# Alexandrie Skill

用于与 Alexandrie 笔记应用程序进行交互（地址：https://notes.eth3rnit3.org）

## 配置信息

- **API 地址**：`https://api-notes.eth3rnit3.org/api`
- **前端页面**：`https://notes.eth3rnit3.org`
- **用户名**：`eth3rnit3`
- **用户 ID**：`671423603690045441`
- **密码**：存储在 `/home/eth3rnit3/clawd/.env` 文件中，键名为 `ALEXANDRIE_PASSWORD`

## 使用方法

所有操作均通过 `alexandrie.sh` 脚本完成：

```bash
/home/eth3rnit3/clawd/skills/alexandrie/alexandrie.sh <command> [args]
```

## 命令说明

### 认证
```bash
./alexandrie.sh login                    # Login and get token
./alexandrie.sh logout                   # Logout
```

### 笔记（节点）
```bash
./alexandrie.sh list                     # List all notes/categories
./alexandrie.sh get <nodeId>             # Get a specific note with content
./alexandrie.sh search <query>           # Search notes
./alexandrie.sh create <name> [content] [parentId]  # Create a note
./alexandrie.sh update <nodeId> <name> [content]    # Update a note
./alexandrie.sh delete <nodeId>          # Delete a note
```

## 节点角色
- **角色：1**：表示分类/工作区（容器）
- **角色：3**：表示包含内容的笔记

## 当前结构
- `671425872858841091` - **Perso**（分类）
- `671426069886271492` - **Test**（笔记）

## 示例操作

### 列出所有笔记
```bash
./alexandrie.sh login
./alexandrie.sh list
```

### 阅读笔记
```bash
./alexandrie.sh get 671426069886271492
# Returns: "Salut, ceci est un **test**"
```

### 创建笔记
```bash
./alexandrie.sh create "My Note" "# Title\n\nContent here" 671425872858841091
```

### 搜索笔记
```bash
./alexandrie.sh search "test"
```

## API 参考

基础 URL：`https://api-notes.eth3rnit3.org/api`

### API 端点
- `POST /auth` - 登录（请求体：`{"username": "...", "password": "..."}`）
- `POST /auth/logout` - 注销
- `GET /nodes/user/:userId` - 列出用户的笔记
- `GET /nodes/:nodeId` - 根据 ID 获取笔记（包含内容）
- `GET /nodes/search?q=query` - 搜索笔记
- `POST /nodes` - 创建笔记
- `PUT /nodes/:nodeId` - 更新笔记
- `DELETE /nodes/:nodeId` - 删除笔记

### 认证机制

登录后，JWT 令牌会存储在 cookie 中（文件路径：`/tmp/alexandrie_cookies.txt`）。