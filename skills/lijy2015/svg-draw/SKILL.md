---
name: svg-draw
description: **技能说明：**  
无需使用外部图形库，即可创建 SVG 图像并将其转换为 PNG 格式。该技能适用于生成自定义插图、头像或艺术作品（例如“绘制一条龙”、“创建一个头像”或“制作一个徽标”），或直接将 SVG 文件转换为 PNG 格式。具体实现方式是通过直接编写 SVG 代码（无需依赖 PIL 或 ImageMagick）来完成 SVG 图像的生成，并利用系统自带的 `rsvg-convert` 工具来进行 PNG 转换。
---

# SVG 绘图

使用纯 SVG 代码和系统转换工具生成矢量图形和光栅图像。

## 快速入门

**对于新绘制的图形：**
1. 直接将 SVG 代码写入文件（可以使用 `assets/` 目录中的模板作为起点）
2. 使用转换脚本将其转换为 PNG 格式
3. 通过适当的渠道（如 DingTalk、Telegram 等）发送

**对于现有的 SVG 文件：**
1. 使用转换脚本将 SVG 转换为 PNG 格式
2. 分享生成的图像

## 创建 SVG 图像

### 基本工作流程

1. **选择或创建模板**
   - 查看 `assets/` 目录中的现有模板（例如龙、龙虾等）
   - 或者从头开始编写 SVG 代码

2. **编写 SVG 文件**
   ```bash
   # Example: Write SVG to file
   write('/path/to/output.svg', svg_content)
   ```

3. **转换为 PNG 格式**
   ```bash
   /root/.openclaw/workspace/skills/svg-draw/scripts/svg_to_png.sh input.svg output.png 400 400
   ```

### SVG 结构提示

**务必包含以下内容：**
- 带有 `xmlns="http://www.w3.org/2000/svg"` 和 `viewBox` 属性的 `<svg>` 标签
- 背景 `<rect>` 元素（防止背景显示为透明）
- 适当的 `width` 和 `height` 属性

**常见的 SVG 元素：**
- 形状：`<rect>`、`<circle>`、`<ellipse>`、`<polygon>`、`<path>`
- 文本：使用 `text-anchor="middle"` 使文本居中
- 颜色：使用十六进制代码或命名颜色
- 不透明度：使用 `opacity` 属性实现透明效果

**示例字符结构：**
```
Background → Body → Head → Face features → Limbs → Accessories → Name
```

## 将 SVG 转换为 PNG

使用随附的转换脚本：

```bash
/root/.openclaw/workspace/skills/svg-draw/scripts/svg_to_png.sh <input.svg> <output.png> [width] [height]
```

**参数：**
- `input.svg`：源 SVG 文件路径
- `output.png`：目标 PNG 文件路径
- `width`：输出图像的宽度（默认值：400 像素）
- `height`：输出图像的高度（默认值：400 像素）

**示例：**
```bash
/root/.openclaw/workspace/skills/svg-draw/scripts/svg_to_png.sh dragon.svg dragon.png 512 512
```

## 可用的模板

### 龙模板 (`assets/dragon_template.svg`)
蓝色龙：
- 蜿蜒的身体和翅膀
- 金色的眼睛（带有高光）
- 角和尖耳朵
- 弯曲的尾巴
- 魔法般的光芒
- 名字标签：“大龙 🐉”

**自定义建议：**
- 更改 `fill="#4a90d9"` 以改变身体颜色
- 通过修改 `fill="#ffcc00"` 来调整眼睛颜色
- 添加或删除元素（如鳞片、火焰等）
- 更改背景颜色

### 龙虾模板 (`assets/lobster_template.svg)`
红色龙虾：
- 橙红色的外壳
- 大型的钳子（左右各一个）
- 八条腿
- 长触角
- 尾巴上的扇形结构
- 海洋气泡背景
- 名字标签：“大龙虾 🦞”

**自定义建议：**
- 调整外壳颜色：`fill="#e85d04"`（更深的红色）或 `fill="#f48c06"`（橙色）
- 改变钳子的大小或位置
- 添加更多气泡
- 修改背景

## 设计指南

### 颜色搭配

**友好/可爱的风格：**
- 身体颜色：`#4a90d9`（蓝色）、`#f48c06`（橙色）
- 强调色：`#ffcc00`（黄色）、`#ff6b6b`（珊瑚色）
- 背景颜色：`#1a1a2e`（深蓝色）

**专业风格：**
- 使用柔和的色调
- 限制使用 2-3 种主要颜色
- 如有需要，可以添加细微的渐变效果

### 字符设计原则

1. **保持简洁** —— 在小尺寸下，过多的细节会显得杂乱无章
2. **使用对比** —— 在深色背景上使用明亮的元素
3. **添加个性** —— 添加眼睛、表情等细节
4. **添加标签** —— 在底部添加名称或标题以提供上下文信息
5. **在目标尺寸下测试** —— 在 400x400 的尺寸下查看图像的可读性

## 常见任务

### 创建头像

1. 从符合风格的模板开始（例如龙、龙虾等）
2. 修改颜色和元素
3. 添加个人化的元素（如配饰、表情）
4. 在底部添加名字标签
5. 转换后发送

### 制作徽标

1. 使用简单的几何形状
2. 限制使用 2-3 种颜色
3. 考虑图标的可缩放性
4. 在多种尺寸下测试图像效果
5. 以更高的分辨率（800x800 或 1024x1024）导出图像

### 自定义模板

**更改颜色：** 找到 `fill="#"` 或 `stroke="#"` 属性，并替换其中的十六进制代码

**调整元素大小：** 调整椭圆的 `rx`、`ry` 属性，或矩形的 `width`、`height` 属性

**重新定位元素：** 修改圆形/椭圆的 `cx`、`cy` 属性，或矩形的 `x`、`y` 属性

**添加文本：**
```xml
<text x="200" y="370" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#ffcc00" text-anchor="middle">Your Text</text>
```

## 资源

### 脚本：`
- `svg_to/png.sh` - 使用 `rsvg-convert` 工具将 SVG 转换为 PNG

### 文件目录：
- `assets/`
  - `dragon_template.svg` —— 友好的蓝色龙模板
  - `lobster_template.svg` —— 可爱的红色龙虾模板

## 故障排除

**SVG 无法渲染：**
- 确保存在带有 `xmlns` 属性的正确的 `<svg>` 标签
- 检查 `viewBox` 是否设置正确
- 确保所有标签都已正确闭合

**转换失败：**
- 确认已安装 `rsvg-convert` 工具：运行 `which rsvg-convert` 命令
- 检查文件路径是否正确
- 验证 SVG 语法是否有效

**图像显示异常：**
- 先在浏览器中测试 SVG 图像
- 检查坐标系统（`viewBox` 与 `width`/`height` 的关系）
- 确保元素的堆叠顺序正确（后面的元素会覆盖前面的元素）