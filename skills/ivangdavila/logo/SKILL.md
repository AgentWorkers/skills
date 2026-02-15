---
name: Logo
description: 使用人工智能图像工具，通过有效的提示结构（prompt structures）和验证流程（validation loops）生成适用于App Store图标和品牌标志的Logo。
---

## 快速入门：AI标志生成

**最适合大多数标志的模型：Nano Banana Pro**（Gemini 3 Pro 图像）

### 基本提示公式
```
Create a [STYLE] logo featuring [ELEMENT] on [BACKGROUND].
[DESCRIPTION]. The logo should look good at 32px with recognizable shapes.
```

### 示例
```
Create a minimalist logo featuring a geometric mountain peak on white background.
Clean lines, navy blue (#1E3A5A), modern and professional style.
The logo should look good at 32px with recognizable shapes.
```

如需查看完整的 7 步提示框架和模型比较，请参阅 `ai-generation.md`。

---

## 决策树

| 情况 | 参考文档 |
|-----------|------|
| AI 生成（Nano Banana、GPT Image、提示、iOS 图标） | `ai-generation.md` |
| 标志类型（文字标志、符号、组合标志、徽标） | `types.md` |
| 与设计师合作进行设计 | `process.md` |
| 文件格式和导出要求 | `formats.md` |
| 不使用 AI 的自主设计（模板、Canva） | `diy.md` |
| 雇佣设计师或设计机构 | `hiring.md` |

---

## 模型快速参考

| 模型 | 最适合生成的内容 |
|-------|----------|
| **Nano Banana Pro** | 文字 + 图标，适用于 App Store 图标 |
| **GPT Image 1.5** | 适用于需要自然语言交互的场景 |
| **Ideogram** | 适用于需要完美文本渲染的情况 |
| **Midjourney v7** | 仅适用于生成艺术风格的图标（不支持文本） |

---

## iOS 应用图标（Liquid Glass 设计）

iOS 26 使用 Liquid Glass 设计规范。请使用以下提示结构：

```
Create a polished iOS app icon featuring [ELEMENT].
Rounded square with [COLOR] gradient, minimalist white symbol centered.
Soft shadows, glassy depth effect, works at 60px.
The icon represents [APP PURPOSE].
```

完整的 iOS 26 提示模板请参阅 `ai-generation.md`。

---

## 验证流程（必选）

**在分享之前，务必进行视觉审核。** 所有 AI 生成的成果都必须经过检查：

1. 生成标志 → 2. 查看实际图像 → 3. 检查是否存在问题 → 4. 修复问题或重新生成 → 5. 重复上述步骤（最多尝试 5-7 次）

**常见问题及解决方法：**
- 图标边缘有不必要的空白区域 → 裁剪图像 |
- 图标中的元素被裁剪掉 → 使用“居中布局”重新生成 |
- 文字显示混乱 → 使用 Nano Banana 或 Ideogram 工具进行修复，或手动调整文本 |
- 图标过于复杂 → 简化提示内容 |

如果经过 5-7 次尝试仍然无法得到满意的结果，请更换模型或调整生成策略。

---

## 常见注意事项

- **AI 生成的成果只是一个起点。** 所有 AI 生成的标志都需要进行矢量化处理、清理，并对文本进行手动优化。切勿直接使用原始输出作为最终版本。
- **尽早在小尺寸下进行测试。** 如果标志在 32px 尺寸下显示效果不佳，说明设计过于复杂，需要简化。
- **不同模型的文本渲染能力各不相同。** 只有 Nano Banana 和 Ideogram 能够可靠地渲染文本；对于 Midjourney，建议仅生成图标。
- **简单的标志更经得起时间考验。** 例如 Nike、Apple、McDonald’s 的标志就非常简洁明了。

---

## 在最终确定设计之前需要确认的事项：

- 标志是否能在黑白背景下正常显示 |
- 标志在 32px 尺寸下是否清晰可读（用于生成favicon） |
- 标志是否为矢量格式（SVG），而不仅仅是 PNG 图像 |
- 是否已经生成了多种样式（水平排列、堆叠显示、仅显示图标等） |
- 文字是否经过手动优化，而非由 AI 生成 |
- 标志在深色和浅色背景下的显示效果是否正常

---

## 何时需要进一步参考其他文档

| 情况 | 参考文档 |
|-----------|-----------|
- 需要完整的提示框架或模型比较信息 | `ai-generation.md` |
- 需要确定使用文字标志、符号还是徽标 | `types.md` |
- 需要与设计师合作或使用设计模板 | `process.md` |
- 需要了解文件格式和导出要求 | `formats.md` |
- 需要记录设计过程中的经验并从中学习 | `feedback.md` |