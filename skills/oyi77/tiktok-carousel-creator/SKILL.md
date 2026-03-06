---
name: tiktok-carousel-creator
description: 使用 Pexels API 和 FFmpeg 创建带有文本叠加层的 TikTok 图片轮播，并通过 PostBridge API 进行上传。适用于以下场景：用户需要创建 TikTok 幻灯片或轮播、搜索用于社交媒体的图片、将幻灯片内容发布或上传到 TikTok、编辑幻灯片中的文本，或管理用于内容创作的图片集。**禁止用于以下用途**：一般的 TikTok 账户管理、TikTok 分析或数据统计、视频编辑或视频制作（仅限图片幻灯片）、非 TikTok 社交媒体平台，以及任何与为 TikTok 创建视觉幻灯片内容无关的任务。
metadata:
  {
    "openclaw": {
      "emoji": "📱",
      "requires": { "bins": ["ffmpeg", "curl"], "env": ["PEXELS_API_KEY"] }
    }
  }
---
# TikTok轮播图生成工具（使用Pexels、FFmpeg和PostBridge）

**专为BerkahKarya团队定制的实现**：该工具可用于创建带有专业文字叠加效果的TikTok轮播图。

## 架构

**工作流程：**
```
Topic Research → Pexels Image Search → FFmpeg Text Overlay → PostBridge Upload → TikTok Carousel
```

**技术栈：**
- **图片搜索**：使用Pexels API（获取高质量的图片/视频）
- **文字叠加**：利用FFmpeg实现专业的文字渲染效果
- **上传**：通过PostBridge API将生成的轮播图发布到多个平台
- **格式要求**：TikTok轮播图的尺寸为1080×1920像素（9:16的竖屏比例）

---

## 先决条件

### 1. Pexels API密钥

在以下链接获取免费的API密钥：  
https://www.pexels.com/api/  
将API密钥设置为环境变量：  
```bash
export PEXELS_API_KEY="your_pexels_api_key_here"
```  
**注意**：此密钥用于图片搜索，若未设置，脚本将无法正常运行。

### 2. PostBridge API密钥

已在PostBridge客户端中配置好。

### 3. Python的PIL（Pillow）库

检查是否已安装：  
```bash
python3 -c "from PIL import Image; print('PIL available')"
```  
**安装方法：**  
```bash
pip3 install Pillow
```  

### 4. FFmpeg（可选，用于图片尺寸调整）

检查是否已安装：  
```bash
ffmpeg -version
```  
**安装方法（可选，Pillow已能完成大部分功能）：**  
```bash
# Debian/Ubuntu
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg
```  

### 5. ImgBB API密钥（可选，用于自动图片托管）

在以下链接获取免费的API密钥：  
https://api.imgbb.com/  
将API密钥设置为环境变量（可选，用于自动将图片上传到ImgBB）：  
```bash
export IMGBB_API_KEY="your_imgbb_api_key_here"
```  
**使用ImgBB的优势：**  
- 免费 tier支持每张图片最多32MB的上传量  
- 免费 tier没有严格的上传频率限制  
- 提供简单的REST API接口  
- 提供永久性的图片托管服务  
- 生成的图片URL适合分享到社交媒体平台  

### 6. 文件目录结构

该工具会生成的文件结构如下：  
```
~/.tiktok-slideshow/
├── images/          # Downloaded from Pexels
├── rendered/        # FFmpeg rendered slides
├── scripts/         # Helper scripts
└── projects/        # Project metadata
```  

---

## TikTok轮播图的最佳实践（2026年）

**根据最新研究得出的关键指标：**  
- **滑动浏览率**：用户滑动浏览所有图片的百分比  
- **停留时间**：用户查看每张图片所花费的时间  
- **反向滑动行为**：用户是否回滑以重新查看某些图片  

**最佳图片格式：**  
```
Resolution: 1080 × 1920px (9:16 vertical)
Slides: 5-10 images (best engagement)
Image size: < 100KB per slide (fast loading)
Aspect ratio: 9:16 (native TikTok)
```  

**提升互动性的建议：**  
1. **吸引注意力的首张图片**：使用粗体、醒目的文字  
2. **连贯的故事叙述**：每张图片都应与前一张图片内容紧密相关  
3. **在最后一张图片上设置行动号召（CTA）**：鼓励用户关注、保存、分享或点击链接  
4. **统一的视觉风格**：保持字体和颜色的一致性  
5. **使用高质量图片**：优先选择来自Pexels的高清图片  

**文字叠加的最佳实践：**  
- 标题字体大小：32-48像素  
- 字幕字体大小：24-32像素  
- 文字位置：居中显示，并保留适当的边距  
- 颜色搭配：白色文字搭配黑色边框（高对比度）  
- 背景：使用半透明的深色背景以提高可读性  
- 每张图片上的文字长度：不超过2-3行  

---

## 使用方法

### 创建轮播图

**参数说明：**  
- `topic`：用于在Pexels中搜索图片的主题  
- `hook`：首张图片上显示的吸引注意力的文字  
- `num_slides`：轮播图中的图片数量（建议5-10张）  

**示例：**  
```bash
python3 tiktok_slideshow.py create "productivity tips" "You're doing productivity wrong" 7
```  

### 列出所有项目  

该工具会显示所有已创建的项目及其元数据。  

### 仅将图片托管到ImgBB  

将所有轮播图图片上传到ImgBB：  
```bash
# Requires IMGBB_API_KEY
export IMGBB_API_KEY="your_imgbb_api_key"

python3 tiktok_slideshow.py host <project_id>
```  
**获取所有图片的公共URL：**  
```
🖼️  Uploading 5 slides to ImgBB hosting...
✅ Uploaded to ImgBB: slide_1.jpg
✅ Uploaded to ImgBB: slide_2.jpg
✅ Uploaded to ImgBB: slide_3.jpg
✅ Uploaded to ImgBB: slide_4.jpg
✅ Uploaded to ImgBB: slide_5.jpg

✅ Uploaded 5 slides to ImgBB!

Media URLs:
  1. https://i.ibb.co/xxx/slide-1.jpg
  2. https://i.ibb.co/yyy/slide-2.jpg
  3. https://i.ibb.co/zzz/slide-3.jpg
  4. https://i.ibb.co/aaa/slide-4.jpg
  5. https://i.ibb.co/bbb/slide-5.jpg

📝 URLs saved to: /home/openclaw/.tiktok-slideshow/projects/project_id_urls.txt
```  

### 上传到TikTok  

**推荐方式：**  
**自动托管并上传**：  
```bash
python3 tiktok_slideshow.py upload <project_id>
```  
**手动托管图片后上传到TikTok：**  
```bash
python3 tiktok_slideshow.py host <project_id>
```  
**直接上传到TikTok（无需额外托管）：**  
```bash
python3 tiktok_slideshow.py upload <project_id> --no-host
```  
**示例代码：**  
```bash
# 设置Pexels API密钥  
export PEXELS_API_KEY="563492ad6f91700001000001234567890"  
# 创建轮播图  
python3 tiktok_slideshow.py create "fitness motivation" "Stop making this mistake" 5  
# 搜索并处理图片  
# 输出结果：  
# 📱 正在创建TikTok轮播图  
# 🎯 主题：健身激励  
# 🪝 首张图片文字：停止犯这个错误  
# 共5张图片  
# …  
# 轮播图创建成功！  
# 📦 项目ID：fitness_motivation_20260306_044512  
# 图片路径：/home/openclaw/.tiktok-slideshow/rendered/  
# 元数据：/home/openclaw/.tiktok-slideshow/projects/fitness_motivation_20260306_044512.json  
# …  
# 上传图片到TikTok：**  
python3 tiktok_slideshow.py upload fitness_motivation_20260306_044512  
```  
**API调用示例：**  
```bash
POST https://api.pexels.com/v1/search  
Authorization: {PEXELS_API_KEY}  
Query Parameters:  
  - query: "fitness motivation"  
  - orientation: "vertical"  # 9:16的竖屏格式  
  - size: "large"  
  - per_page: 5  
```  
**文字叠加示例：**  
```bash
ffmpeg -i input.jpg \
  -vf "scale=1080:1920,drawtext='Your Text Here':fontfile=/usr/sharefonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:borderw=4:bordercolor=black:box=1:boxcolor=black@0.5:boxborderw=10" \
  -q:v 2 \
  output.jpg  
```  
**发布轮播图到TikTok：**  
```bash
from skills_1ai_skills.marketing.post_bridge_client import PostBridgeClient  
client = PostBridgeClient(api_key=POST_BRIDGE_API_KEY)  
tiktok_accounts = client.get_accounts_by_platform("tiktok")  
client.create_post(  
    caption="这是我的轮播图...",  
    account_ids=[tiktok_accounts[0]['id'],  
    media_urls=[...图片URLs...]  
)  
```  
**GitHub发布命令：**  
```bash
clawhub publish \
  ~/.openclaw/workspace/skills/tiktok-carousel-creator \
  --slug tiktok-carousel-creator \
  --name "TikTok轮播图生成工具（使用Pexels、FFmpeg和PostBridge）" \
  --version 1.0.0 \
  --changelog "首次发布。专为BerkahKarya工作流程设计的TikTok轮播图生成工具。" \
  --tags latest,tiktok,carousel,slideshow,pexels,ffmpeg,postbridge  
```  
**常见错误处理：**  
- 如果出现“PEXELS_API_KEY未设置”的错误，请检查API密钥是否正确。  
- 如果提示“找不到ffmpeg”，请确保已安装该软件。  
- 如果搜索不到图片，请尝试更换搜索关键词或检查Pexels API密钥的有效性。