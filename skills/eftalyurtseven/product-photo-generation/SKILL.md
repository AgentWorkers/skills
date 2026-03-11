---
name: Product Photo Generation
description: 使用 each::sense API 为电子商务、市场营销和商品目录生成专业的产品照片。
metadata:
  category: image-generation
  api: each::sense
  modes: [max, eco]
  features: [product-shots, lifestyle-context, studio-lighting, white-background, multi-turn]
---
# 产品照片生成

使用 each::sense API 生成专业的产品照片。您可以创建适合电子商务使用的图片、生活场景照片以及具有工作室品质的产品视觉效果，适用于任何商品。

## 概述

each::sense API 可生成高质量的产品照片，适用于以下场景：

- **电子商务产品照片**：适合在线商店使用的干净、专业的图片
- **生活场景照片**：产品在真实环境中的展示
- **纯白背景照片**：标准的产品目录和市场图片
- **工作室灯光效果**：适合高端产品展示的专业灯光效果
- **营销视觉素材**：吸引眼球的广告和推广图片

您也可以通过 `image_urls` 提供自己的产品图片，将您的实际产品放入专业设计的场景中。

## 快速入门

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a professional product photo of a minimalist ceramic coffee mug on a white background with soft studio lighting",
    "mode": "max"
  }'
```

## 产品照片风格

| 风格 | 描述 | 适用场景 |
|-------|-------------|----------|
| 纯白背景 | 产品置于纯白色背景上 | 电子商务、市场平台、产品目录 |
| 生活场景 | 产品在真实环境中的展示 | 社交媒体、品牌故事讲述 |
| 平铺展示 | 产品与配饰的上下排列 | 时尚、食品、配饰 |
| 实用场景 | 产品被使用或处于其自然环境中的场景 | 营销活动、广告 |
| 重点展示（Hero Shot） | 采用戏剧性的灯光和角度来突出产品 | 主页横幅、特色产品 |
| 细节特写 | 近景拍摄，突出产品的质地和工艺 | 奢侈品、手工制品 |

## 使用案例示例

### 纯白背景产品照片

标准电子商务产品照片，背景为纯白色。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Professional product photo of a stainless steel water bottle on pure white background, centered composition, soft box lighting from above and sides, no shadows, e-commerce style, 4K quality",
    "mode": "max"
  }'
```

### 生活场景照片

产品在真实环境中展示。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Lifestyle product photography of premium wireless headphones on a modern wooden desk, morning light through window, MacBook and coffee cup in soft focus background, warm and inviting atmosphere",
    "mode": "max"
  }'
```

### 平铺展示

产品与配饰的上下排列。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Flat lay product photography of a leather wallet, arranged with sunglasses, car keys, and a fountain pen on marble surface, overhead shot, even lighting, editorial style composition",
    "mode": "max"
  }'
```

### 重点展示（Hero Shot，采用戏剧性灯光）

用于营销材料的高冲击力产品图片。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Hero shot of a luxury perfume bottle, dramatic side lighting creating elegant shadows, dark moody background with subtle gradient, glass reflections and caustics, premium advertising quality",
    "mode": "max"
  }'
```

### 细节特写

近景拍摄，突出产品的质地和工艺。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Macro detail shot of handcrafted leather bag stitching, extreme close-up showing texture and quality of leather grain, shallow depth of field, warm directional lighting highlighting craftsmanship",
    "mode": "max"
  }'
```

### 实用场景照片

产品被实际使用或展示的过程。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Action product shot of running shoes in motion, dynamic angle showing flexibility, slight motion blur on background, athletic track setting, energetic and sporty atmosphere",
    "mode": "max"
  }'
```

### 季节性/主题照片

根据特定季节或节日风格设计的产品照片。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Holiday themed product photo of a scented candle surrounded by pine branches, dried oranges, and cinnamon sticks, warm cozy lighting, festive winter atmosphere, gift-ready presentation",
    "mode": "max"
  }'
```

### 尺寸对比照片

产品与参考物一起展示，以显示比例。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Product scale photo of a compact Bluetooth speaker next to a smartphone and coffee cup for size reference, clean white background, even lighting, showing portable dimensions clearly",
    "mode": "max"
  }'
```

### 包装照片

产品与包装一起拍摄，展示开箱体验。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Product and packaging photo of premium skincare bottle emerging from elegant black box, tissue paper visible, unboxing moment, luxury presentation, soft lighting on neutral background",
    "mode": "max"
  }'
```

## 使用自己的产品图片

通过 `image_urls` 提供自己的产品图片，将您的产品放入专业设计的场景中。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Place this product in a modern kitchen setting, morning light, marble countertop, lifestyle photography style",
    "image_urls": ["https://example.com/my-product.jpg"],
    "mode": "max"
  }'
```

### 带自定义背景的产品照片

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Put this product on a pure white background with professional studio lighting, remove existing background, e-commerce ready",
    "image_urls": ["https://example.com/raw-product-photo.jpg"],
    "mode": "max"
  }'
```

## 产品摄影的最佳实践

### 灯光指南

- **软箱灯光**：适合电子商务照片的均匀照明
- **边缘灯光**：使产品与背景区分开
- **自然窗光**：营造温暖、真实的生活氛围
- **戏剧性侧光**：增加深度和高级感
- **散射顶灯**：减少刺眼阴影

### 构图技巧

- 电子商务照片中将重要产品置于中心
- 生活场景照片中遵循三分法则
- 为文字叠加留出空白区域
- 考虑平台的纵横比要求
- 包含能讲述故事的场景元素

### 背景选择

- 纯白色背景（#FFFFFF）：适合市场平台
- 渐变背景：适合高端产品
- 与产品相得益彰的场景环境
- 有质感的背景：适合手工艺品

## 拍摄提示

有效的拍摄提示包括：

**灯光描述**：
- “软箱灯光”、“自然窗光”、“戏剧性侧光”
- “边缘灯光”、“背光”、“散射顶灯”
- “黄金时刻的光线”、“冷色调的 Studio 灯光”

**角度说明**：
- “平视角度”、“45 度角”、“平铺展示”
- “低角度重点展示”、“四分之三视角”、“正面拍摄”

**背景细节**：
- “纯白背景”、“渐变灰色背景”
- “大理石表面”、“木质桌面”、“混凝土纹理”

**风格参考**：
- “电子商务风格”、“编辑级质量”、“杂志广告风格”
- “产品目录照片”、“Instagram 风格”、“高端品牌视觉”

**配饰和场景元素**：
- “极简主义配饰”、“生活元素”、“季节性装饰”
- “互补的配饰”、“自然元素”

## 模式选择

| 模式 | 适用场景 | 输出质量 |
|------|----------|----------------|
| `max` | 重点展示照片、营销材料、高端产品 | 最高质量、详细渲染 |
| `eco` | 快速迭代、批量目录照片、概念测试 | 快速生成、良好质量 |

使用 `max` 模式制作最终的营销素材和重点展示图片。使用 `eco` 模式进行快速原型制作和生成多个变体。

## 产品系列的多轮拍摄

使用 `session_id` 保持产品系列或产品目录的一致性。

### 开始产品系列拍摄

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a product photo of a blue ceramic coffee mug on white background with soft natural lighting, minimalist style",
    "session_id": "product-catalog-2024",
    "mode": "max"
  }'
```

### 继续保持一致的风格

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now generate the matching red ceramic mug in the same style and lighting setup",
    "session_id": "product-catalog-2024",
    "mode": "max"
  }'
```

### 添加变体

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a lifestyle version showing both mugs on a breakfast table with croissants",
    "session_id": "product-catalog-2024",
    "mode": "max"
  }'
```

## 错误处理

| 错误代码 | 原因 | 解决方案 |
|-------|-------|----------|
| 401 未经授权 | API 密钥无效或缺失 | 确保 `X-API-Key` 头部信息设置正确 |
| 400 错误请求 | 请求体格式不正确 | 检查 JSON 语法和必填字段 |
| 429 请求次数过多 | 请求次数过多 | 实施指数级延迟策略 |
| 500 服务器错误 | 服务暂时不可用 | 稍后重试 |

### 实施指数级延迟重试策略

```bash
for i in 1 2 3; do
  response=$(curl -s -w "%{http_code}" -X POST "https://sense.eachlabs.run/chat" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $EACHLABS_API_KEY" \
    -H "Accept: text/event-stream" \
    -d '{
      "message": "Professional product photo of wireless earbuds on white background",
      "mode": "max"
    }')

  http_code="${response: -3}"
  if [ "$http_code" -eq 200 ]; then
    echo "${response%???}"
    break
  fi
  sleep $((2**i))
done
```

## 相关技能

- [图像生成](/skills/image-generation) - 通用图像创建
- [图像编辑](/skills/image-edit) - 修改和优化现有图像
- [时尚 AI](/skills/fashion-ai) - 专注于时尚产品的摄影技术