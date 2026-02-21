---
name: pinterest
description: 搜索和浏览 Pinterest 上的图片（“pins”），获取图片的详细信息，并通过 Telegram 或其他消息传递方式将图片直接发送给用户。适用于用户需要寻找灵感、搜索图片/想法或浏览 Pinterest 内容的场景。该功能会直接发送图片，而不仅仅是图片链接。
---

# Pinterest Skill

在 Pinterest 上搜索、浏览和分享图片——发送的是实际图片，而不仅仅是链接。

## 快速搜索并发送图片

### 第一步：在 Pinterest 上搜索
```
browser action=navigate url="https://www.pinterest.com/search/pins/?q=YOUR+SEARCH+TERMS"
browser action=snapshot
```

### 第二步：获取高分辨率图片的 URL
从截图中找到图片的 URL。Pinterest 的图片 URL 具有以下格式：
- 缩略图：`https://i.pinimg.com/236x/...`
- 中等分辨率图片：`https://i.pinimg.com/564x/...`
- **高分辨率图片：`https://i.pinimg.com/originals/...`

要获取高分辨率图片，请在 URL 中将 `236x` 或 `564x` 替换为 `originals`。

### 第三步：将图片发送给用户
**发送实际图片（而不是链接！）：**
```
message action=send media="https://i.pinimg.com/originals/xx/xx/image.jpg" message="Pin description here"
```

**发送多张图片：**
```
message action=send media="https://i.pinimg.com/originals/..." message="Option 1: Modern minimal"
message action=send media="https://i.pinimg.com/originals/..." message="Option 2: Cozy rustic"
```

## 图片的详细操作流程

1. **导航** 到 Pinterest 的搜索页面
2. **截图** 以查看搜索结果
3. **点击** 任意一张图片以查看详细信息（会显示更大的图片）
4. **截图** 图片的详细页面，或提取图片的原始 URL
5. **使用 `media=` 参数通过消息工具发送图片**

### 获取原始图片
在图片的详细页面上：
- 查找包含 `src="i.pinimg.com"` 的 `<img>` 标签
- 将图片转换为高分辨率版本：`https://i.pinimg.com/originals/{hash}.jpg`

## 示例：搜索“极简风格的桌面布置”
```
# 1. Search
browser action=navigate url="https://www.pinterest.com/search/pins/?q=minimalist+desk+setup"
browser action=snapshot

# 2. Extract image URLs from snapshot (look for i.pinimg.com)
# 3. Convert to high-res originals

# 4. Send images
message action=send media="https://i.pinimg.com/originals/ab/cd/ef123.jpg" message="Clean white desk with plant 🌿"
message action=send media="https://i.pinimg.com/originals/gh/ij/kl456.jpg" message="Wooden desk, natural light ☀️"
```

## 替代方法：截图
如果提取图片 URL 有困难，可以直接截图图片：
```
browser action=navigate url="https://www.pinterest.com/pin/123456/"
browser action=screenshot
# Then send the screenshot file
message action=send filePath="/path/to/screenshot.jpg" message="Here's the pin!"
```

## API 方法（用于用户自己的内容）

需要设置 OAuth 令牌——请参阅 `references/oauth-setup.md`

```bash
export PINTEREST_ACCESS_TOKEN="your_token"
python3 scripts/pinterest_api.py boards
python3 scripts/pinterest_api.py board-pins <board_id>
python3 scripts/pinterest_api.py pin <pin_id>
```

## 关键要点

- ✅ **始终使用 `media=` 参数直接发送图片**
- ✅ 使用高分辨率图片的原始 URL
- ❌ **不要只发送链接——要发送实际图片**
- 💡 如果图片 URL 无法使用，直接截图图片并发送截图

## 参考资料

- OAuth 设置：`references/oauth-setup.md`
- API 接口：`references/api-reference.md`