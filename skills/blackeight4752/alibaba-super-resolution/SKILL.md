---
name: alibaba-super-resolution
description: "使用阿里云超级分辨率（Alibaba Cloud Super Resolution）API来提升视频分辨率。适用于以下场景：  
(1) 将低分辨率视频提升为更高分辨率；  
(2) 在发布前优化视频质量；  
(3) 将480p视频转换为1080p视频。"
version: 1.0.0
category: media-processing
argument-hint: "[input video] [output video]"
license: MIT
---
# 阿里云视频超分辨率服务

使用阿里云的视频超分辨率API来提升视频分辨率，将低分辨率视频转换为更高分辨率（例如：480p → 960p）。

## 前提条件

请设置以下环境变量以完成身份验证：

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="your-access-key-id"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="your-access-key-secret"
```

### 可选的OSS配置（针对大文件）

对于超过2GB的文件或直接使用OSS的情况：

```bash
export ALIYUN_OSS_BUCKET="your-bucket-name"
export ALIYUN_OSS_ENDPOINT="oss-cn-shanghai.aliyuncs.com"
```

## 执行方式（Python CLI工具）

相关的Python CLI工具位于`~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py`。

### 快速示例

```bash
# Basic usage: local file → local HD file
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --input videos/input-480p.mp4 \
  --output videos/output-960p.mp4

# Custom bit rate (higher = better quality, larger file)
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --input videos/input-480p.mp4 \
  --output videos/output-960p.mp4 \
  --bit-rate 8

# Do not wait for completion (return job ID immediately)
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --input videos/input-480p.mp4 \
  --no-wait

# Check status of an existing job
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --status <JOB_ID>

# Wait for an existing job and download result
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --wait <JOB_ID> \
  --output videos/output-960p.mp4
```

## 输入要求

### 视频文件

- **格式**：MP4、MOV、AVI、MKV
- **最大文件大小**：2GB（直接上传）/ 无限制（通过OSS URL上传）
- **最长时长**：30分钟
- **输入分辨率**：480p、720p

### 输出分辨率

| 输入分辨率 | 输出分辨率 |
|---------|-----------|
| 480p     | 960p     | （2倍放大） |
| 720p     | 2K      | （2倍放大） |

## 比特率设置

| 比特率    | 质量      | 文件大小    | 处理时间    | 适用场景    |
|---------|---------|---------|---------|-----------|
| 1-3      | 低       | 较小文件   | 快速      | 预览/测试    |
| 4-6      | 中等      | 中等文件   | 中等质量   | 社交媒体    |
| 7-10      | 高       | 大文件    | 较慢      | 高清发布    |

## 规则

1. 在调用API之前，请务必检查配置好的认证信息。
2. **超过2GB的文件**必须通过OSS URL上传，而不能直接上传。
3. **默认比特率**：5（在质量和文件大小之间取得平衡）。
4. **默认超时时间**：1200秒（20分钟）。
5. **输出文件会立即下载**——输出URL在24小时后失效。
6. **优雅地处理错误**——显示清晰的错误信息。

## 故障排除

### VideoTooLarge

**错误**：文件大小超过2GB的限制

**解决方法**：使用OSS URL进行上传。

### Timeout

**错误**：任务超时

**解决方法**：增加超时参数：`--timeout 1800`（30分钟）。

### OSSAccessDenied

**错误**：无法访问OSS

**解决方法**：检查访问密钥的RAM权限，确保其具有OSS的读写权限。

## 相关文档

- [阿里云视频超分辨率服务文档](https://help.aliyun.com/zh/viapi/developer-reference/api-w2n4j6)