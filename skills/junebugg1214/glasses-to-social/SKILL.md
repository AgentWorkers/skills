---
name: glasses-to-social
description: 将智能眼镜拍摄的照片转换为社交媒体帖子：监控 Google Drive 文件夹中来自 Meta Ray-Ban 智能眼镜（或其他智能眼镜）的新图片，利用视觉人工智能技术对这些图片进行分析，然后以用户的语音生成推文或帖子内容，并在获得用户批准后发布。该工具适用于建立“眼镜到社交媒体”的数据传输流程、处理智能眼镜拍摄的照片以用于社交媒体发布，或创建无需手动操作的内容工作流程。
---

# Glasses-to-Social

利用人工智能技术，将智能眼镜拍摄的照片转换为适合发布到社交媒体的内容。

## 概述

该功能实现了一个从智能眼镜（如Meta Ray-Ban）到社交媒体的完整流程：

1. 用户佩戴眼镜拍照。
2. 照片自动同步到Google Drive文件夹中。
3. 系统检测到新照片后，通过视觉分析对其进行处理。
4. 系统根据用户的语气和风格生成帖子草稿。
5. 用户审核并确认后，系统将帖子发布到相应的社交媒体平台。

## 设置

### 1. 配置Google Drive文件夹

创建一个用于存储眼镜照片的共享Google Drive文件夹：

```bash
# User creates folder "Glasses-to-Social" in Google Drive
# Share with "Anyone with link can view"
# Copy the folder URL
```

### 2. 设置配置文件

在`glasses-to-social/config.json`文件中配置相关参数：

```json
{
  "googleDriveFolderUrl": "https://drive.google.com/drive/folders/YOUR_FOLDER_ID",
  "folderId": "YOUR_FOLDER_ID",
  "downloadPath": "./glasses-to-social/downloads",
  "processedFile": "./glasses-to-social/data/processed.json",
  "defaultHashtags": ["#MedicalAI", "#HealthTech"],
  "autoPost": false
}
```

### 3. 配置智能眼镜的自动同步功能

对于Meta Ray-Ban眼镜：

1. 在手机上打开Meta View应用程序。
2. 进入“设置” > “相册”，启用“自动导入”功能。
3. 在iOS系统中，启用Google Photos备份功能（以便将相机照片同步到Google Drive）。
4. 创建一个iOS快捷方式，用于将新拍摄的照片自动复制到Google Drive文件夹中。

## 使用方法

### 手动检查

可以手动请求系统检查是否有新照片：

```
Check my glasses folder for new photos
```

### 自动监控

可以设置定时任务（cron job）来定期检查新照片：

```json
{
  "name": "Glasses-to-Social: Check photos",
  "schedule": {"kind": "cron", "expr": "*/15 * * * *", "tz": "UTC"},
  "payload": {
    "message": "Check the Glasses-to-Social folder for new photos. If found, analyze and draft a tweet."
  }
}
```

## 处理流程

当检测到新照片时：

1. 使用`gdown`工具从Google Drive下载照片：
   ```bash
   gdown --folder "FOLDER_URL" -O ./downloads/ --remaining-ok
   ```

2. 将新照片与`data/processed.json`文件中的已处理照片列表进行对比。
3. 对新照片进行视觉分析：
   - 描述场景或主体。
   - 确定适合社交媒体的内容元素。
   - 记录任何文字、人物或显著的元素。
4. 根据用户的语气和风格生成帖子草稿：
   - 保持内容简洁且真实。
   - 添加相关的标签（hashtags）。
   - 以第一人称视角撰写内容效果更佳。
5. 将草稿发送给用户审核：
   - 包含图片预览和生成的标题。
   - 等待用户的“发布”确认或修改意见。
6. 审核通过后，将照片发布到指定的社交媒体平台（如Twitter等）。
7. 在`data/processed.json`文件中标记该照片为已处理状态。

## 脚本

### check-new-photos.sh

用于定期检查Google Drive文件夹中是否有新照片的脚本：

```bash
scripts/check-new-photos.sh
```

**发现新照片时的输出格式：**
```
NEW_PHOTO_PATH:/path/to/downloaded/photo.jpg
```

## 文件跟踪

在`data/processed.json`文件中记录所有已处理的照片信息：

```json
{
  "processed": ["photo1.jpg", "photo2.jpg"],
  "pending": []
}
```

## 提示：

- 以第一人称视角撰写内容效果更佳（例如：“看，我刚刚看到了什么...”）。
- 确保标题真实自然，避免过度修饰。
- 该功能非常适合记录会议内容、有趣的瞬间或日常点滴。
- 在生成帖子时，请考虑时间背景等因素。

## 所需软件和资源：

- `gdown`（Python包），用于访问Google Drive。
- 具有图像分析功能的模型。
- Twitter或X（Facebook）的登录凭据（可选）。