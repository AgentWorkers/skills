---
name: threads
description: 与 Threads API 的交互：用于发布帖子（文本、图片）、读取帖子以及获取用户资料信息。当用户需要通过 Graph API 来操作 Threads 时，请使用这些接口。
---

# Threads 技能

该技能允许您在 Threads 中发布内容、查看自己的帖子动态，并通过 Threads Graph API 获取用户信息。

## 准备工作

使用此技能需要一个 **Threads 访问令牌**，该令牌可在 [Facebook 开发者平台](https://developers.facebook.com/) -> 工具 -> Graph API Explorer 获取。

请将令牌设置到环境变量中：
```bash
export THREADS_ACCESS_TOKEN='ваш_токен'
```

## 使用方法

### 1. 获取用户资料信息
```bash
python3 scripts/threads_cli.py me
```

### 2. 发布文本帖子
```bash
python3 scripts/threads_cli.py post "Привет из OpenClaw!"
```

### 3. 发布图片轮播（最多可包含 10 张图片）
```bash
python3 scripts/threads_cli.py post "Наша новая подборка проектов" --image "https://example.com/1.jpg" --image "https://example.com/2.jpg"
```
*每条帖子最多可上传 10 张图片*

### 4. 通过本地文件发布内容
```bash
python3 scripts/threads_cli.py post "Картинка с моего компьютера" --image "/путь/к/файлу.jpg"
```
*脚本会自动将文件上传到临时服务器进行发布*

### 5. 查看您的所有帖子
```bash
python3 scripts/threads_cli.py list
```

## 相关脚本
- `scripts/threads_cli.py`：用于操作 Graph API 的主要命令行工具。

## 注意事项：
- 发布图片时，图片的 URL 必须是公开可访问的。
- 该技能基于 `graph.threads.net/v1.0` API 进行开发。