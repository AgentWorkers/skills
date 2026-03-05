# 图像质量过滤工具

该工具用于检测并过滤掉质量较低的图像，包括模糊、颜色过暗或过亮、分辨率过低的图像。适用于用户需要清理图像数据集（去除质量不佳的图片）的场景。

## 主要功能

- **模糊检测**：利用拉普拉斯方差算法检测图像是否模糊。
- **亮度分析**：判断图像是否过暗或过亮。
- **分辨率过滤**：移除分辨率低于指定阈值的图像。
- **质量评分**：计算图像的整体质量。
- **批量处理**：支持处理大量图像文件。
- **多种操作选项**：可以列出、删除或移动质量不佳的图像。

## 使用方法

```bash
# Scan for low quality images
python scripts/quality_filter.py scan /path/to/images/

# Filter with custom thresholds
python scripts/quality_filter.py scan /path/to/images/ \
  --blur-threshold 100 \
  --min-resolution 640x480 \
  --min-brightness 30 \
  --max-brightness 220

# Delete low quality images
python scripts/quality_filter.py scan /path/to/images/ --action delete
```

## 使用示例

```
$ python scripts/quality_filter.py scan ./images/

Scanning 150 images...
Analyzing quality...
Found 12 low-quality images:

[BLUR]   photo_blurry.jpg (score: 45)
[BLUR]   image_low.jpg (score: 62)
[DARK]   dark_photo.jpg (score: 38)
[BRIGHT] overexposed.jpg (score: 41)
[RES]    tiny_image.png (320x240)

Total: 12 low-quality images removed
```

## 质量判断标准

| 判断标准 | 阈值 | 说明 |
|---------|---------|--------|
| 模糊度 | < 100 | 拉普拉斯方差值越低，图像越模糊 |
| 亮度 | 30-220 | 亮度值超出此范围表示图像质量较差 |
| 分辨率 | > 640x480 | 分辨率低于此值表示图像质量较低 |

## 安装方法

```bash
pip install pillow numpy opencv-python
```

## 命令行参数选项

- `--blur-threshold`：模糊度阈值（默认值：100）
- `--min-resolution`：最低分辨率（默认值：640x480）
- `--min-brightness`：最低亮度值（范围：0-255，默认值：30）
- `--max-brightness`：最高亮度值（范围：0-255，默认值：220）
- `--action`：对图像执行的操作（列出、删除或移动）
- `--output`：用于保存处理后图像的文件夹路径（仅当选择“移动”操作时使用）