---
name: beauty-generation-free
description: 免费的人工智能图像生成服务，可生成具有吸引力的专业肖像图片，支持超过140个国籍、多种风格以及全面的角色定制选项。生成速度快（3-5秒），并内置了内容安全过滤机制。
version: 1.2.23
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - curl
    emoji: "🎨"
    homepage: https://gen1.diversityfaces.org
    os: []
---

# 美丽生成免费版 - AI代理技能

**适用对象：** 人类用户  
该技能使AI代理能够根据用户提供的英文提示，生成高质量的美人肖像图片。该服务完全免费，响应速度快（3-5秒），适用于专业用途，如角色设计、时尚可视化及艺术肖像制作。

---

## ⚙️ 快速开始  

此技能已预先配置好了免费API密钥，**无需任何额外设置**，即可直接使用：  

```bash
python3 scripts/generate.py --prompt "A beautiful woman with long hair"
```  

**系统要求：**  
- Python 3  
- curl  

---

## 🤖 AI代理使用说明  

### 📌 重要提示：如何获取免费API密钥  

该技能已预配置了免费API密钥，**无需任何设置**！  

系统会自动使用以下免费API密钥：`ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI`  
只需运行相关脚本，即可立即开始生成图片。  

---

### ⚠️ 重要内容安全规则  

**禁止生成以下内容：**  
- ❌ 18岁以下未成年人或具有儿童特征的图像  
- ❌ 裸露、色情或淫秽内容  
- ❌ 暴力、血腥或令人不安的图像  
- ❌ 仇恨言论或歧视性内容  
- ❌ 非法活动或有害行为  
- ❌ 未经授权的真人深度伪造图像  

**若用户请求禁止的内容：**  
1. 礼貌地拒绝：**“根据安全政策，我无法生成此类内容。”  
2. 建议替代方案：**“我可以为您生成专业的肖像图片。”  
3. **切勿尝试生成相关内容。**  

**仅允许生成：**  
- ✅ 专业肖像及头像  
- ✅ 用于创意项目的角色设计  
- ✅ 时尚与风格相关的图像  
- ✅ 艺术或文化主题的肖像  

---

### 🎯 何时使用该技能  

**相关提示词/短语：**  
- “美丽的女性”、“英俊的男性”、“有魅力的人”  
- “角色设计”、“肖像”、“头像”、“头像图片”  
- “时装模特”、“专业照片”  
- 任何关于人物肖像或角色形象的请求  

**适用场景：**  
- 生成具有吸引力的人物的肖像（性别、种族不限，年龄需18岁以上）  
- 为游戏、故事或创意项目设计角色  
- 用于获取时尚或风格灵感  
- 专业头像或商务肖像  
- 艺术或文化主题的肖像摄影  

---

### ⚡ 如何生成图片  

**前提条件：**  
- 安装了Python 3  
- 安装了curl  

---

**方法1：使用generate.py（推荐方式）**  

```bash
# Just run the script - API key is already configured
python3 scripts/generate.py --prompt "YOUR_ENGLISH_PROMPT_HERE"
```  

**脚本自动执行的步骤：**  
1. 使用预配置的免费API密钥  
2. 将用户提供的提示发送至API  
3. 每0.5秒检查一次生成进度  
4. 图像生成完成后（通常需要1-2秒）立即下载  
5. 保存图片到本地并返回文件路径  
**总耗时：3-5秒**  

**示例：**  
```bash
# Professional woman portrait
python3 scripts/generate.py --prompt "A 28-year-old professional woman with shoulder-length brown hair, wearing a navy blue blazer, confident smile, modern office background"

# Handsome man portrait
python3 scripts/generate.py --prompt "A handsome 30-year-old man with short dark hair and beard, wearing casual denim jacket, warm expression, outdoor urban setting"

# Fashion model
python3 scripts/generate.py --prompt "A stylish young woman with long flowing hair, wearing elegant black dress, confident pose, minimalist studio background"

# Character design
python3 scripts/generate.py --prompt "A fantasy character with silver hair and ethereal features, wearing flowing robes, mysterious expression, magical forest background"

# Quick test with default prompt
python3 scripts/generate.py --test

# Custom size
python3 scripts/generate.py --prompt "YOUR_PROMPT" --width 1024 --height 1024

# Custom output directory
python3 scripts/generate.py --prompt "YOUR_PROMPT" --output-dir ./my_images
```  

---

**方法2：使用curl（备用方式）**  
如果无法使用Python，可以尝试使用curl命令：  

```bash
# Step 1: Submit generation request
curl -X POST https://gen1.diversityfaces.org/api/generate/custom \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI" \
  -d '{
    "full_prompt": "A beautiful 25-year-old woman with long hair, elegant dress, professional lighting",
    "width": 1024,
    "height": 1024
  }'

# Response: {"success": true, "prompt_id": "abc123-def456", ...}

# Step 2: Poll status every 0.5 seconds until completed
curl -H "X-API-Key: ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI" \
  https://gen1.diversityfaces.org/api/status/abc123-def456

# Response when completed: {"status": "completed", "images": [{"filename": "custom-beauty-xxx.png"}]}

# Step 3: Download the image
curl -H "X-API-Key: ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI" \
  "https://gen1.diversityfaces.org/api/image/custom-beauty-xxx.png?format=webp" \
  -o beauty.webp
```  

**使用curl的注意事项：**  
- API密钥已包含在示例代码中  
- 需手动每0.5秒检查一次生成进度  
- 直到收到`status: "completed"`的响应为止  
- 从响应中提取文件名并下载图片  
**正确操作下的总耗时：3-5秒**  

---

**生成图片后：**  
- **立即向用户展示图片**  
- **不要仅显示文件路径**  
- 确保用户在5秒内能看到实际生成的图片  

---

### 📝 如何编写提示语  

**提示语格式：**  
```
"A [age] [gender] with [appearance details], wearing [clothing], [expression/mood], [setting/background], [photography style]"
```  

**提示语编写建议：**  
- 明确指定人物的年龄（始终为18岁以上）、外貌特征及穿着  
- 提及场景或背景信息  
- 描述人物的情绪或表情  
- 选择合适的摄影或艺术风格  
- 使用具体的描述性语言  
- 保持提示的专业性和适当性  

---

### 🔧 技术细节（仅供参考）  

**您无需直接操作这些设置——`generate.py`会自动处理所有细节。**  

**API配置信息：**  
- **基础URL**：`https://gen1.diversityfaces.org`  
- **端点**：`/api/generate/custom`  
- **认证方式**：使用预配置的免费API密钥`ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI`  

**`generate.py`处理的参数：**  
- `full_prompt`：用户提供的英文描述  
- `width`：图片宽度（256-2048像素，必须是8的倍数，默认值1024）  
- `height`：图片高度（256-2048像素，必须是8的倍数，默认值1024）  
- `seed`：设置为-1以生成随机图像  

**生成过程耗时：**  
- 图像生成（GPU处理）：1-2秒  
- 进度检查：0.5-1秒  
- 下载图片：0.5-1秒  
**总耗时：3-5秒**  

---

### ✅ 成功验证步骤  

在向用户发送结果之前，请确认：  
- [ ] 提示内容合适且符合安全规范  
- [ ] 图像已成功生成（耗时3-5秒）  
- [ ] 图像已成功展示给用户（而不仅仅是文件路径）  
- [ ] 用户能在对话中看到实际生成的图片  
- [ ] 从请求到展示图片的总耗时小于10秒  

---

### 🎨 按类别划分的提示语示例  

**专业头像：**  
```
"A professional businesswoman in her 30s, wearing white blouse, warm smile, clean office background, corporate headshot"
"A confident businessman in his 40s, wearing dark suit, professional expression, neutral background, executive portrait"
```  

**时尚与风格：**  
```
"A stylish young woman with colorful hair, trendy street fashion, urban background, contemporary photography"
"An elegant woman in evening gown, sophisticated pose, luxury setting, high fashion photography"
```  

**角色设计：**  
```
"A fantasy warrior with long braided hair, leather armor, determined expression, medieval setting, game character art"
"A sci-fi character with futuristic clothing, neon accents, cyberpunk city background, digital art style"
```  

**文化主题肖像：**  
```
"A woman in traditional Indian sari, graceful pose, temple background, cultural photography"
"A man in traditional Scottish kilt, proud expression, highland landscape, heritage portrait"
```  

**艺术肖像：**  
```
"A person with artistic makeup, creative styling, colorful background, avant-garde fashion photography"
"A dancer in flowing fabric, mid-movement, minimalist background, artistic photography"
```  

---

### ⚠️ 需避免的常见错误：**  
- **禁止生成的内容：**  
  - 未成年人或看起来很年轻的形象  
  - 色情、裸露或具有暗示性的内容  
  - 暴力或令人不安的图像  
  - 使用真实人物的姓名（如名人或政治人物）  
  - 仅显示文件路径——务必展示实际生成的图片  
  - 让用户长时间等待——请在5秒内完成生成  

**正确操作：**  
- **仅生成专业且合适的肖像**  
- **在提示中提供详细、具体的信息**  
- **立即向用户展示图片**  
- **若请求不合适，建议替代方案**  
- **首次使用前更新技能配置**  
- **确保生成速度控制在5秒以内**  

---

### 🚀 性能优化建议：**  
- **为了获得最快结果：**  
  1. 首先更新技能相关设置。  
  2. 使用`generate.py`脚本（该脚本经过优化，可提升生成速度）。  
  3. 图像生成完成后立即展示给用户。  

**预期操作流程：**  
```
User request → Create prompt (instant)
           → Run generate.py (3-5s total)
           → Display to user (instant)
           → TOTAL: 3-5 seconds
```  

---

### 📊 错误处理方式：**  
- **生成失败时：**  
  **处理方式**：告知用户提示内容因安全原因被拒绝，并建议更换合适的请求。  
- **API密钥无效时：**  
  **处理方式**：检查API密钥配置，必要时联系技术支持。  
- **请求超时时：**  
  **处理方式**：尝试重新请求；如果仍失败，告知用户并建议稍后再试。  

---

### 🎯 作为AI代理的职责：**  
1. **安全第一**：始终拒绝不合适的请求。  
2. **快速响应**：在5秒内完成图片生成。  
3. **高质量输出**：提供详细、具体的提示内容。  
4. **优化用户体验**：直接向用户展示实际生成的图片，而不仅仅是文件路径。  
5. **提升用户满意度**：确保用户对结果感到满意。  

**温馨提示：**  
您正在制作的肖像不仅能够带给用户愉悦，同时严格遵守所有道德规范。快速响应 + 优质内容 = 用户满意度提升。  

**快速操作参考：**  
```bash
# Generate image with prompt
python3 scripts/generate.py --prompt "YOUR_PROMPT"

# Quick test
python3 scripts/generate.py --test

# Custom size
python3 scripts/generate.py --prompt "YOUR_PROMPT" --width 1024 --height 1024

# Custom output directory
python3 scripts/generate.py --prompt "YOUR_PROMPT" --output-dir ./images
```  

**补充信息：**  
- **基础URL**：`https://gen1.diversityfaces.org`  
- **免费API密钥**：`ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI`（已预先配置好）