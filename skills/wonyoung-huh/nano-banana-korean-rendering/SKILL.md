---
name: text-preserve
description: 该技能能够准确地将非拉丁字母（如韩文、日文、中文等）渲染到 AI 生成的图像中。通过结合 Canvas 的预渲染技术（pre-rendering）和 Gemini 工具，确保文本在图像中显示时不会出现乱码或损坏的情况。
tags:
  - korean
  - 한국어
  - 한글
  - japanese
  - chinese
  - rendering
  - text
  - image
  - canvas
  - gemini
  - font
  - typography
  - 텍스트
  - 렌더링
  - 이미지
---

# 多语言文本预渲染技能

AI图像模型在直接绘制韩文、汉字、日文等非拉丁字符时，可能会出现字符显示异常或错误的情况。  
该技能提供了与Web应用完全相同的处理流程：  

1. **detect**：检测提示信息中是否包含非拉丁字符。  
2. **analyze**：使用Gemini LLM从提示信息中提取文本和样式信息。  
3. **render**：使用正确的字体通过Canvas将文本渲染为PNG格式的图像。  
4. **generate**：将渲染后的PNG图像作为输入，生成最终的图像。  

## 首次设置（仅需执行一次）  

```bash
cd {baseDir} && node setup.mjs
```  
- 安装`canvas`和`@google/generative-ai` npm包。  
- 将Noto Sans字体文件放置在`{baseDir}/fonts/`目录下。  

## 环境变量  

| 变量          | 是否必填 | 说明                |  
|---------------|---------|-------------------|  
| `GEMINI_API_KEY`    | ⭐       | 用于Gemini Flash（分析）和Gemini Image（生成）功能 |  
| `GEMINI_IMAGE_MODEL` | 可选      | 图像生成模型（默认：gemini-3-pro-image-preview） |  

---

## 使用流程（分步说明）  

### 一次性执行：`pipeline`  
通过一个命令执行整个流程：  
```bash
node {baseDir}/render.mjs pipeline "욎홎 뙤앾뼡이라는 지역 축제 포스터 만들어줘" \
  --output /tmp/final-image.png --no-base64
```  
**结果：**  
```json
{
  "detect": { "needsRendering": true, "primaryScript": "hangul", ... },
  "analyze": { "texts": [...], "style": {...}, "reasoning": "..." },
  "render": { "success": true, "outputPath": "/tmp/text-render-xxx.png", ... },
  "generate": { "success": true, "outputPath": "/tmp/final-image.png", ... }
}
```  

### 分步执行  

#### 第1步：检测非拉丁字符（`detect`）  
```bash
node {baseDir}/render.mjs detect "사용자 프롬프트 전체"
```  
- 如果`needsRendering`为`false`，则直接生成普通图像（无需预渲染）。  
- 如果`needsRendering`为`true`，则进入第2步。  

#### 第2步：分析Gemini LLM提示信息（`analyze`）  
```bash
node {baseDir}/render.mjs analyze "욎홎 뙤앾뼡이라는 지역 축제 포스터 만들어줘"
```  
Gemini Flash会分析提示信息：  
- 提取需要显示在图像中的文本（包括引号、标签和上下文信息）。  
- 根据设计需求选择合适的字体、大小和颜色。  
- 为每段文本指定其作用（标题、副标题、正文、说明等）。  
- 自动识别每段文本的样式和语言。  
> 如果未设置`GEMINI_API_KEY`，系统会使用预设规则进行处理。  

#### 第3步：使用Canvas进行预渲染（`render`）  
将分析结果直接传递给渲染模块：  
```bash
node {baseDir}/render.mjs render \
  --json '{"texts":[...],"style":{...}}' \
  --output /tmp/rendered-text.png
```  
**或者，也可以将结果保存为JSON文件：**  
```bash
node {baseDir}/render.mjs render --input /tmp/analysis.json --output /tmp/rendered-text.png
```  

#### 第4步：生成最终图像（`generate`）  
将预渲染后的PNG图像作为输入，生成最终的图像：  
```bash
node {baseDir}/render.mjs generate \
  --prompt "욎홎 뙤앾뼡이라는 지역 축제 포스터 만들어줘" \
  --rendered /tmp/rendered-text.png \
  --analysis '{"texts":[...],"style":{...}}' \
  --output /tmp/final-image.png \
  --no-base64
```  
该命令会：  
1. 将PNG图像作为参考图像传递给Gemini。  
2. 使用`buildTextRenderFinalPrompt`函数构建提示内容（包含文本列表、样式信息以及“请直接使用这些文本，无需重新绘制”的指令）。  
3. Gemini会根据这些信息生成融合了文本的最终图像。  
如果需要使用额外的参考图像，可以使用`--ref`参数：  
```bash
node {baseDir}/render.mjs generate \
  --prompt "포스터 만들어줘" \
  --rendered /tmp/rendered-text.png \
  --ref /tmp/user-reference.jpg \
  --output /tmp/final-image.png
```  

## 支持的字体  

| 语言       | sans-serif | serif   | display | handwriting |  
|------------|---------|---------|---------|---------|  
| 韩文       | Noto Sans KR | Noto Serif KR | Black Han Sans | Nanum Pen Script |  
| 日文       | Noto Sans JP | Noto Serif JP | Noto Sans JP | Noto Sans JP |  
| 中文       | Noto Sans SC | Noto Serif SC | Noto Sans SC | Noto Sans SC |  
| 泰文       | Noto Sans Thai |        |        |        |  
| 英文       | Inter    | Georgia | Impact  | Comic Sans MS |  

## 文本各部分的字体大小  

| 文本类型     | 用途       | 大小比例       |  
|------------|-----------|-------------|-----------|  
| 标题        | 主标题     | 1.0x        |            |          |  
| 副标题     | 子标题     | 0.7x        |            |          |  
| 正文       | 正文       | 0.5x        |            |          |  
| 说明/标题    | 图片说明    | 0.4x        |            |          |  

## 字体大小对照表  

| 字体大小（像素） |       |            |           |           |  
| small       | 24px       |            |           |           |  
| medium     | 36px       |            |           |           |  
| large      | 48px       |            |           |           |  
| xlarge     | 72px       |            |           |           |  

## 触发条件  
当用户提示信息中包含以下关键词时，该技能会自动启动：  
`text`, `letter`, `phrase`, `logo`, `watermark`, `brand`, `font`, `title`, `headline`,  
`text`, `logo`, `title`, `headline`，  
或提示信息中包含韩文、汉字、日文、泰文、阿拉伯文等非拉丁字符时。  

## 规则说明：  
- 检测到非拉丁字符时，必须执行整个流程（`detect` → `analyze` → `render` → `generate`）。  
- 使用`analyze`从提示信息中提取文本和样式信息。  
- 通过`render`使用Canvas生成PNG图像。  
- 将生成的PNG图像作为输入，使用`generate`生成最终图像。  

## 注意事项：  
- 不得要求AI模型直接绘制非拉丁字符。  
- 不得在图像提示中直接使用韩文、汉字或日文文本而跳过预渲染步骤。  
- 不得修改`analyze`步骤的输出结果。