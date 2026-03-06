---
name: logo-generation
description: 使用 each::sense AI 生成专业的标志（logos）。为品牌、初创企业和公司设计文字标志（wordmarks）、图标标志（icon logos）、组合标志（combination marks）、字母组合标志（monograms）、吉祥物（mascots）、徽章（emblems）以及抽象风格的标志（abstract logos）。
metadata:
  author: eachlabs
  version: "1.0"
---
# 标志生成

使用 `each::sense` 生成专业且富有创意的标志。该功能可创建多种风格的标志，包括文字标志、图标标志、组合标志、字母组合标志、吉祥物标志以及抽象设计，适用于各种规模的品牌。

## 特点

- **文字标志**：基于文本的标志，支持自定义排版  
- **图标/符号标志**：独立的图形标识  
- **组合标志**：图标与文本结合的设计  
- **字母组合标志**：以首字母为基础的标志  
- **吉祥物标志**：以特定字符为特色的品牌标识  
- **抽象标志**：几何形状或概念性的设计  
- **徽章标志**：具有封闭结构的徽章或印章  
- **极简主义标志**：简洁、现代的设计风格  
- **标志变体**：提供彩色、黑白版本及仅包含图标的版本  
- **透明背景**：适用于各种用途的导出格式  

## 快速入门  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a modern minimalist logo for a tech startup called Nexus. Clean lines, professional look.",
    "mode": "max"
  }'
```  

## 标志风格与适用场景  

| 标志风格 | 最适合的对象 | 特点 |  
|---------|------------|---------|  
| 文字标志 | 独特的品牌名称、初创企业 | 以排版为核心，易于阅读  
| 图标/符号标志 | 应用图标、网站图标、社交媒体图标 | 可缩放，易于记忆  
| 组合标志 | 全面品牌识别系统、网站 | 多功能，完整的品牌形象  
| 字母组合标志 | 奢侈品牌、律师事务所 | 优雅、简洁  
| 吉祥物标志 | 体育团队、食品品牌、游戏公司 | 亲切、易于识别  
| 抽象标志 | 科技公司、创新型企业 | 现代感强，独特设计  
| 徽章标志 | 大学、政府机构、传统品牌 | 具有传统感，权威性强  
| 极简主义标志 | 现代品牌、应用程序 | 设计简洁，用途广泛  

## 适用场景示例  

### 1. 基于文本的标志（文字标志）  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a wordmark logo for a coffee brand called BREW HAVEN. Use elegant serif typography with a warm, artisanal feel. Rich brown and cream colors. The text should be the main focus with subtle coffee-inspired styling.",
    "mode": "max"
  }'
```  

### 2. 图标/符号标志  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an icon logo for a fitness app. Design a bold, dynamic symbol that represents strength and movement. Use a single striking icon without any text. Electric blue and white colors. Must work well as an app icon at small sizes.",
    "mode": "max"
  }'
```  

### 3. 组合标志（图标 + 文本）  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a combination logo for an eco-friendly cleaning company called GreenClean. Include a leaf icon integrated with the company name. Fresh green and white color scheme. Modern sans-serif font. The icon should work standalone but also pair well with the text.",
    "mode": "max"
  }'
```  

### 4. 字母组合标志  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a monogram logo for a luxury fashion brand with initials JM (James Morrison). Interlock the letters elegantly. Gold on black background. High-end, sophisticated feel. Classic with a modern twist.",
    "mode": "max"
  }'
```  

### 5. 吉祥物标志  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a mascot logo for a gaming company called Thunder Wolves. Design a fierce but friendly wolf character with lightning bolt elements. Bold colors - purple, electric blue, white. The wolf should have personality and attitude. Suitable for esports branding.",
    "mode": "max"
  }'
```  

### 6. 抽象标志  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an abstract logo for a fintech startup called Quantum Finance. Use geometric shapes that suggest growth, security, and innovation. Gradient from deep blue to teal. No literal imagery - focus on abstract forms that feel professional and cutting-edge.",
    "mode": "max"
  }'
```  

### 7. 徽章标志  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an emblem logo for a craft brewery called Mountain Peak Brewing, established 2015. Design a circular badge with mountain imagery, hops, and the company name. Vintage Americana style. Navy blue, gold, and cream colors. Should look great on bottle labels and merchandise.",
    "mode": "max"
  }'
```  

### 8. 极简主义标志  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an ultra-minimalist logo for a design studio called FORM. Single color, black on white. Reduce the concept to its absolute essence - clean lines, perfect proportions, no unnecessary elements. Should work at any size from favicon to billboard.",
    "mode": "max"
  }'
```  

### 9. 多版本标志（多次迭代设计）  

使用 `session_id` 可创建一致的标志变体：  

```bash
# Create the primary logo
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a modern logo for a sustainable fashion brand called Earthwear. Combine a stylized leaf with elegant typography. Earth tones - forest green and warm brown.",
    "session_id": "earthwear-logo-project",
    "mode": "max"
  }'

# Create black and white version
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a black and white version of this logo. Pure black on white background, maintaining all the visual impact.",
    "session_id": "earthwear-logo-project",
    "mode": "max"
  }'

# Create icon-only version
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an icon-only version - just the leaf symbol without any text. This will be used for app icons and social media profile pictures.",
    "session_id": "earthwear-logo-project",
    "mode": "max"
  }'
```  

### 10. 带透明背景的标志  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a logo for a photography studio called Aperture Arts. Modern camera aperture icon with elegant text. Create it with a transparent background (PNG format) so it can be placed on any color background. Black logo that will work on light backgrounds.",
    "mode": "max"
  }'
```  

## 最佳实践  

### 设计原则  
- **简洁性**：优秀的标志应简洁且易于记忆  
- **可伸缩性**：标志应能在从图标（16像素）到大型广告牌的各种尺寸上正常显示  
- **多功能性**：支持彩色、黑白以及反转显示  
- **永恒性**：避免使用容易过时的设计元素  
- **相关性**：标志应反映品牌的行业特点和价值观  

### 提示建议  

在请求标志设计时，请提供以下信息：  
1. **品牌名称**：准确的拼写和大小写  
2. **行业/类型**：您的业务属于哪个领域？  
3. **设计风格偏好**：现代、经典、趣味性、专业性等  
4. **颜色偏好**：具体颜色或颜色风格  
5. **设计灵感**：希望包含的符号或概念  
6. **使用场景**：标志将主要用于哪些场合？  
7. **应避免的风格或元素**：需要避免使用哪些设计元素  

### 示例提示结构  

```
"Create a [style] logo for [brand name], a [industry/description].
[Visual elements and concept].
Colors: [color preferences].
Style: [modern/classic/playful/etc].
The logo should [key requirements]."
```  

## 设计模式选择  

在生成标志之前，请询问用户：  
“您需要快速且低成本的标志，还是高品质的标志？”  

| 设计模式 | 最适合的对象 | 设计速度 | 设计质量 |  
|---------|------------|-----------|---------|  
| `max` | 最终的标志设计、客户演示 | 较慢 | 最高质量 |  
| `eco` | 快速的概念构思、头脑风暴 | 较快 | 一般质量 |  

## 多轮迭代设计  

使用 `session_id` 进行多次迭代设计：  

```bash
# Initial concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a logo for a tech company called Nova Labs. Modern, innovative feel.",
    "session_id": "nova-labs-branding"
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I like the concept but make it more bold and add a gradient from purple to blue.",
    "session_id": "nova-labs-branding"
  }'

# Request variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 3 more variations with different icon styles but keep the same color scheme.",
    "session_id": "nova-labs-branding"
  }'
```  

## 批量标志生成  

快速生成多个设计方案：  

```bash
# Concept A - Minimalist
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a minimalist logo for Horizon Analytics - clean geometric shapes, single color",
    "mode": "eco"
  }'

# Concept B - Bold
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a bold logo for Horizon Analytics - strong typography, gradient colors",
    "mode": "eco"
  }'

# Concept C - Abstract
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an abstract logo for Horizon Analytics - flowing shapes suggesting data and insight",
    "mode": "eco"
  }'
```  

## 错误处理  

| 错误类型 | 原因 | 解决方案 |  
|---------|---------|---------|  
| `Failed to create prediction: HTTP 422` | 资源不足 | 请在 eachlabs.ai 网站充值  
| 内容政策违规 | 使用了被禁止的内容 | 调整提示内容以符合政策要求  
| 超时 | 设计过程复杂 | 将客户端的超时时间设置为至少 10 分钟  

## 相关技能  
- `each-sense`：核心 API 文档  
- `product-photo-generation`：产品照片生成  
- `meta-ad-creative-generation`：社交媒体广告创意设计