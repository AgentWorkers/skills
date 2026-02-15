---
description: 生成有效的 Podcast RSS 2.0 源，支持 iTunes、Spotify 等平台的扩展格式。
---

# 播客发布工具

本工具用于生成可用于提交到播客目录的RSS源文件。

**适用场景**：创建播客RSS源、添加新剧集或设置新播客时使用。

## 使用要求

- 无需外部工具或API密钥
- 生成的结果为静态XML文件，可部署在任何服务器上。

## 使用步骤

1. **收集元数据**（必填字段）：

   **播客（频道）**：
   | 字段 | 是否必填 | 示例 |
   |-------|----------|---------|
   | 标题 | ✅ | “我的科技播客” |
   | 描述 | ✅ | “每周深入探讨……” |
   | 作者 | ✅ | “约翰·多伊” |
   | 图片链接 | ✅ | 图片尺寸需为3000×3000像素（JPEG/PNG格式） |
   | 网站 | ✅ | “https://example.com” |
   | 语言 | ⬚ | “en-us”（默认） |
   | 类别 | ⬚ | “科技” |
   | 是否公开发布 | ⬚ | false（默认） |

   **每集元数据**：
   | 字段 | 是否必填 | 示例 |
   |-------|----------|---------|
   | 标题 | ✅ | “第1集：入门指南” |
   | 描述 | ✅ | “在本集中……” |
   | 音频链接 | ✅ | .mp3/.m4a音频文件的直接链接 |
   | 时长 | ✅ | “01:23:45”（小时:分钟:秒） |
   | 发布日期 | ✅ | 必须符合RFC 2822格式 |
   | GUID | ⬚ | 若未提供则自动生成 |

2. **生成RSS XML文件**：
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:content="http://purl.org/rss/1.0/modules/content/">
     <channel>
       <title>TITLE</title>
       <description>DESCRIPTION</description>
       <language>en-us</language>
       <itunes:author>AUTHOR</itunes:author>
       <itunes:image href="ARTWORK_URL"/>
       <itunes:category text="CATEGORY"/>
       <itunes:explicit>false</itunes:explicit>
       <link>WEBSITE_URL</link>

       <item>
         <title>EPISODE_TITLE</title>
         <description>EPISODE_DESCRIPTION</description>
         <enclosure url="AUDIO_URL" length="FILE_SIZE" type="audio/mpeg"/>
         <itunes:duration>HH:MM:SS</itunes:duration>
         <pubDate>Thu, 15 Jan 2025 10:00:00 +0000</pubDate>
         <guid isPermaLink="false">UNIQUE_ID</guid>
       </item>
     </channel>
   </rss>
   ```

3. **保存前进行验证**：
   - 确保日期格式符合RFC 2822标准（例如：`Thu, 15 Jan 2025 10:00:00 +0000`）
   - 音频链接必须是直接指向音频文件的链接（而非流媒体页面或YouTube链接）
   - 时长格式应为`HH:MM:SS`或`MM:SS`
   - 每集的GUID必须唯一
   - 图片尺寸至少为3000×3000像素（JPEG或PNG格式）
   - XML文件格式正确（文本中不能包含未转义的`&`、`<`、`>`字符）

4. **将生成的文件保存为`feed.xml`。

5. **添加新剧集**：读取现有的`feed.xml`文件，在剧集列表顶部插入新的`<item>`元素，然后保存文件。

## 部署选项

- **GitHub Pages**：免费，将`feed.xml`文件提交到仓库
- **S3 / Cloudflare R2**：上传XML文件和音频文件
- **任何支持静态文件的服务器**：只需以`application/rss+xml`内容类型提供该文件即可

## 播客目录提交链接

- Apple Podcasts：[podcastsconnect.apple.com](https://podcastsconnect.apple.com)
- Spotify：[podcasters.spotify.com]
- Google Podcasts：会自动从RSS源进行索引

## 注意事项

- **文本中的特殊字符**：在标题或描述中，将`&`转换为`&amp;`，将`<`转换为`<`。
- **文件大小未知**：将`length`属性设置为`0`——大多数播放器可以处理这种情况。
- **多类别**：可以使用嵌套的`<itunes:category>`元素来表示多个类别。
- **预告片/特别剧集**：使用`<itunes:episodeType>trailer</itunes:episodeType>`进行标记。
- **季播剧集**：需要添加`<itunes:season>1</itunes:season>`和`<itunes:episode>1</itunes:episode>`元素。

## 验证工具

- [Podbase Validator](https://podba.se/validate/)
- [Cast Feed Validator](https://castfeedvalidator.com/)