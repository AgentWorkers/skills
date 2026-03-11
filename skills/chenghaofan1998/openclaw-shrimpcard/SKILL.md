---
name: openclaw-shrimpcard
description: 为 OpenClaw 创建 ShrimpCard 输出内容。当用户请求生成龙虾/虾的卡片时，可以使用这些输出内容；这些输出应符合 ShrimpCard 的 JSON 和图像格式要求。同时，当图像无法获取时，系统还应能够提供基于像素艺术的 HTML 渲染作为备用方案。
---
# OpenClaw ShrimpCard

## 概述  
根据用户输入和系统内存数据生成准确的 ShrimpCard JSON 数据（以及可选的图片/描述），然后根据预定义的 JSON 模式验证数据。如果无法生成图片，系统会使用像素艺术风格的默认头像作为替代方案，并渲染相应的 HTML 页面。

## 工作流程  

1. **收集所需字段**  
   - 必需字段：`name`（名称）、`tagline`（标语）、`description`（描述）、`top_skills`（3 项核心技能）、`owner.name`（所有者名称）、`lobster_image_desc`（龙虾/虾的图片描述）、`card_id`（卡片 ID）。  
   - 如果缺少任何必填信息，需向用户询问并补齐。  

2. **构建卡片对象**  
   - 遵循 `references/card-schema.json` 中定义的 JSON 模式进行数据结构构建。  
   - 确保 `lobster_image_desc` 包含有效的龙虾或虾的图片描述。  
   - 如果无法获取图片，设置 `image.placeholder` 并保留 `lobster_image_desc`。  

3. **输出前的验证**  
   - 运行 `scripts/validate_card.py <json-file>` 进行数据验证。  
   - 如果验证失败，需修复数据并重新验证。  

4. **HTML 渲染**  
   - 当图片生成失败或用户请求 HTML 格式时执行渲染：  
     - 使用 `assets/card-template.html` 作为模板。  
     - 将 JSON 数据映射到 `window.__CARD_DATA__`（具体映射规则见 `references/html-mapping.md`）。  
     - 如果没有图片 URL 或数据 URL，使用 `assets/pixel-lobster.svg` 作为默认头像。  
     - 可通过 `scripts/render_card_html.py <card-json> --out shrimp-card.html` 生成可直接使用的 HTML 文件。  

5. **输出结果**  
   - 如果用户需要文件格式，将生成的 JSON 数据（`shrimp-card.json`）写入磁盘；  
   - 如果用户请求 JSON 数据，直接将其作为响应内容返回；  
   - 如果用户请求 HTML 页面，输出 `shrimp-card.html`；  
   - 如果用户请求图片，需提供图片的 URL 或描述；如果图片生成失败，使用默认的像素艺术头像并渲染 HTML 页面。  

6. **图片生成辅助（可选）**  
   - 如果用户希望自行生成图片，可使用 `references/card-spec.md` 中提供的模板进行指导。  
   - 提醒用户在图片中添加二维码，并将其嵌入到页面的页脚区域。  

## 准确性要求**  
   - 不得虚构所有者信息或联系方式；如信息缺失，需向用户核实。  
   - `top_skills` 必须严格限制为 3 项，这些技能由 OpenClaw 系统自动选择（不一定是用户最常用的技能）。  
   - 文本内容应简洁明了，以适应卡片布局。  
   - 如果图片生成失败，始终使用像素艺术头像作为替代方案，确保页面仍能正常显示。  

## 资源文件  

### 脚本文件（scripts/）  
- `validate_card.py`：验证 JSON 数据是否符合格式要求。  
- `render_card_html.py`：将 ShrimpCard JSON 数据插入 HTML 模板，并使用像素艺术头像作为替代方案。  

### 参考文档（references/）  
- `card-schema.json`：JSON 数据结构规范。  
- `sample-card.json`：示例数据样本。  
- `card-spec.md`：字段要求及样式说明。  
- `html-mapping.md`：JSON 数据与 HTML 页面的映射规则及像素头像的替代方案。  

### 资源文件（assets/）  
- `card-template.html`：单文件 HTML 卡片模板，支持 `window.__CARD_DATA__` 数据结构。  
- `pixel-lobster.svg`：用于替代方案的像素艺术头像图片。