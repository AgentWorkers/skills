---
description: **Anima Avatar** – 一个交互式视频生成引擎。该引擎能够生成 16:9 比例的视频，其中包含动态的角色精灵（Shutiao）、同步的音频（Fish Audio）以及文本叠加效果。
---

# Anima Avatar（Anima项目）

该项目能够生成高质量的互动视频，让Shutiao根据文本内容使用恰当的表情、手势和声音进行演绎。

## 功能特点
- **真实语音**：采用Fish Audio API实现逼真的语音合成。
- **动态精灵图**：根据情感标签，从包含30多种精灵图（快乐、愤怒、害羞、思考、动作）的库中自动选择合适的精灵图。
- **智能导演**：负责视频的并行渲染、音频同步和视频合成（使用FFmpeg工具）。
- **专业交付**：将生成的视频作为原生流媒体上传到Feishu平台，实现直接播放（时长准确无误）。

## 项目结构
- `src/director.js`：核心引擎，负责生成帧图像（使用sharp和SVG格式）、音频（Fish Audio处理）以及视频（FFmpeg生成）。
- `src/send_video_pro.js`：负责视频的上传和交付，包括转码、时长计算以及与Feishu平台的交互。
- `src/batch_generator.js`：批量生成精灵图的工具，利用Gemini图像生成技术生成不同的精灵图变体。
- `assets/sprites/`：精灵图库，包含1920x1080像素的PNG格式图片。
- `assets/production_plan.csv`：记录所有精灵图信息的文件。
- `assets/manifest.json`：精灵图的元数据文件。
- `output/`：存放生成后的视频文件。

**重要提示**：精灵图不包含在发布包中

**ClawHub仅负责分发文本文件**。发布的软件包中不包含精灵图的PNG图片。

安装完成后，请按照以下步骤**依次**准备所需的精灵图，以便首次使用。

所有图像生成过程都使用**Gemini API（Nano Banana）**作为AI图像生成工具。该工具通过“参考图像 + 文本描述”的方式工作：您提供一张参考图像和文字描述，它便会生成一张包含所需变化的新图像。这样就可以生成基础精灵图（角色与背景的融合图像）及其各种表情变体。

### 第1步：准备角色图像
您需要一张**独立的角色插画图片**（建议使用透明背景的PNG格式）。
- 这张图片将决定所有精灵图的外观。
- 分辨率至少为1920x1080像素，全身图像效果最佳。
- 例如：一张具有透明背景的全身动漫角色PNG图片。
- 将图片保存在可访问的位置（例如：`avatars/my_character.png`）。

### 第2步：准备背景图像
您需要为角色准备一个**背景场景图片**。
- 这张图片会在每个视频帧中显示在角色身后。
- 分辨率至少为1920x1080像素。
- 例如：樱花花园、教室或城市街道的背景图片。
- 将图片保存在`assets/backgrounds/`文件夹中（例如：`assets/backgrounds/cherry_blossom_bg.png`）。

### 第3步：将角色与背景融合成基础精灵图
此步骤使用**Gemini（Nano Banana）**图像生成工具将角色图像融合到背景中。AI会自动处理光照、阴影和混合效果，生成自然的外观。
**操作方法**：
**方法A：直接使用Gemini**（推荐）：
使用任何支持Gemini的图像生成工具（如Nano Banana、Google AI Studio或Gemini API），输入背景图片和角色图片，并输入描述（例如：“将角色自然地放置在这个背景场景中，全身可见，面带微笑”）。
- 保存生成的图片为`assets/sprites/shutiao_base.png`。

**方法B：使用内置的合成脚本（简单叠加）**：
如果您只需要简单的图像叠加效果（不使用AI混合），可以运行`src/compose_base.js`：
1. 修改`src/compose_base.js`文件，将`BG_PATH`和`AVATAR_PATH`设置为相应的文件路径。
2. 运行`node src/compose_base.js`。
- 生成结果保存为`assets/sprites/shutiao_base.png`。
**注意**：方法B仅生成简单的图像叠加效果，而方法A（使用Gemini）能生成更自然的效果。

### 第4步：规划精灵图变体
现在您已经有了基础精灵图，接下来需要规划所需的表情和姿势变体。
打开`assets/production_plan.csv`文件并进行自定义：

**列说明**：
- **Emotion**：视频生成工具用于选择精灵图的类别（快乐、愤怒、害羞、思考、悲伤、动作、基础）。
- **Filename**：输出文件的名称，格式为`shutiao_<emotion>_<variant>.png`。
- **Prompt**：描述该变体与基础版本的差异。生成工具会使用基础图像和该提示，仅改变角色的表情或姿势。
- **Status**：`Pending`表示待生成；`Done`表示已生成，可以跳过。

默认的CSV文件包含25个条目。您可以自由添加、删除或修改条目。

### 第5步：生成精灵图变体
此步骤再次使用**Gemini（Nano Banana）**图像生成工具。对于所有标记为`Pending`的条目，批量生成工具会将基础精灵图和描述发送给Gemini API，要求其仅改变角色的表情或姿势，其他部分保持不变。
1. 在`skills/anima/.env`文件中设置Gemini API密钥：
2. 确保步骤3中生成的`assets/sprites/shutiao_base.png`（或`shutiao_base_1k.png`）文件存在。
3. 运行`src/batch_generator.js`：

**生成过程**：
- 读取`production_plan.csv`文件。
- 找到所有标记为`Pending`的条目。
- 对每个条目，将基础精灵图和描述发送给Gemini API。
- 将生成的图片保存为PNG格式的文件，放入`assets/sprites/`文件夹。
- 更新CSV文件中的状态为`Done`。
- 每次生成之间等待10秒（遵循API的速率限制）。

### 第6步：验证结果
检查`assets/sprites/`文件夹中是否包含`production_plan.csv`文件中的所有精灵图文件。

然后进行一次快速测试：
检查`temp/frame_0.png`文件，确认角色图像和文字显示正确。

如果运行时某个精灵图缺失，系统会使用白色背景并在控制台显示警告信息。

## 设置与要求

### 1. 系统依赖
- **ffmpeg**（视频处理必备）：
  - macOS：`brew install ffmpeg`
  - Linux：`sudo apt install ffmpeg`
  - Windows：下载并安装FFmpeg，并将其添加到系统路径中。

### 2. Node.js依赖
在`skills`文件夹内安装相关依赖：
（具体依赖项已在代码中列出）

**注意**：唯一的原生依赖库是`sharp`，它通过N-API为所有主要平台提供了预编译的二进制文件。即使Node.js版本更新，也无需重新编译。

### 3. 外部服务（需要API密钥）
该项目依赖两个外部服务，您需要提供自己的API密钥：

#### Fish Audio（TTS - 文本转语音）
- 功能：将文本转换为逼真的语音。
- 使用位置：`src/director.js`中的`generateAudio()`函数。
- 获取密钥方式：https://fish.audio/dashboard/api
- 需要的环境变量：
  - `FISH_AUDIO_KEY`：您的API密钥（以`sk-...`或十六进制字符串开头）。
  - `FISH_AUDIO_REF_ID`：语音模型的引用ID。您可以使用Fish Audio提供的默认模型，也可以自定义模型。

#### Gemini API（图像生成 - 可选）
- 功能：使用Google Gemini生成精灵图变体。
- 使用位置：`src/batch_generator.js`（仅在使用新精灵图变体时需要）。
- 无需额外依赖：`batch_generator.js`会直接通过curl调用Gemini API。
- 获取密钥方式：https://aistudio.google.com/apikey
- 注意：常规视频生成不需要此API，仅用于创建新角色精灵图。

#### Feishu / Lark（视频上传服务 - 可选）
- 功能：将视频作为原生媒体消息上传到Feishu平台。
- 使用位置：`src/send_video_pro.js`。
- 需要的环境变量：
  - `FEISHU_APP_ID`：您的Feishu应用ID。
  - `FEISHU_APP_SECRET`：您的Feishu应用密钥。
- 如果仅使用`--preview`模式，则无需此API。

### 4. 环境配置
在`skills`文件夹内创建一个`.env`文件（`skills/anima/.env`）：
（具体配置内容已在代码中列出）

**重要提示**：`.env`文件优先从`skills`文件夹加载（具有最低权限）。请勿提交`.env`文件，因为它已被`.clawignore`文件排除在版本控制之外。

## 使用方法

### 生成并上传视频
（具体操作步骤已在代码中列出）

### 一键式使用（适用于代理）
（具体命令已在代码中列出）

## 脚本格式
脚本中的每个场景都是一个JSON对象：
（具体结构已在代码中列出）

**支持的表情**：`Base`、`Happy`、`Angry`、`Shy`、`Think`、`Sad`、`Action`。

## 扩展：自定义TTS服务
如果您想使用其他TTS服务（如OpenAI、ElevenLabs）：
1. 打开`src/director.js`文件。
2. 找到`generateAudio(text, filename)`函数。
3. 将Fish Audio API的调用替换为新的TTS服务的逻辑。
4. 确保该函数返回的格式为：`{ path: "/path/to/audio.wav", duration: 1.5 }`（时长以秒为单位）。

## 高级功能：添加更多精灵图变体
- 要添加新的表情或姿势，可以在`assets/production_plan.csv`中添加新的条目，并设置`Status=Pending`。
- 为每个新条目编写描述变化的提示（例如：“愤怒的表情，双臂交叉，目光移开”）。
- 运行`node src/batch_generator.js`，它只会处理标记为`Pending`的条目。
- 新生成的精灵图会自动添加到角色的表情库中。

有关完整的制作流程和设计理念，请参阅`ASSETS_PLAN.md`文件。

## 常见问题解决方法
- **时长为00:00**：确保`send_video_pro.js`函数以毫秒为单位计算时长，并将该时长传递给上传和消息数据。
- **Fish Audio出现错误（例如400）**：检查您的Ref ID是否与API密钥对应的模型匹配。
- **视频显示黑屏**：查看`ffmpeg`的转码日志，并检查`temp/frame_*.png`文件中的源图像。
- **SVG文本无法显示**：确保系统中安装了CJK字体（macOS默认已安装；Linux用户需运行`sudo apt install fonts-noto-cjk`）。
- **无音频输出**：如果`FISH_AUDIO_KEY`缺失，系统会使用macOS的`say`命令（仅提供英文语音）。