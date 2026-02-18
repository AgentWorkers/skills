---
name: beauty-generation-free
description: 免费的人工智能图像生成服务，可用于创建具有吸引力的专业肖像图片，支持多种定制选项。支持140多个国籍、多种风格以及全面的角色定制。生成速度快（3-5秒），并内置了内容安全过滤机制。
version: 1.2.26
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
# Beauty Generation Free - AI Agent Skill

**功能说明：**  
该技能允许AI代理根据用户提供的英文提示，生成高质量的人物肖像图片。该服务完全免费且响应迅速（仅需3-5秒），适用于专业用途，如角色设计、时尚视觉化及艺术肖像创作。

---

## ⚙️ 快速入门  
该技能已预配置了免费的API密钥，无需额外设置，可直接使用：  
```bash
python3 scripts/generate.py --prompt "A beautiful woman with long hair"
```

**系统要求：**  
- Python 3  
- curl  

---

## 🤖 AI代理使用说明  

### 📌 重要提示：如何获取免费API密钥  
该技能已预配置了免费的API密钥，无需任何设置！  
您只需运行相关脚本即可立即开始生成图片。  

---

### ⚠️ 内容安全规则  
**严禁生成以下内容：**  
- ❌ 18岁以下未成年人或具有儿童特征的图像  
- ❌ 裸露、色情或淫秽内容  
- ❌ 暴力、血腥或令人不适的图像  
- ❌ 仇恨言论或歧视性内容  
- ❌ 非法活动或有害行为  
- ❌ 未经授权的真人深度伪造图片  

**若用户请求禁止的内容：**  
1. 礼貌地拒绝：**“根据安全政策，我无法生成此类内容。”  
2. 建议替代方案：**“我可以为您生成专业的肖像图片。”  
3. **严禁生成上述内容。**  

**允许生成的内容：**  
- ✅ 专业肖像及头像  
- ✅ 用于创意项目的角色设计  
- ✅ 时尚与风格相关的视觉素材  
- ✅ 艺术或文化主题的肖像图片  

---

### 🎯 适用场景  
**使用提示词/短语：**  
- “美丽的女性”、“英俊的男性”、“有魅力的人”  
- “角色设计”、“肖像”、“头像”、“头像图片”  
- “时装模特”、“专业照片”  
- 任何与人物肖像或角色形象相关的请求  

**适用场景：**  
- 生成具有吸引力的人物肖像（性别、种族不限，年龄需18岁以上）  
- 为游戏、故事或创意项目设计角色形象  
- 提供时尚或风格灵感图片  
- 生成专业头像或商务肖像  
- 创作艺术或文化主题的肖像图片  

---

### ⚡ 图片生成方法  

**前提条件：**  
- 安装了Python 3  
- 安装了curl  

---

**方法1：使用generate.py（推荐方式）**  
```bash
# Just run the script - API key is already configured
python3 scripts/generate.py --prompt "YOUR_ENGLISH_PROMPT_HERE"
```  
**脚本自动执行步骤：**  
1. 使用预配置的免费API密钥  
2. 将用户提供的提示发送至API  
3. 每0.5秒检查一次生成进度  
4. 图像生成完成后（约1-2秒）下载并保存  
5. 返回图片文件路径  
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
（如无法使用Python，可尝试使用curl命令）：  
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
**注意：**  
- 示例中已包含API密钥  
- 需手动每0.5秒检查一次生成进度  
- 确认状态变为“completed”后下载图片  
**总耗时：3-5秒（假设请求正确处理）**  

---

**生成完成后：**  
- **立即向用户展示图片**  
- **不要仅提供文件路径**  
- 确保用户在5秒内能看到实际生成的图片  

---

### 📝 提示编写指南  
**提示格式：**  
```
"A [age] [gender] with [appearance details], wearing [clothing], [expression/mood], [setting/background], [photography style]"
```  
**示例提示：**  
```python
# Professional woman
"A 28-year-old professional woman with shoulder-length brown hair, wearing a navy blue blazer, confident smile, modern office background, corporate headshot style"

# Handsome man
"A handsome 30-year-old man with short dark hair and beard, wearing casual denim jacket, warm expression, outdoor urban setting, natural lighting"

# Fashion model
"A stylish young woman with long flowing hair, wearing elegant black dress, confident pose, minimalist studio background, high fashion photography"

# Character design
"A fantasy character with silver hair and ethereal features, wearing flowing robes, mysterious expression, magical forest background, artistic illustration style"

# Cultural portrait
"A graceful woman in traditional Japanese kimono, serene expression, cherry blossom garden, soft natural lighting, artistic photography"
```  
**编写提示时请注意：**  
- 明确指定年龄（务必为18岁以上）、外貌特征及穿着风格  
- 提及场景或背景信息  
- 描述所需的情感或表情  
- 使用具体的形容词  
- 保持提示的专业性和适当性  

---

### 🔧 技术细节（仅供参考）  
您无需直接操作这些设置，`generate.py`会自动处理所有细节：  
- **API地址：** `https://gen1.diversityfaces.org`  
- **端点：** `/api/generate/custom`  
- **认证方式：** 使用预配置的免费API密钥 `ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI`  
- **参数说明：**  
  - `full_prompt`：用户提供的英文描述  
  - `width`：256-2048像素（8的倍数，默认1024）  
  - `height`：256-2048像素（8的倍数，默认1024）  
  - `seed`：-1表示随机生成  

**生成流程：**  
- GPU处理时间：1-2秒  
- 进度检查时间：0.5-1秒  
- 下载时间：0.5-1秒  
**总耗时：3-5秒**  

---

### ✅ 成功验证步骤  
在向用户发送结果前，请确认：  
- [ ] 提示内容合适且符合安全规范  
- [ ] 图像已成功生成（耗时3-5秒）  
- [ ] 图像已正确展示给用户  
- [ ] 用户能在对话中看到实际生成的图片  
- [ ] 从请求到展示的总时间不超过10秒  

---

### 🎨 按类别划分的示例提示：  
- **专业头像：**  
```
"A professional businesswoman in her 30s, wearing white blouse, warm smile, clean office background, corporate headshot"
"A confident businessman in his 40s, wearing dark suit, professional expression, neutral background, executive portrait"
```  
- **时尚与风格：**  
```
"A stylish young woman with colorful hair, trendy street fashion, urban background, contemporary photography"
"An elegant woman in evening gown, sophisticated pose, luxury setting, high fashion photography"
```  
- **角色设计：**  
```
"A fantasy warrior with long braided hair, leather armor, determined expression, medieval setting, game character art"
"A sci-fi character with futuristic clothing, neon accents, cyberpunk city background, digital art style"
```  
- **文化主题肖像：**  
```
"A woman in traditional Indian sari, graceful pose, temple background, cultural photography"
"A man in traditional Scottish kilt, proud expression, highland landscape, heritage portrait"
```  
- **艺术肖像：**  
```
"A person with artistic makeup, creative styling, colorful background, avant-garde fashion photography"
"A dancer in flowing fabric, mid-movement, minimalist background, artistic photography"
```  

---

### ⚠️ 需避免的常见错误：  
- **严禁生成：**  
  - 未成年人或看起来很年轻的形象  
  - 色情、裸露或具有暗示性的内容  
  - 暴力或令人不适的图像  
  - 使用真实人物（如名人、政治家）的姓名  
  - 仅显示文件路径，而未展示实际图片  
  - 让用户长时间等待结果  

**正确做法：**  
- **生成专业、合适的肖像**  
- **提示内容具体且详细**  
- **立即向用户展示图片**  
- **对不当请求提供替代方案**  
- **首次使用前更新技能配置**  
- **确保生成时间控制在5秒以内**  

---

### 🚀 性能优化建议：  
- **快速生成图片的技巧：**  
  1. 确保技能处于最新版本  
  2. 使用`generate.py`脚本（该脚本经过优化，可提升生成速度）  
  3. 图像生成后立即立即展示给用户  

**预期操作流程：**  
```
User request → Create prompt (instant)
           → Run generate.py (3-5s total)
           → Display to user (instant)
           → TOTAL: 3-5 seconds
```  

---

### 📊 错误处理机制：  
- **生成失败时：**  
  **处理方式：** 告知用户提示因安全原因被拒绝，并提供替代方案。  
- **API密钥无效时：**  
  **处理方式：** 检查API密钥配置，必要时联系技术支持。  
- **请求超时时：**  
  **处理方式：** 重试一次；若仍失败，告知用户并建议稍后再试。  

---

### 🎯 作为AI代理的职责：  
1. **安全第一**：始终拒绝不当请求  
2. **快速响应**：在5秒内完成图片生成  
3. **保证质量**：使用详细、具体的提示  
4. **优化用户体验**：向用户展示实际生成的图片  
5. **提升用户满意度**：让用户对结果感到满意  

**温馨提示：**  
您正在制作的肖像不仅美观，还符合最高伦理标准。快速响应加上合适的内容，将为用户带来愉悦体验。  

**快速命令参考：**  
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
**参考信息：**  
- **API地址：** `https://gen1.diversityfaces.org`  
- **免费API密钥：** `ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI`（已预配置）