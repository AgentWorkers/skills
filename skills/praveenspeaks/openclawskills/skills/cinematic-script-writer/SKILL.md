# 电影剧本编写工具

该工具专为 AI 视频生成提供专业的电影剧本编写服务，确保角色表现的一致性，同时具备丰富的电影摄影知识，并支持与 Google Drive 的存储集成。

## 说明

此技能可帮助您为动画/喜剧视频编写完整的电影剧本，包括以下功能：

- **故事生成**：创建故事背景、角色设定并生成故事创意。
- **电影剧本编写**：编写包含镜头角度、拍摄方式、灯光效果和对话的完整剧本。
- **角色一致性**：确保所有镜头中的角色外观一致。
- **语音一致性**：保持每个角色的说话风格统一。
- **环境一致性**：确保场景中的建筑、服装和道具符合历史背景。
- **时代错误检测**：防止在历史场景中出现现代元素。
- **Google Drive 存储**：自动将所有内容保存到有序的文件夹中。
- **YouTube 元数据生成**：自动生成视频标题、描述和标签。

## 特点

### 电影摄影数据库（175+ 技巧）
- **20 多种镜头角度**（平视、低角度、荷兰角、鸟瞰、第一人称视角）
- **20 多种镜头移动方式**（移动摄影车、云台、摇臂、轨道对焦、蛇形拍摄）
- **25 多种镜头类型**（超广角、特写、插入镜头、剪影镜头）
- **30 多种灯光技巧**（三点照明法、明暗对比、霓虹灯光效果）
- **20 多种构图规则**（三分法则、黄金分割、引导线）
- **20 多种色彩分级风格**（蓝绿色调、黑色调、复古风格、荧光效果）
- **15 多种视觉风格**（皮克斯风格、动漫风格、电影黑色风格、印度微型画风格）
- **15 多种类型电影摄影指南**

### 一致性系统
- **角色参考资料**：包含角色的视觉细节。
- **语音资料**：包含角色的音高、词汇和常用语。
- **环境风格指南**：确保场景符合历史时代特征。
- **提示生成器**：确保提示内容的一致性。
- **时代错误检测**：检查脚本中是否存在时代错误。

### 存储集成
- **Google Drive OAuth 连接**：支持与 Google Drive 的数据同步。
- **本地存储**：支持将文件下载到本地。
- **有序的文件夹结构**：确保文件存储整齐有序。
- **项目导出**：支持导出整个项目文件。

## 使用示例

### 基本故事创作

```javascript
// Create a story context
const context = await skill.createContext(
  "Kutil's Adventure",
  "A cursed rakshasa's journey",
  [{
    name: "Kutil",
    description: "Cute purple rakshasa",
    personality: "Mischievous, kind",
    appearance: "Purple fur, golden eyes",
    role: "protagonist"
  }],
  "Ramayana Era",
  "Ancient India",
  "Lanka",
  "short",
  "comedy",
  "All ages",
  "Pixar 3D style"
);

// Generate story ideas
const ideas = await skill.generateStoryIdeas(context.id, 3);

// Create script
const script = await skill.createCinematicScript(
  context.id,
  ideas[0].id,
  ideas[0]
);
```

### 使用电影摄影技巧

```javascript
// Get camera techniques
const angles = skill.getAllCameraAngles();
const lighting = skill.suggestLighting('interior-day', 'comedy');
const grading = skill.suggestColorGrading('comedy');

// Get complete setup
const setup = skill.getRecommendedCameraSetup(
  'dialogue-intimate',
  'emotional',
  'intermediate'
);
```

### 确保角色一致性

```javascript
// Create character reference
const ref = skill.createCharacterReference(
  "char-123",
  "Kutil",
  "Purple fur, small horns, golden eyes",
  "Ramayana Era",
  "pixar-3d"
);

// Generate consistent prompts
const prompt = skill.generateCharacterConsistencyPrompt("char-123");

// Validate for anachronisms
const result = skill.validatePrompt(
  "Kutil wearing sunglasses",
  ["char-123"],
  context.id
);
// Returns error: glasses don't belong in Ramayana Era
```

### 保存到 Google Drive

```javascript
// Connect Google Drive
const auth = await skill.connectGoogleDrive();
// Visit auth.authUrl, authorize, paste code
await skill.connectGoogleDrive(userAuthCode);

// Save everything
const result = await skill.saveScriptToStorage(
  "Story Title",
  context.id,
  script.id
);
console.log(result.shareLink);
```

## 工具

### 上下文管理
- `createContext()`：创建故事背景。
- `listContexts()`：列出所有可用的故事背景。
- `getContext()`：获取特定故事背景。
- `deleteContext()`：删除指定的故事背景。

### 故事生成
- `generateStoryIdeas()`：生成故事创意。
- `createCinematicScript()`：编写完整的电影剧本。
- `generateYouTubeMetadata()`：生成适用于 YouTube 的元数据。

### 一致性管理
- `createCharacterReference()`：创建角色视觉参考资料。
- `createVoiceProfile()`：创建角色的语音资料。
- `createEnvironmentStyleGuide()`：生成符合时代特征的环境风格指南。
- `buildConsistentPrompts()`：生成一致性的提示内容。
- `validatePrompt()`：检查提示内容是否存在时代错误。

### 电影摄影相关功能
- `getAllCameraAngles()`：获取所有可用的镜头角度。
- `getAllCameraMovements()`：获取所有可用的镜头移动方式。
- `getAllShotTypes()`：获取所有可用的镜头类型。
- `getAllLightingTechniques()`：获取所有可用的灯光技巧。
- `suggestCameraTechnique()`：推荐合适的镜头拍摄技巧。
- `suggestLighting()`：推荐合适的灯光效果。
- `suggestColorGrading()`：推荐合适的色彩分级方案。

### 存储管理
- `connectGoogleDrive()`：连接 Google Drive。
- `connectLocalStorage()`：使用本地存储空间。
- `saveScriptToStorage()`：将剧本保存到指定的存储位置。
- `getStorageStatus()`：检查存储连接状态。

## 文件结构

当剧本保存到 Google Drive 时，会生成以下文件结构：

```
📁 Story Title/
├── 00_INDEX.md                    # Navigation
├── 01_SCRIPT_README.md            # Human-readable script
├── 02_IMAGE_PROMPTS.md            # AI generation prompts
├── 03_CHARACTER_REFERENCES.md     # Design guides
├── 04_VOICE_GUIDELINES.md         # Dialogue guides
├── 05_YOUTUBE_METADATA.md         # Upload info
└── 99_CONTEXT_INFO.md             # Background
```

## 系统要求

- **Node.js 18.0 或更高版本**。
- 需要安装并配置 OpenClaw Agent（需具备相应的系统权限）。
- **Google Drive API**（可选，用于文件存储）。

## 标签

创意、视频、剧本编写、电影摄影、一致性、角色设计、语音处理、文件存储、Google Drive、YouTube

## 版本

1.3.0

## 作者

Praveen Kumar

## 许可证

MIT 许可证