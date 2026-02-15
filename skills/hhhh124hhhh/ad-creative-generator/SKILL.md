---
name: ad-creative-generator
description: 生成多样化的、引人入胜的广告创意，适用于任何产品或品牌，涵盖20多种创意风格和10个类别。这些创意可用于用户需要广告概念、营销提示或创意营销内容生成的场景。
---

# 广告创意生成器

## 概述
这是一个功能全面的广告创意生成工具，能够为任何产品或品牌创建多样且引人入胜的广告创意。它支持生成20多种不同风格的广告概念，并将这些概念分为10个类别。

## 说明
该工具帮助营销人员、设计师和内容创作者生成创新的广告创意和提示。它具备以下特点：
- 提供10个类别中的20多种独特创意风格
- 提供交互式的命令行界面（CLI）以便轻松选择
- 支持多种导出格式（JSON、文本、Markdown）
- 可根据产品/品牌信息自定义创意提示
- 具备完善的错误处理机制，确保生成的内容可用于实际发布

## 安装
除了Node.js（版本14及以上）之外，无需额外依赖。

## 使用方法

### 基本使用方法
```bash
node generate.js
```

### 交互式模式
运行脚本并按照提示操作：
1. 输入您的产品/品牌名称
2. 选择创意类别（支持多选）
3. 在所选类别中挑选具体风格
4. 选择导出格式
5. 查看或导出生成的创意提示

### 命令行选项
```bash
# Generate prompts for a specific product
node generate.js --product "Luxury Perfume"

# Export directly to JSON
node generate.js --product "Smart Watch" --export json --output ads.json

# Generate specific categories
node generate.js --product "Organic Tea" --categories minimalist,eco

# Generate all categories
node generate.js --product "New App" --all
```

## 类别

### 1. 极简风格
设计简洁明了，注重核心元素，非常适合现代品牌。

### 2. 产品转换
将产品以不同的材料、场景或形式进行创意转换。

### 3. 文化/异国情调
融入文化元素、异国风情和多种美学风格。

### 4. 生活方式
展示产品如何融入理想的生活方式或日常场景中。

### 5. 科技风格
具有未来感、科技感的创意设计，强调数字元素和创新主题。

### 6. 豪华风格
优雅、高档的设计，体现精致与独特性。

### 7. 环保风格
注重可持续性，采用自然、环保的设计理念。

### 8. 季节性风格
根据季节、节日或特殊场合设计合适的广告创意。

### 9. 情感风格
能够触动观众情感的创意设计。

### 10. 轻松幽默风格
有趣、富有想象力的设计，旨在娱乐和吸引观众。

## 输出格式

### JSON
结构化数据格式，便于与其他工具集成：
```json
{
  "product": "Example Product",
  "generated_at": "2025-01-29T12:00:00Z",
  "prompts": [
    {
      "category": "Minimalist",
      "style": "Hand-drawn Minimalist",
      "prompt": "..."
    }
  ]
}
```

### 文本
纯文本格式，易于阅读和复制。

### Markdown
带有标题和结构的Markdown格式，适合文档编写。

## 示例

### 示例1：极简风格的美妆产品广告
```
Product: "Rose Glow Serum"
Style: Hand-drawn Minimalist
Output: Minimalist creative advertisement with hand-drawn elements,
featuring Rose Glow Serum with clean lines, soft pastel accents,
negative space emphasizing the product, botanical sketches of rose
ingredients, elegant typography, white background
```

### 示例2：产品转换广告
```
Product: "Crystal Water Bottle"
Style: Translucent Material
Output: Crystal Water Bottle transformed into translucent paper glass
material, soft light filtering through, visible water layers, delicate
paper-like texture, ethereal lighting, pastel color gradient background
```

### 示例3：异国情调广告
```
Product: "Spice Blend Collection"
Style: Moroccan Market
Output: Spice Blend Collection beauty product in exotic Moroccan market
scene, vibrant souk stalls, golden hour lighting, intricate mosaic
patterns as background, cultural textiles, authenticity, warm color
palette, cinematic composition
```

## 功能特点
- **20多种创意风格**：涵盖多个类别的多样化创意
- **交互式CLI**：用户友好的菜单系统
- **批量生成**：一次生成多个广告创意
- **导出选项**：支持JSON、文本和Markdown格式
- **错误处理**：全面的验证机制和错误提示
- **可定制**：易于修改模板和添加新风格
- **适合实际使用**：代码稳定，支持日志记录和调试

## 文件结构
```
ad-creative-generator/
├── SKILL.md           # This file
├── generate.js        # Main script with CLI
├── templates.js       # Prompt templates by category
└── README.md          # Additional usage documentation
```

## 错误处理
该脚本包含以下方面的全面错误处理：
- 无效的产品名称
- 导出过程中的文件系统错误
- 无效的命令行参数
- 模板渲染错误
- JSON解析错误

## 贡献方式
如需添加新的创意风格：
1. 修改 `templates.js` 文件
2. 添加新的类别或风格信息
3. 遵循现有的代码结构
4. 使用 `node generate.js` 测试新功能

## 许可证
本工具属于Clawdbot技能生态系统的一部分。

## 版本
1.0.0