---
name: trtc-config-inspector
description: "TRTC SDK配置检查与分析工具：  
该工具可以从用户提供的URL下载场景配置模板（Excel格式）及检查结果（Excel格式）和项目代码，将检查结果与目标场景配置进行对比，定位源代码中的TRTC相关参数，并生成结构化的修改报告。随后，AI代理会根据该报告执行代码修改。该工具支持实时流媒体、语音聊天室、视频通话等多种场景。  
主要功能包括：  
- TRTC配置检查  
- 配置对比与代码修改  
- TRTC场景配置优化  
触发条件：  
- 执行TRTC配置检查  
- 对比配置并修改代码  
- 优化TRTC场景配置"
version: 2.1.0
author: CwlVincent
permissions: "Network access (download Excel and code files from user-provided URLs), file read access (parse config Excel and scan source code)"
---
# TRTC 配置检查器

该工具会对比 TRTC 场景配置模板与检查结果，生成结构化的差异报告，并指导 AI 代理或用户根据报告调整源代码。

## 描述

此技能实现了 TRTC SDK 配置的检查与分析，并提供修改建议：
1. **下载资源**：从用户提供的 URL 下载场景配置模板 Excel 文件、检查结果 Excel 文件以及项目代码压缩包。
2. **解析与对比**：解析两个 Excel 文件，逐项比较当前配置与目标配置。
3. **定位代码**：在项目源代码中找到对应的 TRTC API 调用位置。
4. **生成修改计划**：输出结构化的修改建议（JSON 格式），包括目标值、代码位置以及每个差异项的修改建议。
5. **输出报告**：生成差异汇总表；AI 代理随后使用代码编辑工具应用这些修改。

> **注意**：这些脚本本身不会修改任何用户代码，仅生成分析报告和修改建议。实际代码修改由 AI 代理使用标准代码编辑工具（如 `replace_in_file`）完成，用户可以查看每个修改步骤。

## 适用场景

当用户提出以下请求时，可触发此技能：
- “根据这个检查结果和直播配置帮助我修改代码”
- “下载这些文件并根据 TRTC 配置模板优化代码”
- “对比 TRTC 检查配置并按模板修改代码”
- “检查 TRTC SDK 配置是否符合场景要求”
- 用户提供了场景配置 Excel 文件（`scene_config_*.xlsx`）和/或检查结果 Excel 文件（`inspection_result_*.xlsx`）

## 使用方法

### 第一步：收集用户输入

与用户确认以下信息（如果尚未提供）：

| 参数 | 描述 | 是否必填 |
|---|---|---|
| 场景配置模板 | 场景配置 Excel 文件的 URL 或本地路径 | 必填 |
| 检查结果 | 检查结果 Excel 文件的 URL 或本地路径 | 必填（如果未提供，则仅输出目标配置） |
| 代码下载链接 | 项目代码压缩包的 URL 或本地目录路径 | 必填 |

用户可以通过多种方式提供输入：
- 直接的 URL 链接
- 本地文件/目录路径
- 工作区中已存在的文件

### 第二步：下载资源文件

使用下载脚本获取远程文件：

```bash
python3 SKILL_BASE_DIR/scripts/download_files.py \
  --config-url "Scene config Excel URL" \
  --inspect-url "Inspection result Excel URL" \
  --code-url "Code archive URL" \
  --output-dir "SKILL_BASE_DIR/workspace"
```

该脚本将：
- 将场景配置 Excel 文件下载到 `workspace/config.xlsx`
- 将检查结果 Excel 文件下载到 `workspace/inspect.xlsx`
- 将代码文件下载并解压到 `workspace/code/`
- 输出包含每个文件本地路径的 JSON 格式下载结果

如果用户提供了本地文件路径，则跳过该文件的下载，直接使用本地路径。

### 第三步：解析并对比配置

运行差异脚本以生成差异报告：

```bash
python3 SKILL_BASE_DIR/scripts/diff_config.py "inspection_result_excel_path" "scene_config_excel_path"
```

JSON 报告输出包含：
- `diffs` — 当前值与目标值不同的配置项（需要修改代码）
- `matches` — 已经匹配的配置项（无需修改）
- `unable_to_compare` — 无法自动对比的项（需要手动审核）

如果只有场景配置模板（没有检查结果），则直接解析模板：

```bash
python3 SKILL_BASE_DIR/scripts/parse_excel.py "scene_config_excel_path" --type config
```

### 第四步：根据报告定位并修改代码

根据差异报告中的 `diffs` 数组，AI 代理使用代码编辑工具找到代码中的相应 API 调用并修改参数值。以下是配置项与代码 API 之间的对应关系：

#### 4.1 房间进入模式（Scene / AppScene）

找到 `enterRoom` 调用，并修改第二个参数。

| 配置值 | Android 代码常量 | iOS 代码常量 |
|---|---|---|
| `Live` | `TRTCCloudDef.TRTC_APP_SCENE_LIVE` | `TRTCAppSceneLIVE` |
| `VideoCall` | `TRTCCloudDef.TRTC_APP_SCENE_VIDEOCALL` | `TRTCAppSceneVideoCall` |
| `AudioCall` | `TRTCCloudDef.TRTC_APP_SCENE_AUDIOCALL` | `TRTCAppSceneAudioCall` |
| `VoiceChatRoom` | `TRTCCloudDef.TRTC_APP_SCENE_VOICECHATROOM` | `TRTCAppSceneVoiceChatRoom` |

#### 4.2 音频质量

找到 `startLocalAudio` 调用。

| 配置值 | Android 代码常量 | iOS 代码常量 |
|---|---|---|
| `MUSIC` | `TRTCCloudDef.TRTC_AUDIO_QUALITY_MUSIC` | `TRTCAudioQualityMusic` |
| `DEFAULT` | `TRTCCloudDef.TRTC_AUDIO_QUALITY_DEFAULT` | `TRTCAudioQualityDefault` |
| `SPEECH` | `TRTCCloudDef.TRTC_AUDIO_QUALITY_SPEECH` | `TRTCAudioQualitySpeech` |

#### 4.3 系统音量类型

找到 `setSystemVolumeType` 调用。

| 配置值 | Android 代码常量 | iOS 代码常量 |
|---|---|---|
| `media` | `TRTCCloudDef.TRTCSystemVolumeTypeMedia` | `TRTCSystemVolumeTypeMedia` |
| `voip` | `TRTCCloudDef.TRTCSystemVolumeTypeVOIP` | `TRTCSystemVolumeTypeVOIP` |
| `auto` | `TRTCCloudDef.TRTCSystemVolumeTypeAuto` | `TRTCSystemVolumeTypeAuto` |

#### 4.4 视频编码器参数

找到 `setVideoEncoderParam` 调用和 `TRTCVideoEncParam` 对象。

**重要提示 — 视频编码器参数必须逐项对比；不要遗漏任何子参数：**

在场景配置 Excel 中，视频编码器参数（分辨率、FPS、比特率）分布在多行中。差异脚本会分别输出每个子参数的对比结果。**必须检查并应用所有视频编码器子参数的差异**，包括：
- **分辨率**：例如，“推荐 720p” -> 更新 `videoResolution`
- **FPS**：例如，“25fps” -> 更新 `videoFps`（**经常被忽略！**）
- **比特率**：例如，“720p-1800kbps” -> 更新 `videoBitrate`

| 参数 | 字段名 | 描述 |
|---|---|---|
| Resolution | `videoResolution` | 例如，`TRTC_VIDEO_RESOLUTION_1280_720`（720p） |
| FPS | `videoFps` | 整数，例如 15 或 25 |
| Bitrate | `videoBitrate` | 整数（kbps），例如 1800 |
| Min Bitrate | `minVideoBitrate` | 整数（kbps） |
| Resolution Mode | `videoResolutionMode` | `PORTRAIT` 或 `LANDSCAPE` |
| Adaptive Resolution | `enableAdjustRes` | 布尔值 |

分辨率常量对应关系：
- 540p -> `TRTC_VIDEO_RESOLUTION_960_540`
- 720p -> `TRTC_VIDEO_RESOLUTION_1280_720`
- 1080p -> `TRTC_VIDEO_RESOLUTION_1920_1080`

推荐的比特率：
- 540p -> 1300 kbps
- 720p -> 1800 kbps
- 1080p -> 3000 kbps

#### 4.5 捕获音量 / 远端播放音量

找到 `setAudioCaptureVolume` 和 `setAudioPlayoutVolume` 调用。

#### 4.6 实验性 API

找到带有 JSON 字符串参数的 `callExperimentalAPI` 调用。Excel 文件的 `code_example` 列提供了具体的 JSON 结构。

### 第五步：确保 API 调用顺序正确

当 AI 代理修改代码时，TRTC API 调用必须遵循以下顺序：
1. `TRTCCloud.sharedInstance()` — 创建实例
2. `setListener()` — 设置回调监听器
3. `setSystemVolumeType()` — 设置音量类型（在进入房间之前）
4. `callExperimentalAPI()` — 实验性设置（在进入房间之前）
5. `setVideoEncoderParam()` — 设置视频编码器参数
6. `startLocalPreview()` — 启动本地摄像头预览
7. `startLocalAudio()` — 启动本地音频捕获
8. `enterRoom()` — 进入房间

### 第六步：输出修改报告

完成所有修改后，输出汇总表：

| 配置项 | 修改前 | 修改后 | 状态 |
|---|---|---|---|
| 房间进入模式 | VideoCall | Live | 已修改 |
| 音频质量 | DEFAULT | MUSIC | 已修改 |
| 系统音量类型 | VOIP | Media | 已修改 |
| 视频分辨率 | 640x480 | 1280x720 | 已修改 |
| 视频 FPS | 15fps | 25fps | 已修改 |
| 视频比特率 | 900kbps | 1800kbps | 已修改 |

对于标记为“可选”的项，告知用户是否应用这些修改。

## 实现方式

### 依赖项

- Python 3.8+
- `openpyxl`（如果未安装则自动安装）
- `requests`（如果未安装则自动安装）

### 脚本清单

| 脚本 | 功能 |
|---|---|
| `scripts/download_files.py` | 从 URL 下载场景配置、检查结果和代码压缩包并解压 |
| `scripts/parse_excel.py` | 解析单个 Excel 文件（场景配置或检查结果）并输出结构化 JSON |
| `scripts/diff_config.py | 对比检查结果与场景配置模板并输出差异报告 |
| `scripts/run_inspector.py` | 全端检查流程：下载 -> 解析 -> 对比 -> 分析代码 -> 生成修改计划 |

### 核心函数

- `download_files.py::download_and_extract(config_url, inspect_url, code_url, output_dir)` — 下载并解压所有资源文件
- `parse_excel.py::parse_config_excel(filepath)` — 解析场景配置 Excel 文件
- `parse_excel.py::parse_inspect_excel(filepath)` — 解析检查结果 Excel 文件
- `diff_config.py::diff_configs(inspect_data, config_data)` — 对比配置文件并输出差异

## 边缘情况

- **URL 无法访问**：提示用户验证链接是否有效或是否需要登录授权
- **Excel 格式异常**：捕获解析异常，提示用户确认文件格式是否符合 TRTC 平台的导出标准
- **代码中找不到 API 调用**：在报告中标记为“新添加”，AI 代理会按照 API 调用顺序将其添加到代码中
- **可选配置项**：标记为“可选”的项不会自动修改；提示用户决定是否应用
- **多平台代码**：自动检测代码语言（Kotlin/Java/Swift/ObjC）并相应调整语法
- **代码压缩包格式**：支持 .zip 和 .tar.gz 格式

## 重要说明

- Excel 文件由 TRTC 平台检查工具和场景配置工具生成
- 修改代码时，请保持现有代码结构，仅更改特定参数值
- 对于 Kotlin 项目，将 Excel 中的 Java 示例代码转换为 Kotlin 语法
- `code_example` 列提供了参考实现；请根据项目的实际代码风格进行调整
- **视频编码器参数必须逐项检查**：差异脚本会分别输出每个子参数的差异；所有参数都必须应用。FPS 是最容易遗漏的参数

## 安全性

- **脚本不修改代码**：所有 Python 脚本（`download_files.py`、`parse_excel.py`、`diff_config.py`、`run_inspector.py`）仅执行下载、解析、对比和分析操作。**它们不会直接修改任何用户源代码文件**。代码修改由 AI 代理使用标准编辑工具完成，用户可以查看每个修改步骤。
- **URL 由用户控制**：脚本仅从用户提供的 URL 下载文件；不会访问任何硬编码的外部地址。
- **解压范围有限**：代码压缩包仅解压到指定的工作区输出目录。
- **不存储凭证**：脚本不会读取、存储或传输任何密钥、令牌或用户凭证。
- **运行时依赖项**：仅自动安装 `openpyxl`（Excel 解析）和 `requests`（HTTP 下载），这两个都是标准的 PyPI 包。