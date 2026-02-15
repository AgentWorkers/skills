---
name: Cubox Integration
description: 使用 Open API 将网页和备忘录保存到 Cubox 上
---

# Cubox 集成技能

该技能允许您使用 Open API 将内容保存到 Cubox 中。Cubox 是一个“稍后阅读”和书签服务，支持保存网页链接以及快速创建便签。

## 先决条件

1. **Cubox 高级会员资格**——Open API 是高级会员专属功能。
2. **API 密钥**——请从 Cubox 设置中获取您的 API URL：
   - 进入 Cubox 设置 > 扩展中心与自动化 > API 扩展
   - 启用“API 链接”功能以获取您的个人 API URL。

> ⚠️ **安全提示**：您的 API URL 是一个唯一的凭证，请妥善保管，切勿分享。

## 环境配置

使用您的个人 API URL 设置 `CUBOX_API_URL` 环境变量：

```bash
export CUBOX_API_URL="https://cubox.pro/c/api/save/YOUR_TOKEN"
```

## 可用工具

### 1. 保存网页链接（`scripts/save_url.py`）

将网页链接保存到 Cubox 中。

```bash
python scripts/save_url.py <url> [--title "Title"] [--description "Description"] [--tags "tag1,tag2"] [--folder "Folder Name"]
```

**参数：**
- `url`（必填）：要保存的网页链接
- `--title`（可选）：书签的标题
- `--description`（可选）：描述
- `--tags`（可选）：用逗号分隔的标签列表
- `--folder`（可选）：目标文件夹名称（默认为“收件箱”）

**示例：**
```bash
python scripts/save_url.py "https://example.com/article" --title "Great Article" --tags "tech,reading" --folder "Articles"
```

### 2. 保存便签（`scripts/save_memo.py`）

将快速创建的便签或笔记保存到 Cubox 中。

```bash
python scripts/save_memo.py <content> [--title "Title"] [--description "Description"] [--tags "tag1,tag2"] [--folder "Folder Name"]
```

**参数：**
- `content`（必填）：便签文本内容
- `--title`（可选）：标题（如果未提供，Cubox 会自动生成）
- `--description`（可选）：描述
- `--tags`（可选）：用逗号分隔的标签列表
- `--folder`（可选）：目标文件夹名称（默认为“收件箱”）

**示例：**
```bash
python scripts/save_memo.py "Remember to review the quarterly report" --title "Todo" --tags "work,reminder"
```

## API 使用限制

- 高级用户：每天最多 500 次 API 调用。

## 注意事项

- 保存内容后，Cubox 云端会自动处理相关操作（如文章解析、快照存档等），这可能需要一些时间。
- 如果未指定标题或描述，Cubox 会尝试自动生成这些信息。
- 如果未指定文件夹，内容将默认保存到您的“收件箱”中。