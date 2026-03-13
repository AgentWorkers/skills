---
name: wan-image-video-gen-edit
description: >
  使用Wan系列模型进行图像和视频的生成与编辑。该模型支持以下功能：  
  - **文本转图像（text2image）**  
  - **图像编辑（含提示功能）**  
  - **文本转视频（text2video）**  
  - **图像转视频（image2video）**  
  - **基于参考图像或视频的视频生成（reference(image or video)2video）**
homepage: https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["python3"],"env":["DASHSCOPE_API_KEY"]},"primaryEnv":"DASHSCOPE_API_KEY"},"author":"KrisYe"}
---
# Wan 模型

Wan 模型由阿里巴巴集团开发，是广泛应用于图像和视频生成及编辑领域的模型，在全球范围内备受推崇。该技能可以与 ModelStudio（Bailian-Alibaba Model Service Platform）上的 Wan 模型 API 进行集成。

## 从文本生成图像（text2image）
根据用户提供的文本提示生成图像
```bash
python3 {baseDir}/scripts/wan-magic.py text2image --prompt "一个女生站在楼顶的阳台上，夕阳照在她的脸上"
python3 {baseDir}/scripts/wan-magic.py text2image --prompt "一位长发女孩坐在书桌前，背对着镜头，戴着耳机。阳光透过窗户洒进房间，照亮了她和周围散落的书籍与杂物" --size 1280*1280
python3 {baseDir}/scripts/wan-magic.py text2image --prompt "女生优雅地倚在车门旁，身穿红色褶皱长裙，在复古色调的室内场景中缓慢转身看向镜头，霓虹光斑在玻璃窗上流动，轻微晃动，背景家具逐渐虚化凸显人物独白，画面带有电影胶片颗粒质感，港风朦胧光影映照出淡淡的忧伤情绪" --quantity 1
```

### 参数选项：
- `--quantity`：生成的图像数量（默认值：1，最大值：4）
- `--prompt`：用于图像生成的文本提示
- `--size`：图像分辨率（默认值：1280*1280；支持宽度在 512 到 1440 像素、高度在 512 到 1440 像素之间的分辨率，总像素数不得超过 1440*1440。常见分辨率：1280*1280、1104*1472、1472*1104、960*1696、1696*960）

## 从图像生成图像（image2image）
根据现有图像进行编辑
```bash
python3 {baseDir}/scripts/wan-magic.py image-edit --prompt "参考图1的风格和图2的背景，生成一张全新的图片" \
  --images 'https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png' \
  'https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp' \
  --size "1280*1280"
  python3 {baseDir}/scripts/wan-magic.py image-edit --prompt "参考图1的风格和图2的背景，生成一张全新的图片" \
  --images '/Users/yejianhongali/workDir/pic1.png' \
  '/Users/yejianhongali/workDir/pic2.webp' 
python3 {baseDir}/scripts/wan-magic.py image-edit --prompt "参考图1的风格和图2的背景，生成一张全新的图片" --images 'https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png' 'https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp' --quantity 1
```

### 参数选项：
- `--quantity`：编辑的图像数量（默认值：1，最大值：4）
- `--prompt`：用于图像编辑的文本提示
- `--images`：需要编辑的图像文件（至少 1 张图像，最多 4 张）。可以是图像 URL 或本地图像文件（wan-magic.py 脚本会将本地图像转换为 Base64 格式并传递给模型 API）
- `--size`：图像分辨率（默认值：1280*1280；支持宽度在 512 到 1440 像素、高度在 512 到 1440 像素之间的分辨率，总像素数不得超过 1440*1440。常见分辨率：1280*1280、1104*1472、1472*1104、960*1696、1696*960）

## 从文本生成视频（text2video）
根据用户提供的文本提示生成视频
### text2video 任务提交（task-submit）
```bash
python3 {baseDir}/scripts/wan-magic.py text2video-gen --prompt "一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说：”青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。“。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是“可爱”与“霸气”的搞笑和史诗般的融合。" --duration 10 --size "1920*1080"
```

#### 参数选项：
- `--duration`：视频的时长（秒）（默认值：5，最大值：15）
- `--prompt`：用于视频生成的文本提示
- `--size`：视频分辨率（默认值：1920*1080；支持 720p 和 1080p 分辨率。输入时需要提供具体的分辨率数值，例如：1280*720）

### 分轮获取生成的视频结果（text2video tasks-get (round-robin)）
```bash
python3 {baseDir}/scripts/wan-magic.py text2video-get --task-id “<TASK_ID_FROM_VIDEO_GEN>”
```

## 以某张图像作为第一帧生成视频（image2video）
根据某张图像生成视频
### image2video 任务提交（task-submit）
```bash
python3 {baseDir}/scripts/wan-magic.py image2video-gen --prompt "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。" --image "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png" --duration 10 --resolution "720P"
python3 {baseDir}/scripts/wan-magic.py image2video-gen --prompt "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。" --image "/Users/yejianhongali/workDir/rap.png" 
```

#### 参数选项：
- `--duration`：视频的时长（秒）（默认值：5，最大值：15）
- `--prompt`：用于视频生成的文本提示
- `--image`：作为视频第一帧的图像文件（可以是图像 URL 或本地图像文件）。wan-magic.py 脚本会将本地图像转换为 Base64 格式并传递给模型 API
- `--resolution`：视频分辨率（默认值：1080P；支持 720P 和 1080P 分辨率。输入时需要提供具体的分辨率数值）

### 分轮获取生成的视频结果（image2video tasks-get (round-robin)）
```bash
python3 {baseDir}/scripts/wan-magic.py image2video-get --task-id “<TASK_ID_FROM_VIDEO_GEN>”
```

## 从参考图像或视频生成视频（reference2video）
根据参考图像或视频生成视频
### reference2video 任务提交（task-submit）
```bash
python3 {baseDir}/scripts/wan-magic.py reference2video-gen  --prompt "character1 在海边漫步，微风吹拂头发" --reference-files "https://example.com/person.mp4"
python3 {baseDir}/scripts/wan-magic.py reference2video-gen  --prompt "character1 在咖啡厅看书" --reference-files "https://example.com/person.mp4/person.jpg" --duration 5
python3 {baseDir}/scripts/wan-magic.py reference2video-gen --prompt "Character2 坐在靠窗的椅子上，手持 character3，在 character4 旁演奏一首舒缓的美国乡村民谣。Character1 对Character2开口说道：“听起来不错”" --reference-files "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/hfugmr/wan-r2v-role1.mp4" "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4" "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png" "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png" --duration 10
python3 {baseDir}/scripts/wan-magic.py reference2video-gen --prompt "character2 坐在窗边弹吉他，character1 在旁边听。character1 说：'弹得真好听。'" --reference-files "https://example.com/listener.mp4" "https://example.com/guitarist.mp4" --shot-type "multi" --duration 10 --size "1920*1080"

```

#### 参数选项：
- `--duration`：视频的时长（秒）（默认值：5，最大值：10）
- `--prompt`：用于视频生成的文本提示。注意：使用 'character1' 表示参考文件中的第一张图像/视频，'character2' 表示第二张图像/视频。
- `--reference-files`：用于视频生成的参考图像或视频的 URL。生成的视频会参考这些图像/视频中的内容（角色、声音、场景等）。每个 URL 可以是图像或视频。参考图像数量：0 至 5 张；参考视频数量：0 至 3 张；总参考资源数量：不超过 5 个。
- `--resolution`：视频分辨率（默认值：1920*1080；支持 720P 和 1080P 分辨率，例如：720*1280、1280*720、960*960、1088*832、832*1088、1920*1080、1080*1920、1440*1440、1632*1248、1248*1632）
- `--shot-type`：视频的拍摄类型。"single" 表示连续拍摄；"multi" 表示多镜头拍摄（默认值：single）

### 分轮获取生成的视频结果（reference2video tasks-get (round-robin)**
```bash
python3 {baseDir}/scripts/wan-magic.py reference2video-get --task-id “<TASK_ID_FROM_VIDEO_GEN>”
```