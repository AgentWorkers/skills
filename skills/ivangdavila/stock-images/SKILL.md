---
name: Stock Images
slug: stock-images
version: 1.0.0
homepage: https://clawic.com/skills/stock-images
description: 提供来自 Unsplash、Pexels、Pixabay 和 Lorem Picsum 的免费库存照片及占位符图片，附带直接链接。
metadata: {"clawdbot":{"emoji":"📸","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请静默阅读 `setup.md` 文件。基本使用无需进行任何设置。

## 使用场景

当用户需要用于 mockup（原型设计）、原型、网站或演示文稿的库存照片或占位图片时，可以使用本工具。在可能的情况下，该工具会直接提供图片链接，而无需使用 API 密钥。

## 架构

无需使用持久化存储；相关参考文件会在需要时被加载。

## 快速参考

| 主题 | 文件 |
|-------|------|
| 设置 | `setup.md` |
| 内存模板 | `memory-template.md` |
| 所有提供者及示例 | `providers.md` |
| Unsplash 图片分类链接 | `unsplash-categories.md` |

## 核心规则

### 1. 尽量使用直接提供图片的网站
对于快速制作 mockup 和原型，建议使用无需 API 密钥的服务：
- **Lorem Picsum**：按尺寸随机生成图片
- **Placehold.co**：提供带文字的彩色占位图片
- **PlaceKeanu**：提供 Keanu Reeves 的占位图片
- **Unsplash Source**：直接链接到 Unsplash 图库的图片

### 2. 根据需求选择合适的图片来源
| 需求 | 最佳图片来源 |
|------|-------------|
| 通用图片占位 | Lorem Picsum, Unsplash Source |
| 特定主题（商业、自然） | Unsplash, Pexels, Pixabay |
| 带尺寸的彩色框 | Placehold.co |
| 头像/人物图片 | UI Faces, This Person Does Not Exist |
| 图标 | Iconify, Feather Icons |

### 3. 了解图片链接的格式
以下是一些常用的图片链接格式：

```
# Lorem Picsum - random photo at size
https://picsum.photos/800/600

# Lorem Picsum - specific image by ID
https://picsum.photos/id/237/800/600

# Lorem Picsum - grayscale
https://picsum.photos/800/600?grayscale

# Placehold.co - gray placeholder with text
https://placehold.co/800x600

# Placehold.co - custom colors
https://placehold.co/800x600/000/fff

# Unsplash Source - specific search
https://source.unsplash.com/800x600/?nature

# PlaceKeanu - with size
https://placekeanu.com/800/600
```

### 4. 使用缓存过的图片以确保一致性
在构建需要在不同会话中保持图像一致性的原型时：
- 在Lorem Picsum 中使用 `id` 参数
- 保存特定的 Unsplash 图片链接
- 仅在需要多样性时使用 `?random=1` 参数

### 5. 遵守许可协议
| 服务 | 许可协议 | 是否需要署名 |
|---------|---------|-------------|
| Unsplash | Unsplash 许可协议 | 不强制要求，但建议署名 |
| Pexels | Pexels 许可协议 | 不强制要求 |
| Pixabay | Pixabay 许可协议 | 不强制要求 |
| Lorem Picsum | 多种许可协议 | 图片来源于 Unsplash |

对于商业项目，请在原始图片页面上核实许可协议。

### 6. 根据需求加载特定类别的图片
当用户需要特定主题的图片（如商务人士、风景、食物等）时，可以加载 `unsplash-categories.md` 文件以获取按类别分类的图片链接。

### 7. 优化性能
- 在支持的情况下使用 WebP 格式：`https://picsum.photos/800/600.webp`
- 使用所需的精确尺寸（避免使用过大的图片）
- 对于视网膜屏幕：Placehold.co 支持 `@2x` 和 `@3x` 格式

## 常见错误
- 在生产环境中直接使用随机生成的图片链接（未进行缓存）→ 图片不一致
- 未经检查就使用热点链接（hotlink）→ 导致服务拒绝请求
- 在最终产品中使用占位图片服务 → 显示不专业
- 请求过大的图片 → 加载速度变慢

## 外部接口

| 接口 | 发送的数据 | 用途 |
|----------|-----------|---------|
| picsum.photos | 图片尺寸 | 随机图片 |
| placehold.co | 尺寸、颜色、文字 | 占位图片 |
| source.unsplash.com | 搜索关键词 | Unsplash 图库图片 |
| placekeanu.com | 尺寸 | Keanu Reeves 的占位图片 |

这些接口无需身份验证，也不会发送任何用户数据。

## 安全性与隐私
- **离开用户设备的数据**：包含图片尺寸和可选的搜索关键词的 HTTP 请求
- **保留在用户设备上的数据**：浏览器中的缓存图片；无需使用 API 密钥

**本工具不执行以下操作：**
- 存储用户凭证
- 跟踪用户使用情况
- 要求用户注册 API

## 相关技能
如果用户需要，可以使用以下命令安装相关工具：
- `clawhub install <slug>`：安装相关工具
- `image`：图像分析和处理
- `image-generation`：AI 图像生成
- `frontend`：前端开发
- `design`：设计原则
- `ui`：用户界面设计模式

## 反馈
- 如果觉得本工具有用，请给它点赞：`clawhub star stock-images`
- 保持更新：`clawhub sync`