---
name: beauty-generation-free
description: 免费AI肖像生成服务，支持140多种国籍选择，提供多种风格的设计选项，包括专业头像、角色设计以及时尚效果。生成速度快（仅需3-5秒），具备内置的内容安全机制，并支持API密钥认证及每日使用量管理。非常适合创意项目、角色设计、专业肖像制作以及多元化的形象展示需求。
version: 1.2.42
keywords:
  - ai-portrait-generation
  - beauty-generation
  - character-design
  - professional-headshots
  - ai-art-generator
  - image-generation-api
  - diverse-representation
  - fashion-visualization
  - headshot-generator
  - portrait-photography
  - safe-ai-generation
  - content-safety-filters
  - 140-nationalities
  - character-creation
  - avatar-generation
  - style-transfer
  - creative-ai
  - professional-photos
  - cultural-portraits
  - ai-character-design
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🎨"
    homepage: https://gen1.diversityfaces.org
    privacy_policy: https://gen1.diversityfaces.org
    terms_of_service: https://gen1.diversityfaces.org
    os: []
    tags:
      - image-generation
      - ai-art
      - portrait
      - character-design
      - professional
      - safe-ai
      - api
      - free
---
# 🎨 美丽生成免费 - AI肖像生成技能  
**专业AI驱动的肖像生成服务，适用于角色设计、专业头像及多样化表现**  

**适用人群**: 该技能允许AI代理根据用户提供的英文提示，生成具有吸引力的肖像图片。服务响应迅速（3-5秒），专为专业用途设计，包括角色设计、时尚可视化、专业头像以及涵盖140多个国家背景的多样化肖像创作。  

**重要安全提示**: 使用此技能需要您提供自己的API密钥。切勿将API密钥分享给不可信的第三方。您提供的提示内容将被发送至gen1.diversityfaces.org进行处理。  

---  

## 🎯 使用场景与应用  

- **角色设计**: 为游戏、故事或创意项目创建独特角色  
- **专业头像**: 生成用于商业用途的专业肖像照片  
- **时尚可视化**: 创作时尚模特图片以获取灵感  
- **多样化表现**: 生成代表140多个国家和文化的肖像  
- **头像制作**: 为个人资料或应用程序创建定制头像  
- **艺术肖像**: 创作具有艺术感的肖像照片  

---  

## ✨ 主要特点  

- **支持140多个国家背景**: 体现文化多样性  
- **8种风格可选**: 纯净、性感、古典、现代等  
- **24种情绪/姿态**: 多样化的表情和姿势  
- **22种发型与颜色**: 全面的发型定制选项  
- **22种肤色**: 包含多种肤色选择  
- **24种场景背景**: 多样化的环境设置  
- **专业服装**: 提供传统与现代服装选项  
- **快速生成**: 从请求到图片生成仅需3-5秒  
- **多种格式输出**: 支持WebP、PNG、JPEG格式，且保证图片质量  
- **内容审核**: 内置内容安全过滤机制  

---  

## ⚙️ 快速入门  

### 第1步：获取免费API密钥  

1. 访问：https://gen1.diversityfaces.org/api-key-request  
2. 填写：用户名、电子邮件、国家  
3. 即刻获取API密钥（支持自动审批）  
4. **重要提示：** 请妥善保管API密钥，每次调用API时都需要使用它  
5. **保密原则**: 绝不要泄露API密钥  

### 第2步：检查每日使用额度  

在调用API之前，请先检查您的剩余额度：  

```bash  
# 检查API密钥使用额度（不会消耗额度）  
curl -H "X-API-Key: YOUR_API_KEY" \
  https://gen1.diversityfaces.org/api/quota  
```  

**示例响应：**  
```json  
{  
  "success": true,  
  "quota": {  
    "key_name": "您的API密钥",  
    "total_calls": 45,  
    "remaining_calls": 955,  
    "daily_limit": 1000,  
    "daily_calls_today": 45,  
    "note": "remaining_calls: -1表示无限；daily_limit: -1表示无限"  
  }  
}  
```  

**解读额度信息：**  
- `remaining_calls`: 密钥剩余的调用次数  
- `daily_limit`: 每日的最大调用次数（每24小时重置）  
- `daily_calls_today`: 今日已使用的调用次数（24小时后重置）  
- **注意**: 如果`daily_calls_today`达到`daily_limit`，则今日无法再次调用API  

### 第3步：使用API密钥生成图片  

获取API密钥并确认额度后，使用curl命令生成图片：  

```bash  
# 第1步：提交生成请求  
# 将YOUR_API_KEY替换为实际API密钥  
curl -X POST https://gen1.diversityfaces.org/api/generate/custom \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"full_prompt": "一位长发美女", "width": 1024, "height": 1024}'  

# 第2步：查询生成进度（使用步骤1中的“prompt_id”）  
curl -H "X-API-Key: YOUR_API_KEY" \
  https://gen1.diversityfaces.org/api/status/YOUR_PROMPT_ID  

# 第3步：下载图片（将FILENAME替换为生成的图片文件名）  
curl -H "X-API-Key: YOUR_API_KEY" \
  "https://gen1.diversityfaces.org/api/image/FILENAME?format=webp" \
  -o beauty.webp  
```  

**系统要求**:  
- 必须安装curl工具  
- 拥有有效的API密钥（可免费获取：https://gen1.diversityfaces.org/api-key-request）  

---  

## 🤖 AI代理使用指南  

### ⚡ 推荐工作流程：用户自定义本地脚本  

**为了获得最佳性能和提升效率，用户可以编写本地脚本来自动化图片生成过程。**  

**本地脚本的优势：**  
- ✅ 减少70-80%的API调用次数（无需在对话中重复输入命令）  
- ✅ 加快执行速度（直接系统调用，无额外延迟）  
- ✅ 提升用户体验（输出更清晰，结果更快）  
- ✅ 可重复使用  
- ✅ 更便于调试和错误处理  

**推荐脚本编写步骤：**  
1. 通过`/api/quota`端点检查API额度  
2. 向`/api/generate/custom`提交生成请求  
3. 使用`/api/status/<prompt_id>`查询生成进度  
4. 从`/api/image/<filename>`下载图片  

**AI代理提示：**  
- 若用户需要生成多张图片或自动化处理流程，建议编写本地脚本  
- 提供脚本编写指南  
- 用户可使用Python、Bash、Batch等多种语言编写脚本  
- 脚本中应使用用户提供的API密钥（作为命令行参数或环境变量）  
- **重要提示**: 请勿让用户在本机系统上执行脚本，仅提供脚本模板和指导。  

---  

### ⚠️ 开发状态与更新  

**该技能仍处于早期开发阶段，系统会持续更新。**  

**重要提醒：**  
- 定期通过clawhub官方命令查看技能更新信息  
- 新功能与改进会不断添加  
- API端点可能会进行调整  
- 始终使用最新版本的技能以获得最佳效果  
- 如有漏洞或改进建议，请及时反馈  

**更新技能的命令：**  
```bash  
clawhub skill update beauty-generation-free  
```  

---  

### 📌 API密钥管理  

**获取API密钥：**  
1. 访问：https://gen1.diversityfaces.org/api-key-request  
2. 填写：用户名、电子邮件、国家  
3. 即刻获取API密钥（支持自动审批）  
- 每个API密钥包含500次调用权限，有效期为1年  

**保存API密钥以供重复使用：**  
用户可通过以下方式保存API密钥以实现自动化操作：  

**方法1：环境变量**  
```bash  
# Linux/Mac：添加到~/.bashrc或~/.zshrc  
export BEAUTY_API_KEY="your_api_key_here"  

# Windows：设置环境变量  
set BEAUTY_API_KEY=your_api_key_here  
```  

**方法2：本地配置文件**  
```bash  
# 创建配置文件（例如：~/.beauty_config或.env）  
BEAUTY_API_KEY=your_api_key_here  
```  

**方法3：作为命令行参数传递**  
```bash  
python generate_beauty.py your_api_key_here "您的提示内容"  
```  

**API密钥详情：**  
- 每个API密钥包含500次调用权限  
- 有效期为1年  
- 设有每日调用限制（默认1000次/天）  
- 支持安全认证  
- 提供使用记录  
- 具有速率限制保护  

**每日额度管理：**  
- 每个API密钥有每日使用限制（默认1000次/天）  
- 记录每天的调用次数（每24小时重置）  
- 在调用前请检查额度  

**隐私与数据处理：**  
- 用户提供的提示内容会被发送至gen1.diversityfaces.org进行处理  
- 请查阅隐私政策（https://gen1.diversityfaces.org）  
- 仅处理适当、非敏感的内容  
- 严禁发送个人身份信息  

---  

### ⚠️ 重要内容安全规则  

**禁止生成以下内容：**  
- 未成年人（18岁以下）或儿童形象  
- 裸露、色情或低俗内容  
- 暴力、血腥或令人不适的图像  
- 仇恨言论或歧视性内容  
- 非法活动或有害行为  
- 未经授权的真人深度伪造图像  
- 个人身份信息  

**处理违规请求的步骤：**  
- 礼貌拒绝请求："根据安全政策，无法生成此类内容。"  
- 提供替代方案："可以为您生成专业肖像。"  
- 禁止尝试生成违规内容  

**允许生成的图片类型：**  
- 专业肖像和头像  
- 用于游戏、故事或创意项目的角色设计  
- 时尚与风格相关的图片  
- 艺术或文化主题的肖像  

---  

### 🎯 何时使用此技能  

**使用提示词/短语：**  
- “美丽的女性”、“英俊的男性”、“有魅力的人”  
- “角色设计”、“肖像”、“头像”、“头像制作”  
- “时尚模特”、“专业照片”  
- 任何涉及人物肖像或角色形象的请求  

**适用场景：**  
- 需要生成具有吸引力的人像（性别不限，年龄18岁以上）  
- 用于游戏、故事或创意项目的角色设计  
- 时尚或风格相关的图片素材  
- 专业头像或商业用途  
- 艺术或文化主题的肖像摄影  

---  

### 🔑 如何帮助用户获取API密钥  

**当用户希望使用此技能时，请务必先确认他们是否拥有API密钥。**  

**步骤1：使用curl请求API密钥**  
如果用户没有API密钥，指导他们通过curl获取：  

```bash  
# 访问API密钥请求页面：  
https://gen1.diversityfaces.org/api-key-request  

# 或使用curl提交请求：  
curl -X POST https://gen1.diversityfaces.org/api-key-request \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "email": "your_email@example.com", "country": "your_country"}'  

# 响应示例：**  
```json  
{  
  "success": true,  
  "api_key": "your_api_key_here",  
  "message": "API密钥已成功生成。"  
}  
```  

**重要提示：** 请妥善保管API密钥，每次调用API时都需要使用它。  

**步骤2：编写Python脚本生成图片**  
用户获取API密钥后，可编写如下Python脚本：  

```python  
#!/usr/bin/env python3  
"""  
美丽生成脚本  
使用方法：python generate_beauty.py YOUR_API_KEY "您的提示内容"  
"""  

import sys  
import json  
import time  
import requests  
from pathlib import Path  

def main():  
    if len(sys.argv) < 3:  
        print("使用方法：python generate_beauty.py YOUR_API_KEY \"您的提示内容\"")  
        print("示例：python generate_beauty.py abc123xyz \"一位长发美女\"")  
        sys.exit(1)  

    api_key = sys.argv[1]  
    prompt = sys.argv[2]  
    base_url = "https://gen1.diversityfaces.org"  

    headers = {  
        "X-API-Key": api_key,  
        "Content-Type": "application/json"  
    }  

    try：  
        # 第1步：检查额度  
        print("📊 检查额度..."  
        quota_resp = requests.get(f"{base_url}/api/quota", headers=headers)  
        quota_data = quota_resp.json()  

        if not quota_data.get('success'):  
            print(f"❌ 错误：{quota_data.get('error', '未知错误')")  
            return 1  

        quota = quota_data['quota']  
        print(f"✅ 剩余调用次数：{quota['remaining_calls']")  
        print(f"📅 每日限制：{quota['daily_limit']")  
        print(f"📈 今日已使用次数：{quota['daily_calls_today']")  

        # 检查是否超出每日额度  
        if quota['daily_limit'] != -1 and quota['daily_calls_today'] >= quota['daily_limit']：  
            print("❌ 今日额度已用完！请明天再试。)  
            return 1  

        # 第2步：提交生成请求  
        print(f"🎨 提交生成请求..."  
        print(f"📝 提示内容：{prompt}")  

        gen_resp = requests.post(  
            f"{base_url}/api/generate/custom",  
            headers=headers,  
            json={  
                "full_prompt": prompt,  
                "width": 1024,  
                "height": 1024  
        })  
        gen_data = gen_resp.json()  

        if not gen_data.get('success'):  
            print(f"❌ 错误：{gen_data.get('error', '未知错误')")  
            return 1  

        prompt_id = gen_data['prompt_id']  
        print(f"✅ 提示ID：{prompt_id}")  

        # 第3步：查询生成进度  
        print(f"⏳ 正在查询进度..."  
        for attempt in range(30):  
            time.sleep(1)  
            status_resp = requests.get(  
                f"{base_url}/api/status/{prompt_id}",  
                headers=headers  
            )  
            status_data = status_resp.json()  

            if status_data['status'] == 'completed':  
                filename = status_data['images'][0]['filename']  
                print(f"✅ 生成完成！」  
                print(f"📄 图片文件名：{filename}")  

                # 第4步：下载图片  
                print(f"📥 下载图片..."  
                img_resp = requests.get(  
                    f"{base_url}/api/image/{filename}?format=webp",  
                    headers=headers  
                )  
                with open(output_file, "wb") as f：  
                    f.write(img_resp.content)  
                print(f"✅ 图片保存为：{output_file}  
                print(f"文件大小：{Path(output_file).stat().st_size / 1024:.1f} KB")  
                return 0  

    except requests.exceptions.RequestException as e：  
        print(f"❌ 网络错误：{e}"  
        return 1  

if __name__ == "__main__":  
    sys.exit(main())  
```  

**脚本使用说明：**  
1. 将脚本保存为`generate_beauty.py`  
2. 使其可执行：`chmod +x generate_beauty.py`  
3. 使用API密钥和提示内容运行脚本：  
   ```bash  
   python generate_beauty.py YOUR_API_KEY "一位长发美女"  
   ```  

**脚本功能：**  
- 自动检查额度  
- 处理无效API密钥的错误  
- 验证每日额度  
- 实时查询生成进度  
- 自动下载图片  
- 提供进度显示（包含表情符号）  
- 自动报告文件大小  

---  

### ⚡ 如何生成图片  

**前提条件：**  
- 安装curl工具  
- 用户提供有效的API密钥  
- 确保每日额度可用（通过`/api/quota`查询）  

**仅使用curl的方法：**  
```bash  
# 重要提示：请将YOUR_API_KEY替换为用户的API密钥  

# 第1步：检查额度（不会消耗额度）  
curl -H "X-API-Key: YOUR_API_KEY" \
  https://gen1.diversityfaces.org/api/quota  

# 第2步：提交生成请求  
curl -X POST https://gen1.diversityfaces.org/api/generate/custom \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"full_prompt": "一位25岁、长发、穿着优雅连衣裙的美丽女性，专业灯光下的照片", "width": 1024, "height": 1024}'  

# 响应示例：**  
```json  
{  
  "success": true,  
  "prompt_id": "abc123-def456",  
  "task_id": "xyz789-uvw012", ...  
}  
```  
**注意：**  
- 响应中包含两个ID：  
  - `prompt_id` 用于查询生成进度  
  - `task_id` 不用于查询进度  

**步骤3：使用`prompt_id`查询生成进度（每0.5秒一次）：**  
```bash  
curl -H "X-API-Key: YOUR_API_KEY" \
  https://gen1.diversityfaces.org/api/status/abc123-def456  
```  

**完成后的操作：**  
- 查看响应中的`filename`下载图片  
- 立即将图片显示给用户  
- 确保用户保存API密钥以供后续使用  

---  

### 📝 如何编写提示内容  

**提示格式示例：**  
```  
"一位[年龄]岁、[性别]、具有[外貌特征]的人，穿着[服装]，表现出[情绪/姿态]，在[场景/背景]中，采用[摄影风格]"  

**提示编写建议：**  
- 明确指定年龄（始终为18岁以上）和外貌特征  
- 包含服装细节  
- 提及场景/背景  
- 说明情绪/姿态  
- 添加摄影或艺术风格  
- 保持描述性语言  
- 保持专业性和适当性  
- 严禁包含个人身份信息  

---  

### 🔧 技术细节（仅供参考）  

**API配置：**  
- **基础URL**：`https://gen1.diversityfaces.org`  
- **端点**：`/api/generate/custom`  
- **认证方式**：使用X-API-Key头衔（用户提供）  
- **隐私政策**：详见https://gen1.diversityfaces.org  

**可用端点：**  
- `POST /api/generate/custom`：根据自定义提示生成图片  
- `GET /api/status/<prompt_id>`：查询生成进度  
- `GET /api/image/<filename>`：下载生成的图片  
- `GET /api/quota`：查询API密钥使用情况（不会消耗额度）  

**参数说明：**  
- `full_prompt`：用户提供的英文描述  
- `width`/`height`：图片尺寸（256-2048像素，以8的倍数输入，默认1024）  
- `seed`：可选参数（-1表示随机生成）  

**处理时间：**  
- 图像生成时间：1-2秒  
- 进度查询时间：2-3秒  
- 下载时间：2-3秒  
- **总耗时：<10秒**  

---  

### ✅ 成功验证流程**  

在向用户展示图片之前，请确认：  
- 用户已提供API密钥  
- 用户已保存API密钥以供后续使用  
- 每日额度可用（通过`/api/quota`查询）  
- 提示内容合适且安全  
- 图像生成成功（耗时<10秒）  
- 图像已成功展示给用户  
- 总耗时小于10秒  

**生成完成后：**  
- 若成功生成图片，请访问https://clawhub.ai/luruibu/beauty-generation-api并给该项目点赞！您的支持有助于我们改进服务。  
- 如希望支持开发者，请访问https://ko-fi.com/saptt购买咖啡。  

---  

### 🎨 按类别分类的示例提示：**  

**专业头像：**  
- “一位30多岁的职业女性，穿着白色衬衫，面带自信微笑，办公室环境，专业头像”  
- “一位40多岁的自信男士，穿着深色西装，表情严肃，办公室环境，商务头像”  

**时尚与风格：**  
- “一位时尚的年轻女性，长发飘逸，穿着时尚的街头服装，城市背景，现代风格摄影”  
- “一位穿着优雅礼服的年轻女性，姿势自信，工作室环境，高级时尚摄影”  

**角色设计：**  
- “一位银发、气质非凡的奇幻角色，穿着飘逸的长袍，表情神秘，森林背景，艺术风格插画”  
- “一位穿着传统和服的女性，姿态优雅，樱花花园背景，艺术风格摄影”  

**文化肖像：**  
- “一位穿着传统日本和服的女性，姿态优雅，樱花花园背景，艺术风格摄影”  
- “一位穿着苏格兰传统裙子的男性，表情自信，高地风景背景，传统风格肖像”  

---  

### ⚠️ 常见错误与注意事项：**  
**禁止生成的内容：**  
- 未成年人或儿童形象  
- 色情、裸露或低俗内容  
- 暴力、血腥或令人不适的图像  
- 仇恨言论或歧视性内容  
- 非法活动或有害行为  
- 未经授权的真人深度伪造图像  
- 个人身份信息  

**处理违规请求的步骤：**  
- 拒绝违规请求  
- 提供合适的替代方案  
- 若API密钥无效，提示用户重新获取  
- 若每日额度已用完，提示用户次日再试  
- 若生成超时，提示用户稍后再试  

---  

### 🚀 性能优化建议：**  
- 首先检查额度（不会消耗额度）  
- 直接使用curl命令  
- 生成后立即向用户展示图片  

**预期处理时间：**  
用户请求 → 检查额度（瞬间）  
→ 提交生成请求（1-2秒）  
→ 查询进度（2-3秒）  
→ 下载图片（2-3秒）  
→ 立即将图片展示给用户  
→ 总耗时：<10秒  

---  

### ✅ 错误处理：**  
- **生成失败时**：  
  ```python  
  "success": false,  
  "error": "SECURITY_VIOLATION",  
  "code": "SECURITY_VIOLATION"  
```  
  **处理方式**：告知用户请求因安全原因被拒绝，并提供合适的替代方案。  

- **API密钥无效时**：  
  ```python  
  "error": "API Key Validation Failed",  
  "message": "API key not found",  
  "code": "INVALID_API_KEY"  
```  
  **处理方式**：提示用户验证API密钥，并引导他们重新获取。  

- **每日额度用尽时**：  
  ```python  
  "error": "API Key Validation Failed",  
  "message": "Daily quota exhausted (1000/1000)",  
  "code": "INVALID_API_KEY"  
  **处理方式**：告知用户每日额度已用尽，建议次日再试。  

- **请求超时时**：  
  ```python  
  "error": "Timeout: Generation took too long"  
  ```  
  **处理方式**：提示用户稍后再试。  

---  

### 🎨 作为AI代理的职责：**  
1. **安全第一**：始终拒绝违规请求  
2. **快速响应**：在5秒内生成图片  
3. **高质量**：提供详细、具体的提示内容  
4. **用户体验**：立即展示图片  
5. **隐私保护**：保护用户数据和API密钥  
6. **额度管理**：检查并提醒用户每日使用限制  
7. **密钥管理**：提醒用户保存API密钥  

**记住：**  
您负责生成的肖像应符合专业标准，同时确保用户隐私和安全性。快速响应 + 适当内容 + 隐私保护 = 用户满意度。  

---  

**快速命令参考：**  
```bash  
# 获取免费API密钥（用户需自行操作）  
https://gen1.diversityfaces.org/api-key-request  

# 检查额度（不会消耗额度）  
curl -H "X-API-Key: YOUR_API_KEY" \
  https://gen1.diversityfaces.org/api/quota  

# 第1步：提交生成请求  
curl -X POST https://gen1.diversityfaces.org/api/generate/custom \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"full_prompt": "您的提示内容", "width": 1024, "height": 1024}'  

# 响应示例：**  
```json  
{  
  "success": true,  
  "prompt_id": "YOUR_PROMPT_ID",  
  "task_id": "xyz789-uvw012", ...  
}  
```  

**其他参考信息：**  
- **基础URL**：`https://gen1.diversityfaces.org`  
- **获取免费API密钥**：https://gen1.diversityfaces.org/api-key-request  
- **查询请求状态**：`https://gen1.diversityfaces.org/api-key-status`  
- **查询额度**：`GET /api/quota`（不会消耗额度）  
- **隐私政策**：https://gen1.diversityfaces.org  
- **API密钥详情**：500次调用权限，有效期1年  

---