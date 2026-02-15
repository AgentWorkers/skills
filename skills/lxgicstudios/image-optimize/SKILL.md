---
name: image-optimizer
description: 获取基于人工智能的图像优化建议。当图像导致网站加载速度变慢时，请使用此功能。
---

# 图像优化工具

你的图片每个大小约为5MB，之前没人注意到这个问题，直到Lighthouse工具提醒了你。这个工具会扫描你的图片，并告诉你具体需要优化哪些地方。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-image-optimize ./public/images/
```

## 工作原理

- 扫描图片目录，寻找优化机会
- 识别过大的图片
- 建议进行格式转换（例如将PNG转换为WebP）
- 提供响应式图片处理的策略

## 使用示例

```bash
# Scan images directory
npx ai-image-optimize ./public/images/

# Scan assets folder
npx ai-image-optimize ./assets/

# Get detailed report
npx ai-image-optimize ./public/ --verbose
```

## 最佳实践

- **使用WebP格式**：WebP格式的图片比PNG或JPEG更小，但质量相同
- **提供响应式图片**：不要将适用于桌面的图片发送给移动设备
- **延迟加载非可视区域的图片**：推迟加载屏幕外的图片
- **进行高效压缩**：通常80%的压缩率就足够了

## 适用场景

- Lighthouse工具提示图片文件过大
- 页面加载速度较慢
- 需要审核图片的使用情况
- 计划进行图片优化工作

## 该工具属于LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发者工具之一。免费版本无需支付费用、无需注册，也不需要API密钥。这些工具都能正常使用。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。运行该工具前需要设置`OPENAI_API_KEY`环境变量。

```bash
npx ai-image-optimize --help
```

## 工作机制

该工具会扫描你的图片文件，收集图片的尺寸、分辨率等元数据，并将这些数据发送给GPT-4o-mini模型，后者会提供优先级的优化建议。

## 许可证

采用MIT许可证，永久免费。你可以随意使用该工具。