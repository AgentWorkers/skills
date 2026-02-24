---
name: menuvision
description: "使用 Gemini Vision 和 AI 图像生成技术，您可以根据餐厅的网址、PDF 文件或照片来创建美观的 HTML 照片菜单。"
version: 1.0.0
emoji: "🍽️"
user-invocable: true
metadata: {"openclaw": {"requires": {"env": ["GOOGLE_API_KEY"], "bins": ["python3"]}, "primaryEnv": "GOOGLE_API_KEY", "homepage": "https://github.com/ademczuk/MenuVision"}}
---
# MenuVision - 餐厅菜单生成器

该工具可根据餐厅提供的URL、PDF文件或照片，生成美观的HTML格式菜单。

## 使用场景

当用户需要为餐厅创建数字菜单时。触发命令包括：`build a menu`、`create restaurant menu`、`menu from PDF`、`menu from photos`、`digital menu`、`menuvision`。

## 快速入门

1. **数据提取**：从URL/PDF/照片中提取菜单数据（使用`Gemini Vision`模块）。
2. **图片生成**：根据提取的数据生成菜品图片（使用`Gemini Image`模块）。
3. **页面构建**：将菜单数据和图片合并生成完整的HTML页面（包含内联的CSS/JS代码，图片路径使用相对路径）。

### 示例用法

- “为https://www.shoyu.at/menus生成菜单”
- “根据这份PDF文件创建菜单”
- “根据这些餐厅菜单的照片制作数字菜单”

## 工作流程组件

AI代理会执行以下脚本：

| 脚本 | 功能 |
|--------|---------|
| `extract_menu.py` | 从URL/PDF/照片中提取菜单数据并转换为结构化JSON |
| `generate_images.py` | 使用`Gemini Image`生成菜品图片 |
| `build_menu.py` | 根据JSON数据和图片构建HTML页面（内含CSS/JS代码，图片路径为相对路径） |
| `publish_menu.py` | （可选）将生成的HTML页面发布到GitHub Pages |

---

## 数据规范

所有流程阶段都使用相同的JSON格式。AI代理必须严格遵循这些字段名称，任何偏差都可能导致流程失败。

### menu_data.json 数据结构

```json
{
  "restaurant": {
    "name": "餐厅名称（如果显示在页面上）",
    "cuisine": "菜品类型（中式、印度菜、奥地利菜、日式等）",
    "tagline": "餐厅标语或宣传语"
  },
  "sections": [
    {
      "title": "章节标题（主语言）",
      "title_secondary": "章节标题（次要语言，如果存在）",
      "category": "食物或饮料",
      "note": "章节备注（例如‘配米饭食用’、‘周一至周五11:00-15:00’）",
      "items": [
        {
          "code": "M1",
          "name": "菜品名称（主语言）",
          "name_secondary": "菜品名称（次要语言，如果存在）",
          "description": "简要描述（主语言）",
          "description_secondary": "简要描述（次要语言，如果存在）",
          "price": "12,90",
          "price_prefix": "",
          "allergens": "A C F",
          "dietary": ["vegan", "spicy"],
          "variants": []
        }
      ]
    }
  ],
  "allergen_legend": {
    "A": "麸质",
    "B": "甲壳类"
  },
  "metadata": {
    "languages": ["German", "English"],
    "currency": "EUR"
  }
}
```

### 字段说明

- `restaurant`：餐厅的基本信息。
- `sections`：菜单的各个章节。
- `items`：每个章节中的菜品信息。
- `allergen_legend`：食物中的过敏原信息。
- `metadata`：菜单支持的语言和货币格式。

---

## 提取规则

请严格按照以下提示向Gemini发送请求：

```python
您是一个餐厅菜单数据提取工具。请分析此菜单内容，并将所有菜品信息提取为结构化JSON格式。

返回以下JSON结构：
```json
{
  "restaurant": {
    ...
  },
  "sections": {
    ...
  },
  "allergen_legend": {
    ...
  },
  "metadata": {
    ...
  }
}
```

**重要规则：**
1. 请提取所有菜品信息，不要遗漏任何菜品。
2. 保留原始的菜品代码（如M1、K2等）。如果不存在，请为每个章节生成连续的代码（例如，开胃菜用A1、A2表示）。
3. 请严格按照原始格式提取价格（例如“12,90”）。
4. 如果菜品有价格前缀（如“ab”），请将其包含在`price_prefix`字段中。
5. 如果菜品有多种规格/数量选项（例如“6份/8.90元”），请使用`variants`数组进行表示。
6. 请准确提取过敏原代码（如“A”、“B”等）。
7. 如果菜单有过敏原提示，请将其包含在`allergen_legend`中。
8. 请根据描述或图标识别饮食限制（如素食、辣味、无麸质、清真等）。
9. 如果菜单是双语的，请同时保留两种语言信息。
10. 对于固定价格的多选菜单或午餐特餐，请创建一个带有说明的章节，并将每个选项作为单独的菜品列出。
11. 将每个章节分类为“食物”或“饮料”。
12. 即使是饮料，也请提取名称、价格和规格信息。

---

## 特殊情况（基于图片的输入）

对于截图、PDF页面或照片输入，请在基础提示前添加以下上下文：

```python
EXTRACTION_PROMPT_VISION = (
    "您是一个餐厅菜单数据提取工具。"
    "这是一张餐厅菜单页面的截图/扫描图片。"
    "返回以下JSON结构："
    + EXTRACTION_PROMPT.split("返回以下JSON结构:")[1]
```

根据输入类型，会在基础提示前添加相应的前缀：

| 输入类型 | 添加的前缀 |
|---------|-----------|
| 截图 | `"这是{url}餐厅菜单网页的截图。提取所有可见的菜单项目。" |
| PDF页面 | `"这是餐厅菜单PDF的第{n}页。从该页面提取所有菜单项目。" |
| 照片 | `"这是一张餐厅菜单的照片。提取所有可见的菜单项目。" |
| 静态HTML | 直接使用`EXTRACTION_PROMPT`（无需特殊处理） |
```

---

## Gemini API配置

```python
import os
from google import genai

client = genai.Client(os.environ["GOOGLE_API_KEY"]

def gemini_config():
    return genai.types.GenerateContentConfig(
        max_output_tokens=65536,          # 用于处理大型菜单
        response_mime_type="application/json",  # JSON格式
    )

# 使用的模型：gemini-2.5-flash（默认）
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt_text,    # 或 [image, prompt_text] （针对图片输入）
    config=gemini_config(),
)
```

---

## 图片生成

```python
def build_food_prompt(name: str, description: str, cuisine: str = "") -> str:
    # ...
```

## 其他细节

- 文件命名规则：文件名根据餐厅名称或URL生成。
- 图片路径使用相对路径，以确保跨平台兼容性。
- HTML页面使用内联的CSS/JS代码，并引用相对路径的图片文件。
- 对于缺失的图片，使用Base64编码的SVG占位符。
- 支持多种语言和字体格式。
- 提供货币转换功能，允许用户在页面上切换货币显示。

---

## 部分代码示例

```python
import base64
import html_mod
import re

# ... （其他代码实现细节）
```

---

## 注意事项

- 请确保安装所有必要的依赖库，并设置正确的环境变量。
- 构建脚本包含自动重试逻辑，以处理API调用失败的情况。
- 提供了详细的错误处理和优化措施，以确保输出的稳定性和准确性。