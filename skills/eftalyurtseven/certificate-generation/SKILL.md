---
name: certificate-generation
description: 使用 each::sense AI 生成专业证书、文凭和奖项。可以创建课程结业证书、成就奖、专业认证证书、学术文凭以及自定义品牌的证书。
metadata:
  author: eachlabs
  version: "1.0"
---
# 证书生成

使用 `each-sense` 工具可以生成专业的证书、文凭和奖励证书。该功能能够为教育机构、企业培训、职业发展及表彰项目生成高质量的证书图片。

## 主要特性

- **课程结业证书**：适用于在线课程、研讨会和训练营
- **成就证书**：用于表彰里程碑、目标达成或竞赛成绩
- **奖励证书**：用于表彰优秀表现或卓越贡献
- **专业资格证书**：包含行业认可的认证信息
- **学术文凭**：用于证明学位或学术成就
- **培训证书**：记录企业培训内容及员工技能提升情况
- **感谢证书**：表达感谢或认可志愿者的贡献
- **参与证书**：用于记录活动、会议或项目的参与情况
- **员工表彰证书**：用于表彰月度优秀员工或长期服务的员工
- **定制品牌证书**：可添加公司Logo和品牌元素

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional course completion certificate for a web development bootcamp. Include placeholder text for recipient name, course name, completion date, and instructor signature.",
    "mode": "max"
  }'
```

## 证书设计要素

| 元素        | 描述                          | 位置              |
|-------------|---------------------------------|-------------------|
| 边界/框架      | 装饰性边框                         | 证书外边缘            |
| 标题        | 组织名称、Logo占位符                     | 顶部中央            |
| 标题        | 证书类型（如“结业证书”等）                   | 上部中央            |
| 接收者姓名    | 大字体、显眼的位置                     | 中心位置            |
| 说明        | 成就详情、课程名称                     | 姓名下方            |
| 日期        | 完成/颁发日期                        | 下部区域            |
| 签名        | 发证机构的签名及职位                   | 最底部区域            |
| 徽章/奖章      | 官方印章、徽标或奖章                     | 角落或底部中央          |
| 证书ID      | 证书的唯一标识符                     | 最底部角落            |

## 使用场景示例

### 1. 课程结业证书

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an elegant course completion certificate for an online learning platform. Modern design with navy blue and gold accents. Include sections for: recipient name, course title, completion date, instructor signature, and platform logo placeholder. Add a decorative border and official seal.",
    "mode": "max"
  }'
```

### 2. 成就证书

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design an achievement certificate for a sales team. Celebratory design with star motifs and ribbon accents. Include fields for: employee name, achievement description (e.g., exceeded quarterly target by 150%), date, and manager signature. Corporate professional style with red and silver color scheme.",
    "mode": "max"
  }'
```

### 3. 奖励证书

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an award certificate for a science fair competition. First place winner design with trophy imagery and laurel wreath elements. Include: winner name, project title, competition name, date, and judges signatures. Premium golden design with white background.",
    "mode": "max"
  }'
```

### 4. 专业资格证书

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a professional certification certificate for a project management credential. Formal corporate style with clean lines. Include: certified professional name, certification title (Certified Project Manager), issue date, expiration date, certification ID number, and certifying authority signature. Use dark blue and white color scheme with embossed seal look.",
    "mode": "max"
  }'
```

### 5. 学术文凭

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a traditional academic diploma for a university. Classic formal design with ornate border and calligraphic elements. Include: graduate name, degree title (Bachelor of Science in Computer Science), university name, graduation date, university seal placeholder, and signatures for dean and president. Ivory background with dark green and gold accents.",
    "mode": "max"
  }'
```

### 6. 培训证书

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a corporate training certificate for workplace safety compliance. Professional and official design. Include: employee name, training program name, training hours completed, completion date, trainer signature, and HR manager signature. Add company logo placeholder and compliance badge. Blue and gray corporate colors.",
    "mode": "max"
  }'
```

### 7. 感谢证书

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a certificate of appreciation for volunteer work. Warm and heartfelt design with soft colors. Include: volunteer name, organization name, description of service, hours contributed, date, and director signature. Add decorative elements like hands or hearts. Use teal and coral color palette.",
    "mode": "max"
  }'
```

### 8. 参与证书

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a participation certificate for a hackathon event. Modern tech-inspired design with geometric patterns. Include: participant name, event name, event dates, category/track participated in, and organizer signature. Use vibrant purple and electric blue colors with clean sans-serif typography.",
    "mode": "max"
  }'
```

### 9. 月度优秀员工证书

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an Employee of the Month certificate. Prestigious and motivating design with star and spotlight elements. Include: employee name, month and year, department, reason for recognition, CEO signature, and company logo placeholder. Premium gold and black design with elegant typography.",
    "mode": "max"
  }'
```

### 10. 定制品牌证书

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a certificate template for a tech company named TechForward. Minimalist modern design that matches tech startup aesthetics. Include: recipient name, certificate title (flexible), achievement description, date, and dual signature lines. Use clean white background with gradient accent in purple to blue. Include prominent logo placeholder area and QR code placeholder for verification.",
    "mode": "max"
  }'
```

## 设计模式选择

在生成证书前，请询问用户：

**“您需要快速且低成本的证书，还是高质量的吗？”**

| 设计模式 | 适用场景          | 生成速度 | 证书质量         |
|---------|------------------|------------|-------------------|
| `max`     | 最终版证书、官方文件                  | 较慢         | 最高质量           |
| `eco`     | 快速草图、模板预览                  | 较快         | 一般质量           |

## 多轮证书设计

可以使用 `session_id` 进行多次证书设计迭代：

```bash
# Initial design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a certificate of completion for a coding bootcamp",
    "session_id": "cert-bootcamp-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the design more modern with darker colors and add a tech-inspired geometric border",
    "session_id": "cert-bootcamp-001"
  }'

# Add specific elements
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a QR code placeholder in the bottom right corner and include space for a holographic seal",
    "session_id": "cert-bootcamp-001"
  }'
```

## 证书系列生成

可以为不同级别的证书生成统一风格的系列证书：

```bash
# Bronze level certificate
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Bronze level achievement certificate for a learning platform. Use bronze/copper metallic accents. Include level badge prominently.",
    "session_id": "cert-levels-001"
  }'

# Silver level certificate (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the Silver level version of this certificate. Same layout but with silver metallic accents.",
    "session_id": "cert-levels-001"
  }'

# Gold level certificate
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the Gold level version. Same layout but with gold metallic accents and more ornate details.",
    "session_id": "cert-levels-001"
  }'
```

## 设计最佳实践

### 设计指南
- **字体选择**：使用优雅、易读的字体；人名使用手写体字体，正文使用简洁的无衬线字体
- **层次结构**：确保接收者姓名是最显眼的元素
- **布局平衡**：正式证书采用对称布局效果最佳
- **空白空间**：为各个设计元素留出足够的间距
- **颜色搭配**：最多使用2-3种颜色；金色、深蓝色或酒红色能体现尊贵感

### 内容建议
- **明确标题**：醒目地标注证书类型
- **具体成就**：详细说明所取得的成就
- **权威性体现**：添加签名和官方印章
- **验证信息**：包含证书ID或二维码占位符
- **日期标注**：务必注明颁发日期（如适用）

### 技术注意事项
- **分辨率要求**：为打印输出请求高分辨率
- **比例规范**：标准证书比例为横向4:3或信纸大小
- **文本占位符**：使用清晰的占位符（如“[接收者姓名]”）
- **Logo位置**：确保为组织Logo预留指定位置

## 证书生成提示建议

在生成证书时，请包含以下信息：
- **证书类型**：结业证书、成就证书、奖励证书等
- **用途/场合**：明确证书的颁发目的或认证内容
- **设计风格**：正式、现代、传统或趣味性风格
- **色彩方案**：指定具体颜色或使用通用色彩搭配
- **必备元素**：接收者姓名、日期、签名、印章、Logo
- **组织背景**：所属行业及证书的正式程度
- **特殊功能**：是否需要二维码、安全验证元素或徽章

### 示例提示结构

```
"Create a [certificate type] certificate for [organization/purpose].
Style: [formal/modern/traditional].
Color scheme: [colors].
Include: [list of required elements].
Special features: [QR code, seal, badge, etc.]."
```

## 错误处理

| 错误类型 | 原因                | 解决方案                |
|---------|-------------------|----------------------|
| `Failed to create prediction: HTTP 422` | 平衡性不足             | 在 eachlabs.ai 补充数据           |
| 内容违规    | 包含违禁内容             | 调整提示内容以符合政策要求       |
| 超时        | 生成过程复杂             | 将客户端超时时间设置为至少10分钟       |

## 相关技能

- `each-sense`：核心API文档
- `product-photo-generation`：产品及品牌图像生成工具
- `logo-generation`：证书Logo制作工具