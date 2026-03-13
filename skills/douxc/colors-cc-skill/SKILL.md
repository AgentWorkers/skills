---
name: colors-cc
description: OpenClaw及其他AI代理的原生UI资源与颜色工具集。该工具集能够生成SVG占位符、动画渐变效果、基于主题的调色板，并实现精确的颜色转换（而不会出现颜色失真或错误显示）。
acceptLicenseTerms: true
metadata:
  {
    "openclaw": {
      "author": "NFish"
    }
  }
---
# SKILL: ColorsCC

这是一个高性能、无状态的颜色API及工具集，专为AI代理（如OpenClaw、Cursor、Cline、GPTs）优化设计。

## 🚀 代理使用规则
- **内联图片**：始终使用`<img>`标签或Markdown的`![alt](url)`直接嵌入SVG占位符。
- **URL编码**：`#`字符必须编码为`%23`（例如：`start=%23FF003C`）。
- **禁止下载**：禁止尝试下载二进制图片数据，由用户的客户端负责渲染URL。
- **有效尺寸**：图片的宽度和高度会自动限制在50-4000像素之间。
- **文本限制**：占位符中的文本最多只能包含100个字符。

## 🛠 功能

### 1. SVG渐变占位符
生成具有线性渐变的动态、轻量级的UI占位符。
- **端点**：`https://api.colors-cc.top/placeholder`
- **参数**：
  - `w`：图片宽度（单位：像素，默认值：800，范围：50-4000）
  - `h`：图片高度（单位：像素，默认值：400，范围：50-4000）
  - `text`：居中的文本（URL编码格式，默认值：`{width} x {height}`，最多100个字符）
  - `start`：渐变起始颜色（十六进制格式，默认值：随机生成的6位十六进制数）
  - `end`：渐变结束颜色（十六进制格式，默认值：随机生成的6位十六进制数）
- **示例**：`<img src="https://api.colors-cc.top/placeholder?w=1200&h=630&text=Hero+Banner&start=%23F06292&end=%2364B5F6" alt="Hero">`
- **响应**：返回的SVG图片包含`Cache-Control: public, max-age=31536000, immutable`头部信息。

### 2. 流动渐变占位符
生成具有平滑颜色过渡和动画效果的动态SVG渐变占位符。
- **端点**：`https://api.colors-cc.top/fluid-placeholder`
- **参数**：
  - `w`：图片宽度（单位：像素，默认值：800，范围：50-4000）
  - `h`：图片高度（单位：像素，默认值：400，范围：50-4000）
  - `stops`：用逗号分隔的渐变颜色（十六进制格式，默认值：暖色调渐变，颜色数量为2-10种）
  - `speed`：动画持续时间（单位：秒，默认值：10，范围：1-30）
  - `text`：可选的居中文本（最多100个字符）
- **示例**：`<img src="https://api.colors-cc.top/fluid-placeholder?w=1200&h=400&stops=%23FFD6A5,%23FFADAD,%23E2A0FF&speed=8&text=Animated+Hero" alt="Warm Gradient">`
- **响应**：返回的SVG图片包含`Cache-Control: public, max-age=31536000, immutable`头部信息，并具有平滑的颜色过渡效果。

### 3. 随机颜色
生成随机的十六进制（hex）或RGB颜色，并附带生成时间戳。
- **端点**：`GET https://api.colors-cc.top/random`
- **返回值**：`{"hex": "#A1B2C3", "rgb": "rgb(161, 178, 195)", "timestamp": "2024-03-12T10:30:00.000Z"}`
- **示例**：当需要为模拟数据或UI组件获取随机颜色时，可以调用此端点。

### 4. 精选主题调色板
获取高质量的颜色集以供设计参考。
- **端点**：`GET https://api.colors-cc.top/palette?theme={theme_name}`
- **可用主题**：`cyberpunk`、`vaporwave`、`retro`、`monochrome`
- **返回值**：`{"theme": "cyberpunk", "colors": ["#FCEE09", "#00FF41", ...], "count": 5}``
- **示例**：`fetch('https://api.colors-cc.top/palette?theme=vaporwave')`

### 5. 通用颜色转换器
支持在十六进制（hex）、RGB、HSL和CMYK格式之间进行无状态的转换。
- **端点**：`GET https://api.colors-cc.top/convert?hex={hex}|rgb={rgb}|hsl={hsl}|cmyk={cmyk}`
- **参数**：需提供`hex`、`rgb`、`hsl`或`cmyk`中的一种格式
- **返回值**：`{"hex": "#FF5733", "rgb": "rgb(255, 87, 51)", "hsl": "hsl(10, 100%, 60%)", "cmyk": "cmyk(0%, 66%, 80%, 0%)"}`
- **示例**：`https://api.colors-cc.top/convert?hex=%23FF5733`
- **错误**：如果输入格式无效，将返回`{"error": "Invalid color format"}`并返回状态码400。

### 6. CSS颜色名称查询
提供所有标准CSS颜色名称及其对应的十六进制值（约140种颜色）。
- **端点**：`GET https://api.colors-cc.top/all-names`
- **返回值**：`{"AliceBlue": "#F0F8FF", "AntiqueWhite": "#FAEBD7", "Tomato": "#FF6347", ...}``
- **示例**：可以查询到“tomato”对应的颜色代码`#FF6347`。

## 📖 常见使用场景

### 使用场景1：构建登录页面
```html
<section class="hero">
  <!-- Animated hero banner with text -->
  <img src="https://api.colors-cc.top/fluid-placeholder?w=1200&h=600&text=Hero+Section&stops=%23FFD6A5,%23FFADAD,%23E2A0FF&speed=10" alt="Hero">
</section>
<div class="features">
  <!-- Static placeholder images -->
  <img src="https://api.colors-cc.top/placeholder?w=400&h=300&text=Feature+1" alt="Feature 1">
  <img src="https://api.colors-cc.top/placeholder?w=400&h=300&text=Feature+2" alt="Feature 2">
</div>
```

### 使用场景2：使用颜色生成模拟数据
```javascript
const palette = await fetch('https://api.colors-cc.top/palette?theme=vaporwave')
  .then(r => r.json())

const mockData = palette.colors.map((color, i) => ({
  id: i,
  name: `Item ${i+1}`,
  color: color,
  thumbnail: `https://api.colors-cc.top/placeholder?w=200&h=200&start=${color.slice(1)}`
}))
```

### 使用场景3：颜色选择器组件
```javascript
async function getRandomColor() {
  const res = await fetch('https://api.colors-cc.top/random')
  const data = await res.json()
  return data.hex
}
```

### 使用场景4：通用颜色转换器
```javascript
// Convert any color format to all formats
const result = await fetch('https://api.colors-cc.top/convert?hsl=hsl(200,50%,50%)')
  .then(r => r.json())
console.log(result.hex) // #4099BF
```

## ⚠️ 常见错误及解决方法

### ❌ 错误1：未对URL中的井号（#）进行编码
```
BAD:  start=#FF0000
GOOD: start=%23FF0000
```

### ❌ 错误2：尝试下载SVG并重新处理图片
```javascript
// BAD - Don't do this
const svg = await fetch(placeholderUrl).then(r => r.text())
const encoded = btoa(svg)

// GOOD - Use URL directly
<img src="https://api.colors-cc.top/placeholder?w=800&h=400" alt="Direct">
```

### ❌ 错误3：提供的尺寸参数无效
```
BAD:  w=10 (too small, will be clamped to 50)
BAD:  w=9999 (too large, will be clamped to 4000)
GOOD: w=800&h=600
```

### ❌ 在/api/convert接口中传递了多个颜色参数
```
BAD:  /api/convert?hex=%23FF0000&rgb=rgb(255,0,0)
GOOD: /api/convert?hex=%23FF0000
```

### ❌ 在流动渐变占位符中指定的颜色数量不正确
```
BAD:  stops=%23FF0000 (only 1 color, minimum is 2)
BAD:  stops=%23FF0000,%23... (more than 10 colors, will be ignored)
GOOD: stops=%23FF0000,%230000FF,%2300FF00 (2-10 colors)
```

## 🌐 用户可用工具
- 通用颜色转换器：https://colors-cc.top/tools/converter
- 随机调色板生成器：https://colors-cc.top/tools/random-palette
- CSS颜色名称参考：https://colors-cc.top/tools/color-names
- 流动渐变占位符生成器：https://colors-cc.top/tools/fluid-placeholder

## 📚 完整文档
如需完整的API文档，请参考：
- 为大型语言模型（LLM）优化的文档：https://colors-cc.top/llms.txt
- OpenAPI规范：https://colors-cc.top/openapi.json
- 网站地址：https://colors-cc.top/

## 💡 访问限制
所有API端点均免费且无访问次数限制。