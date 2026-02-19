# 提示库（Prompt Library）

用于存储、整理和检索可重复使用的提示模板。避免重复编写相同的提示内容——构建属于您自己的提示库。

## 工具（Tools）

### `prompt_save`  
将提示模板保存到您的提示库中。  

**参数：**  
- `name`（字符串，必填）：提示的简短名称（例如：“blog-outline”、“sales-email”）  
- `template`（字符串，必填）：提示模板的文本内容。请使用 `{{variable}}` 作为占位符。  
- `category`（字符串，可选）：提示所属的类别（例如：“writing”、“coding”、“research”、“sales”）  
- `description`（字符串，可选）：提示的简要描述  
- `variables`（字符串数组，可选）：模板中使用的变量名称列表  

**返回值：** 包含提示 ID 的确认信息。  

### `prompt_search`  
根据关键词或类别搜索您的提示库。  

**参数：**  
- `query`（字符串，可选）：用于匹配提示名称、描述或模板内容的搜索词  
- `category`（字符串，可选）：按类别过滤  
- `limit`（数字，可选）：返回的最大结果数量，默认为 10  

**返回值：** 匹配的提示列表，包含提示的名称、类别和预览内容。  

### `prompt_use`  
检索提示模板并填充变量内容。  

**参数：**  
- `name`（字符串，必填）：要使用的提示的名称  
- `variables`（对象，可选）：用于填充 `{{variable}}` 占位符的键值对  

**返回值：** 填充好内容的提示模板，可直接使用。  

### `prompt_list_categories`  
列出提示库中的所有类别及其对应的提示数量。  

**返回值：** 类别名称及其对应的提示数量。  

### `prompt_delete`  
从提示库中删除某个提示。  

**参数：**  
- `name`（字符串，必填）：要删除的提示的名称  

**返回值：** 删除操作的确认信息。  

### `prompt_export`  
将整个提示库导出为 JSON 格式。  

**返回值：** 提示库的完整数据。  

## 存储方式（Storage）  
提示模板以单独的 Markdown 文件形式存储在 `memory/prompts/` 目录下，便于版本控制和移植。  

## 使用示例（Example Usage）  
```
Save: prompt_save name="cold-email" template="Hi {{name}}, I noticed {{observation}}. I built {{product}} that could help with {{pain_point}}. Would you be open to a quick look?" category="sales"

Search: prompt_search query="email" category="sales"

Use: prompt_use name="cold-email" variables={"name": "Alex", "observation": "your team ships weekly", "product": "a deployment tracker", "pain_point": "release coordination"}
```  

## 为何需要这个工具（Why This Exists）  
随着时间的推移，使用提示库的代理程序会变得更加高效。无需每次会话都从头开始创建提示，而是可以重用已有的有效模板。这样能够提升提示设计的效率。  

## 标签（Tags）  
utility（实用工具）、productivity（生产力）、prompts（提示）、templates（模板）、writing（写作）