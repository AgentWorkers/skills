---
name: free-resource
description: "从 Pixabay（图片/视频）、Freesound（音频效果）和 Jamendo（音乐/背景音乐）中搜索并获取免版税的媒体资源。当用户需要查找库存照片、插图、矢量图、视频、音效或背景音乐时，可以使用这些服务；用户还可以下载媒体文件，或通过过滤器查询媒体库。"
---
# 免费资源

您可以从 Pixabay、Freesound 和 Jamendo 上搜索并下载免版税的图片、视频、音效和音乐。

## 快速入门

```bash
# 1. Copy config template and fill in your API keys
cp config.example.json config.json

# 2. Edit config.json with your API keys

# 3. Use without passing API keys
bun ./scripts/jamendo.ts search --query "background" --limit 5
bun ./scripts/freesound.ts search --query "piano"
bun ./scripts/pixabay.ts search-images --query "nature"
```

## 配置

API 密钥存储在 `config.json` 文件中。请复制 `config.example.json` 文件，然后填写您的密钥：

```json
{
  "pixabay": {
    "api_key": "YOUR_PIXABAY_API_KEY"
  },
  "freesound": {
    "api_token": "YOUR_FREESOUND_TOKEN"
  },
  "jamendo": {
    "client_id": "YOUR_JAMENDO_CLIENT_ID"
  }
}
```

### 获取 API 密钥

| 平台 | 类型 | 获取 API 密钥的链接 |
|----------|------|-------------|
| Pixabay | 图片/视频 | https://pixabay.com/accounts/register/ |
| Freesound | 音效 | https://freesound.org/apiv2/apply |
| Jamendo | 音乐/背景音乐 | https://devportal.jamendo.com/ |

### API 密钥的优先级

1. **命令行参数**：`--key`、`--token` 或 `--client-id`
2. **环境变量**：`PIXABAY_API_KEY`、`FREESOUND_API_TOKEN`、`JAMENDO_CLIENT_ID`
3. **配置文件**：`config.json`

---

## Pixabay（图片与视频）

### 搜索图片

```bash
bun ./scripts/pixabay.ts search-images --query "yellow flowers" --image-type photo --orientation horizontal --per-page 5
```

参数：
- `--query`：搜索关键词
- `--id`：图片 ID
- `--lang`：语言
- `--image-type`：图片类型（all | photo | illustration | vector）
- `--orientation`：图片方向（all | horizontal | vertical）
- `--category`：图片类别
- `--colors`：颜色（用逗号分隔）
- `--min-width`：最小宽度
- `--min-height`：最小高度
- `--editors-choice`：编辑器推荐
- `--safesearch`：安全搜索（避免使用低质量图片）
- `--order`：排序方式（popular | latest）
- `--page`：当前页面编号
- `--per-page`：每页显示的数量（5-200）
- `--output`：将结果保存到文件

### 搜索视频

```bash
bun ./scripts/pixabay.ts search-videos --query "ocean waves" --video-type film --per-page 5
```

### 下载图片/视频

```bash
bun ./scripts/pixabay.ts download --url "https://pixabay.com/get/..." --output "/path/to/save.jpg"
```

---

## Freesound（音效）

### 搜索音效

```bash
bun ./scripts/freesound.ts search --query "piano note" --page-size 10
```

参数：
- `--query`：搜索关键词
- `--filter`：过滤条件
- `--sort`：排序方式
- `--fields`：显示的字段
- `--page`：当前页面编号
- `--page-size`：每页显示的数量（最多 150 个音效）
- `--group-by-pack`：按音效包分组显示

### 过滤示例

```bash
bun ./scripts/freesound.ts search --query "drum" --filter "duration:[0 TO 2]"
bun ./scripts/freesound.ts search --query "ambient" --filter "type:wav"
bun ./scripts/freesound.ts search --query "explosion" --sort downloads_desc
```

### 查看音效详情

```bash
bun ./scripts/freesound.ts get --id 12345 --fields id,name,previews,duration
```

### 下载音效预览

```bash
bun ./scripts/freesound.ts download --id 12345 --output ./sound.mp3
```

---

## Jamendo（音乐与背景音乐）

### 搜索音乐

```bash
bun ./scripts/jamendo.ts search --query "rock" --limit 10
```

参数：
- `--query`：搜索关键词
- `--tags`：标签
- `--fuzzytags`：模糊搜索关键词
- `--artist-name`：艺术家名称
- `--album-name`：专辑名称
- `--order`：排序方式
- `--limit`：搜索结果数量（最多 200 条）
- `--offset`：搜索偏移量
- `--output`：下载结果格式

### 音乐属性过滤

```bash
# Instrumental background music
bun ./scripts/jamendo.ts search --query "background" --vocalinstrumental instrumental

# Search by tags (AND logic)
bun ./scripts/jamendo.ts search --tags "electronic+chill" --order popularity_total_desc

# Search by speed
bun ./scripts/jamendo.ts search --query "energetic" --speed high+veryhigh
```

### 查看音乐详情

```bash
bun ./scripts/jamendo.ts track --id 12345 --include musicinfo,stats
```

### 下载音乐

```bash
bun ./scripts/jamendo.ts download --id 12345 --output ./music.mp3
```

---

## API 参考

有关完整的参数表、响应字段说明和速率限制信息，请参阅 `./references/api_reference.md`。