# Feishu 群组管理器

用于管理 Feishu 群组聊天（包括设置、名称和元数据）。

## 工具

### 切换繁忙状态
通过在群组名称前添加前缀（例如 `[⏳]`）来标记该群组正在处理耗时较长的任务。

```bash
node skills/feishu-group-manager/toggle_busy.js --chat-id <chat_id> --mode <busy|idle>
```

### 更新设置
可以更新群组名称、描述（公告区域）和权限设置。

```bash
node skills/feishu-group-manager/update_settings.js --chat-id <chat_id> [options]
```

**选项：**
- `-n, --name <文本>`：设置新的群组名称
- `-d, --description <文本>`：设置新的群组描述
- `--edit-permission <所有成员|仅限所有者>`：指定谁可以编辑群组信息
- `--at-all-permission <所有成员|仅限所有者>`：指定谁可以使用 @All 功能
- `--invite-permission <所有成员|仅限所有者>`：指定谁可以邀请其他人加入群组

## 使用说明
请参阅 `MEMORY.md` 文件中的“繁忙状态协议”部分。
- 触发条件：在一对一控制组中，当任务运行时间超过 30 秒时，系统会自动触发该功能。