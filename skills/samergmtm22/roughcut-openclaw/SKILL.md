---
name: roughcut
description: "在 macOS 上无头运行 RoughCut，从带有旁白的视频中生成 Final Cut Pro (FCPXML) 格式的粗略剪辑时间线版本——优先使用本地资源，无需上传任何媒体文件。"
metadata:
  {
    "openclaw":
      {
        "os": ["darwin"],
        "requires":
          {
            "bins": ["bash", "python3", "curl", "ffmpeg", "node", "npm"],
            "config": [
              "skills.entries.roughcut.config.repo_root",
              "skills.entries.roughcut.config.output_root"
            ]
          },
        "primaryEnv": "GEMINI_API_KEY"
      }
  }
---
# RoughCut（macOS）

此功能允许OpenClaw代理在用户的Mac上本地运行RoughCut工具，从原始视频文件生成`RoughCut.xml_variants.zip`文件，而无需上传视频文件。

## 前提条件

1. 确认视频文件存在于本地磁盘上，并获取其绝对路径（示例：`/Users/alice/Movies/raw.mp4`）。如果视频文件位于Google Drive、iCloud或Dropbox中，请确保已完全下载并可以作为本地文件路径访问。  
   提示：在macOS上，您可以将视频文件拖放到终端中以复制其绝对路径。  
   如果用户使用的机器与运行OpenClaw的Mac不同，请确定数据传输方式：  
     - 同步文件夹：一个会同步到OpenClaw Mac的文件夹（例如iCloud Drive、Dropbox、Google Drive Desktop等）。  
     - 直接下载链接：请求用户提供直接的HTTPS下载链接（例如S3/R2/GCS预签名链接），然后使用`--video-url`参数运行RoughCut工具（视频文件将自动保存在`output_root/RoughCut.inputs/`目录中）。  

2. 确保RoughCut仓库存在于同一台Mac上。  
   仓库地址：https://github.com/samerGMTM22/OpenClaw-RoughCut  

3. 如果用户启用了视频中的无关内容（如广告、多余画面等）的去除功能，请确保在运行RoughCut的环境中设置了`GEMINI_API_KEY`。  
   如果未设置该密钥，请让用户提供密钥，并说明该密钥仅用于此目的。  

## 需要向用户询问的问题

1. 是否希望删除视频中的不良片段？（默认值：是）  
2. 是否希望删除视频中的无关内容或离题的部分？（默认值：否）  
3. 如果启用了无关内容去除功能，请说明视频的主题或处理目标。  

## 运行方法

使用OpenClaw配置文件中的`repo_root`和`output_root`路径：

```bash
bash "$REPO_ROOT/scripts/openclaw/roughcut.sh" \
  --video "$VIDEO_ABS_PATH" \
  --out "$OUTPUT_ROOT" \
  --remove-bad-takes true \
  --remove-fluff false
```  

如果用户提供了直接下载链接，可以直接使用该链接（运行脚本时会先将视频文件下载到`$OUTPUT_ROOT/RoughCut.inputs/`目录中）：  

```bash
bash "$REPO_ROOT/scripts/openclaw/roughcut.sh" \
  --video-url "$VIDEO_URL" \
  --out "$OUTPUT_ROOT" \
  --remove-bad-takes true \
  --remove-fluff false
```  

如果下载链接不包含文件名（这种情况常见于预签名链接），请添加`--video-name`参数；可选地，还可以添加`--video-sha256`参数：  

```bash
bash "$REPO_ROOT/scripts/openclaw/roughcut.sh" \
  --video-url "$VIDEO_URL" \
  --video-name "my_video.mov" \
  --video-sha256 "0123456789abcdef..." \
  --out "$OUTPUT_ROOT" \
  --remove-bad-takes true \
  --remove-fluff false
```  

如果启用了无关内容去除功能：  

```bash
bash "$REPO_ROOT/scripts/openclaw/roughcut.sh" \
  --video "$VIDEO_ABS_PATH" \
  --out "$OUTPUT_ROOT" \
  --remove-bad-takes true \
  --remove-fluff true \
  --topic "$TOPIC"
```  

脚本会将处理结果以JSON格式输出到标准输出（stdout）中。成功时，输出内容包括：  
- `xml_variants_zip`：`RoughCut.xml_variants.zip`文件的绝对路径  
- `video_path`：用于处理的输入视频文件的绝对路径  
- `downloaded_video_path`：仅在使用了`--video-url`参数时输出（即视频文件的保存路径）  

如果处理失败，输出内容将包含：  
- `error`：错误信息  
- 可选地：`debug_zip`：包含中间处理结果的文件包  

## 需要返回给用户的信息

1. 处理后的视频文件的压缩包路径。  
2. 如何将处理后的文件导入Final Cut Pro：  
   - 解压`RoughCut.xml_variants.zip`文件。  
   - 在Final Cut Pro中，选择“文件”→“导入”→“XML...”选项，然后选择所需的`.fcpxml`文件格式。