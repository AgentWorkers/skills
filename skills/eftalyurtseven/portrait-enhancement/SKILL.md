---
name: portrait-enhancement
description: 使用 each::sense AI 来优化肖像照片。提供专业级别的修图服务，包括皮肤平滑处理、牙齿美白、眼部美化、瑕疵去除、光线调整等。
metadata:
  author: eachlabs
  version: "1.0"
---
# 肖像美化

使用 `each::sense` 的专业级 AI 技术，对肖像照片进行美化处理。该功能为摄影师、内容创作者以及所有希望提升照片质量的人提供全面的肖像美化服务。

## 主要功能

- **皮肤平滑**：保留自然质感的皮肤修复
- **牙齿美白**：提亮笑容的同时保持真实感
- **眼睛美化**：提亮、锐化眼睛，增强清晰度
- **瑕疵去除**：去除痤疮、疤痕等皮肤瑕疵
- **光线调整**：修复刺眼的阴影，添加摄影棚般的光线效果
- **背景模糊（散景）**：打造专业的景深效果
- **头发美化**：增加头发的蓬松度和光泽，修复飞散的头发
- **妆容优化**：提升现有妆容或添加自然效果的妆容
- **抗衰老**：进行微妙的抗衰老修图
- **专业修整**：完成全面的肖像修整流程

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance this portrait with natural skin smoothing and subtle teeth whitening",
    "mode": "max",
    "image_urls": ["https://example.com/portrait.jpg"]
  }'
```

## API 配置

| 设置 | 值 |
|---------|-------|
| 端点 | `POST https://sense.eachlabs.run/chat` |
| 内容类型 | `application/json` |
| 接受类型 | `text/event-stream` |
| 客户端超时 | 最低 10 分钟 |

## 模式选择

在生成结果前，请询问用户：

**“您需要快速且低成本的效果，还是高质量的效果？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终成品、客户使用、适合打印 | 较慢 | 最高质量 |
| `eco` | 快速预览、批量处理、草图 | 较快 | 良好质量 |

## 使用案例示例

### 1. 皮肤平滑与修整

自然地平滑皮肤，同时保留质感和毛孔，减少瑕疵。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply natural skin smoothing to this portrait. Keep the skin texture realistic, reduce visible pores and fine lines, but avoid the plastic look. Maintain skin detail around eyes and lips.",
    "mode": "max",
    "image_urls": ["https://example.com/portrait.jpg"]
  }'
```

### 2. 牙齿美白

自然地提亮牙齿，避免过度美白。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Whiten the teeth in this portrait photo. Make them bright but natural looking - not Hollywood white. Remove any yellow or staining while keeping the natural tooth shape and texture.",
    "mode": "max",
    "image_urls": ["https://example.com/smile-portrait.jpg"]
  }'
```

### 3. 眼睛美化

提亮并锐化眼睛，打造更具吸引力的眼神。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance the eyes in this portrait. Brighten the whites, add subtle catchlights, increase iris clarity and color vibrancy, and reduce any redness or dark circles under the eyes. Keep it natural.",
    "mode": "max",
    "image_urls": ["https://example.com/headshot.jpg"]
  }'
```

### 4. 瑕疵去除

去除痤疮、疤痕等皮肤瑕疵。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove blemishes from this portrait including acne spots, small scars, and any temporary skin imperfections. Keep moles and natural beauty marks. Preserve the natural skin texture in treated areas.",
    "mode": "max",
    "image_urls": ["https://example.com/portrait-blemishes.jpg"]
  }'
```

### 5. 光线调整

修复不良的光线条件，或添加摄影棚级别的光线效果。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Fix the lighting in this portrait. It was taken in harsh midday sun with unflattering shadows. Apply soft studio-style lighting with gentle shadows, reduce harsh highlights on the forehead, and add subtle rim lighting for depth.",
    "mode": "max",
    "image_urls": ["https://example.com/harsh-light-portrait.jpg"]
  }'
```

### 6. 背景模糊（散景）

打造专业的景深效果，突出主体。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a professional bokeh effect to this portrait. Blur the background with a smooth, creamy quality like an 85mm f/1.4 lens. Keep the subject perfectly sharp including hair edges. The blur should gradually increase with distance from the subject.",
    "mode": "max",
    "image_urls": ["https://example.com/portrait-busy-background.jpg"]
  }'
```

### 7. 头发美化

增加头发的蓬松度和光泽，修复飞散的头发。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance the hair in this portrait. Add natural-looking shine and healthy luster, tame flyaway hairs, add subtle volume at the crown, and make the hair color more vibrant. Keep the overall hairstyle unchanged.",
    "mode": "max",
    "image_urls": ["https://example.com/portrait-hair.jpg"]
  }'
```

### 8. 妆容优化

提升现有妆容或添加自然效果的妆容。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance the makeup in this portrait photo. Add subtle contouring to define cheekbones, slightly darken and define the eyebrows, add a soft natural lip color, and apply light mascara effect to the lashes. Keep everything looking natural and not overdone.",
    "mode": "max",
    "image_urls": ["https://example.com/natural-portrait.jpg"]
  }'
```

### 9. 抗衰老

进行微妙的抗衰老修图。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply subtle age reduction to this portrait. Soften fine lines and wrinkles, reduce sagging under the eyes, lift the corners of the mouth slightly, and add a healthy glow to the skin. The result should look natural - like a well-rested version, not like a different person.",
    "mode": "max",
    "image_urls": ["https://example.com/mature-portrait.jpg"]
  }'
```

### 10. 专业肖像修整

结合多种美化效果，完成专业的修整流程。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Give this portrait a complete professional polish suitable for a corporate headshot. Apply natural skin smoothing, subtle teeth whitening, eye enhancement with catchlights, blemish removal, soft studio lighting, gentle background blur, and hair touch-up. The final result should look polished but authentic - suitable for LinkedIn or company website.",
    "mode": "max",
    "image_urls": ["https://example.com/corporate-portrait.jpg"]
  }'
```

## 多轮修图流程

使用 `session_id` 迭代优化肖像效果：

```bash
# Initial enhancement
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Start with basic skin smoothing on this portrait",
    "session_id": "portrait-retouch-001",
    "image_urls": ["https://example.com/portrait.jpg"]
  }'

# Add teeth whitening
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now add subtle teeth whitening to the result",
    "session_id": "portrait-retouch-001"
  }'

# Add eye enhancement
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance the eyes - brighten and add catchlights",
    "session_id": "portrait-retouch-001"
  }'

# Final background blur
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Finally, add a gentle background blur for a professional look",
    "session_id": "portrait-retouch-001"
  }'
```

## 批量处理多张肖像

一致地处理多张肖像：

```bash
# Portrait 1
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Professional headshot retouch: natural skin smoothing, eye brightening, subtle background blur",
    "mode": "eco",
    "image_urls": ["https://example.com/team-member-1.jpg"]
  }'

# Portrait 2
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Professional headshot retouch: natural skin smoothing, eye brightening, subtle background blur",
    "mode": "eco",
    "image_urls": ["https://example.com/team-member-2.jpg"]
  }'

# Portrait 3
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Professional headshot retouch: natural skin smoothing, eye brightening, subtle background blur",
    "mode": "eco",
    "image_urls": ["https://example.com/team-member-3.jpg"]
  }'
```

## 肖像美化提示

请求肖像美化时，请提供以下详细信息：

1. **具体美化内容**：需要美化的部位（皮肤、眼睛等）
2. **强度级别**：轻微、中等或强烈
3. **自然效果**：强调保持结果的真实性
4. **需要保留的部分**：需要保持不变的面部特征
5. **使用场景**：头像、社交媒体、打印等

### 示例提示结构

```
"Apply [enhancement type] to this portrait.
[Specific instructions for the enhancement].
Keep [what to preserve].
The result should look [desired outcome] for [use case]."
```

## 最佳实践

### 保持真实感
- 在请求中始终注明“自然效果”或“真实感”
- 在进行皮肤平滑处理时，要求保留皮肤纹理
- 避免过度美白牙齿或过度提亮眼睛
- 在专业场合中，保持修图效果的自然感

### 保留面部特征
- 不要要求改变面部结构
- 保留自然的面部特征和独特之处
- 保持整张图片的肤色一致
- 保持自然的画面比例

### 技术注意事项
- 提供高分辨率的源图片以获得最佳效果
- 光线条件良好的图片效果更佳
- 正面朝向的肖像更适合大多数美化处理
- 支持 JPG 和 PNG 格式

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不平衡 | 在 eachlabs.ai 补充数据 |
| 内容违规 | 禁止的内容 | 确保提供的肖像适合使用 |
| 超时 | 修图过程复杂 | 将客户端超时设置为至少 10 分钟 |
| 未检测到面部 | 肖像中看不到面部 | 提供面部清晰可见的肖像 |

## 相关技能

- `each-sense` - 核心 API 文档
- `face-swap` - 面部替换功能
- `image-edit` - 通用图像编辑
- `image-generation` - 从头开始生成新肖像