---
name: image-nuke
description: "**核级图像元数据清洗工具**：  
该工具能够彻底清除图像中的所有 EXIF、GPS 信息以及相机相关数据，并通过添加噪声来实现重新编码。这样的处理方式使得图像在法医学调查中无法被追踪，同时也能有效抵抗反向图像搜索技术。"
metadata:
  openclaw:
    emoji: "☢️"
    requires:
      bins: ["python3"]
---
# Image Nuke - 核心元数据清除工具

该工具能够彻底清除图像中的所有元数据，包括 EXIF 数据、GPS 位置信息、ICC 色彩配置文件、XMP/IPTC 元数据以及 Adobe 标签和编辑历史记录等。同时，通过注入高斯噪声和进行微妙的颜色调整，使得图像在法医调查中无法被追踪。

## 清除的内容：

- 所有 EXIF 元数据（包括相机型号、镜头信息、曝光参数、时间戳、使用软件等）
- GPS 位置坐标
- ICC 色彩配置文件
- XMP/IPTC 元数据
- Adobe 标签及编辑记录
- 嵌入的缩略图

## 核心处理步骤：

- 注入亚像素级的高斯噪声（人眼无法察觉）
- 进行微妙的颜色调整（无法检测到色调变化）
- 对每个像素进行亮度调整
- 随机裁剪图像（尺寸变化 1-3 像素）
- 使用随机化的质量设置和采样率重新编码图像为 JPEG 格式
- 生成全新的图像哈希值（防止图像被反向搜索）

## 使用方法：

```bash
# Single image - nuclear mode
python3 {baseDir}/scripts/nuke_image.py photo.jpg

# Custom output + max noise
python3 {baseDir}/scripts/nuke_image.py photo.jpg clean.jpg --noise 5

# Batch process entire directory
python3 {baseDir}/scripts/nuke_image.py --batch ./photos/ ./clean/

# Lower quality for harder reverse matching
python3 {baseDir}/scripts/nuke_image.py photo.jpg --quality 80 --noise 4
```

## 噪声强度等级：

| 等级 | 噪声标准（Sigma） | 适用场景 |
|-------|-------|----------|
| 1    | 0.8       | 轻度清除 - 仅去除部分元数据 |
| 2    | 1.6       | 标准设置 - 平衡性较好 |
| 3    | 2.4       | 默认设置 - 推荐使用 |
| 4    | 3.2       | 强度较高 - 更难被反向搜索 |
| 5    | 4.0       | 最高级别 - 最大程度匿名化 |

## 系统要求：

- Python 3
- Pillow 库（需通过 `pip install Pillow` 安装）
- NumPy 库（需通过 `pip install numpy` 安装）

## 注意事项：

- 输出格式始终为 JPEG（即使输入文件为 PNG）
- 原始文件不会被修改
- 每次运行都会生成不同的输出结果（因为噪声是随机生成的）