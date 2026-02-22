---
name: menuvision
description: "使用 Gemini Vision 和 AI 图像生成技术，可以从餐厅的网址、PDF 文件或图片中生成精美的 HTML 照片菜单。"
version: 1.0.0
emoji: "🍽️"
user-invocable: true
metadata: {"clawdbot": {"requires": {"env": ["GOOGLE_API_KEY"], "bins": ["python3"]}, "primaryEnv": "GOOGLE_API_KEY", "homepage": "https://github.com/ademczuk/MenuVision"}}
---
# MenuVision - 餐厅菜单生成器

**功能：**  
根据餐厅提供的URL、PDF文件或照片，生成美观的HTML格式菜单。

## 使用场景：**  
当用户需要为餐厅创建数字菜单时。相关指令包括：`build a menu`、`create restaurant menu`、`menu from PDF`、`menu from photos`、`digital menu`、`menuvision`。

## 快速入门：**  
1. **数据提取：** 从URL/PDF/照片中提取菜单数据（使用`Gemini Vision`模块）。  
2. **图片生成：** 根据提取的数据生成菜品图片（使用`Gemini Image`模块）。  
3. **菜单构建：** 将菜单数据和图片合并，生成完整的HTML页面（包含内联的CSS/JS代码；图片路径为相对路径）。  

### 示例用法：**  
- “为https://www.shoyu.at/menus生成菜单”。  
- “根据这份PDF创建菜单”。  
- “根据这些餐厅菜单的照片生成数字菜单”。  

## 工作流程：**  
AI代理执行以下步骤：  
- `extract_menu.py`：从URL/PDF/照片中提取菜单数据（生成`menu_data.json`文件）。  
- `generate_images.py`：使用`Gemini Image`生成菜品图片。  
- `build_menu.py`：使用`menu_data.json`和生成的图片构建HTML页面（包含内联的CSS/JS代码；图片路径为相对路径）。  

### 数据格式：**  
`menu_data.json`文件包含以下结构：  
```json
{
  "restaurant": {
    "name": "餐厅名称",
    "cuisine": "菜品类型（中餐、印度菜、奥地利菜、日餐等）",
    "tagline": "餐厅标语"
  },
  "sections": [
    {
      "title": "章节名称",
      "title_secondary": "章节名称（如果有第二语言版本，则显示）",
      "category": "食物或饮料",
      "note": "章节备注（例如：‘配米饭食用’、‘周一至周五11:00-15:00’）",
      "items": [
        {
          "code": "M1",
          "name": "菜品名称",
          "name_secondary": "菜品名称（如果有第二语言版本，则显示）",
          "description": "简要描述",
          "description_secondary": "详细描述（如果有第二语言版本，则显示）",
          "price": "12.90",
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
    "languages": ["德语", "英语"],
    "currency": "EUR"
  }
}
```

### 注意事项：**  
1. 保持技术准确性，自然翻译内容。  
2. 保留所有代码示例、命令和URL。  
3. 保持Markdown格式不变。  
4. 在适当的情况下使用英文技术术语（如OpenClaw、ClawHub、API、CLI）。  
5. 仅翻译代码块中的解释性注释。  
6. 保持原始结构和组织结构不变。  
7. 不要添加或删除任何部分。  
8. 原始的`___CODE_BLOCK_0___`占位符保持不变。