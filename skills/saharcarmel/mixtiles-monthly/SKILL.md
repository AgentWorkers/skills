---
name: mixtiles-monthly
description: >
  自动化每月照片转Mixtiles的流程：  
  该流程会从WhatsApp群组中收集照片，利用图像识别技术筛选出最优质的照片，生成一个包含多张照片的Mixtiles订单链接，然后将其发送出去。  
  适用场景包括：  
  - 每月需要生成Mixtiles订单时；  
  - 被要求“运行每月的照片处理任务”时；  
  - 需要收集家庭照片以用于生成Mixtiles时；  
  - 通过每月的定时任务（cron trigger）自动执行该流程时。
metadata: {"openclaw": {"emoji": "🖼️", "requires": {"bins": ["wacli", "jq", "python3"]}}}
---
# Mixtiles 月度处理流程

每月自动从 WhatsApp 群组中收集最佳的家庭照片，对这些照片进行筛选，并生成一个可购买的 Mixtiles 购物车链接。

## 配置

以下环境变量用于控制整个处理流程。请在运行前设置它们：

| 变量          | 描述                                      | 默认值       |
|---------------|-----------------------------------------|------------|
| `MIXTILES_GROUP_JID` | 用于收集照片的 WhatsApp 群组 ID             | *(必填)*     |
| `MIXTILES_SEND_TO` | 购物车链接的发送目标（群组 ID 或电话号码）           | 与 `MIXTILES_GROUP_JID` 相同 |
| `MIXTILES_PHOTO_COUNT` | 需要选择的照片数量                         | `4`         |
| `MIXTILES_tile_SIZE` | 购物车中使用的瓷砖尺寸                         | `RECTANGLE_12X16`   |

## 处理流程步骤

### 第一步：收集照片

计算上个月的日期范围，并从群组中下载所有照片：

```bash
# Calculate first day of last month
YEAR_MONTH=$(date -v-1m +%Y-%m)  # macOS
AFTER_DATE="${YEAR_MONTH}-01"
OUTPUT_DIR=~/mixtiles-queue/${YEAR_MONTH}

# Run the collection script
bash <skill-dir>/scripts/collect-photos.sh "$MIXTILES_GROUP_JID" "$AFTER_DATE" "$OUTPUT_DIR"
```

脚本会将下载到的每张照片的信息（包括 `id`、`sender`、`timestamp` 和 `filepath`）以 JSON 格式输出到标准输出（stdout）。

### 第二步：使用视觉识别技术进行筛选

使用视觉识别技术分析每张下载的照片。对于每张照片，判断是否满足以下条件：

**符合条件则纳入筛选范围：**
- 真实的生活或家庭场景（人物、聚会、重要时刻、孩子、旅行、宠物）
- 图像质量良好（清晰、光线充足、对焦准确）
- 图像具有独特性（与其他照片无明显重复）

**不符合条件则排除：**
- 屏幕截图、表情包、转发的图片或链接预览
- 图像模糊、过暗或质量过低
- 与已选中的高质量照片高度相似
- 包含大量文字的图片（如 WhatsApp 转发的内容、新闻文章）
- 促销内容或广告

### 第三步：挑选最佳照片

从筛选后的照片中选出 `$MIXTILES_PHOTO_COUNT` 张照片（默认值为 4 张）。优先考虑以下类型：
1. 人物和面部（尤其是孩子、家庭聚会）
2. 重要时刻（生日、首次走路、毕业等）
3. 旅行经历
4. 照片的多样性（如果同一事件有多张符合条件的照片，不要只选 4 张）

如果符合条件的照片数量少于 `$MIXTILES_PHOTO_COUNT`，则选择所有符合条件的照片。

### 第四步：生成多张照片的购物车链接

使用 `mixtiles-it` 技能的脚本，并添加 `--batch` 标志：

```bash
MIXTILES_CART_SCRIPT="$(find ~/.openclaw/workspace/skills/mixtiles-it/scripts -name 'mixtiles-cart.py')"

python3 "$MIXTILES_CART_SCRIPT" \
  --batch <photo1> <photo2> <photo3> <photo4> \
  --size "${MIXTILES_TILE_SIZE:-RECTANGLE_12X16}"
```

该脚本会将所有照片上传到 Cloudinary 并生成一个包含所有照片的 Mixtiles 购物车链接。

### 第五步：发送购物车链接

将生成的购物车链接发送到指定聊天对象：

```bash
SEND_TO="${MIXTILES_SEND_TO:-$MIXTILES_GROUP_JID}"

wacli send text \
  --to "$SEND_TO" \
  --message "Your monthly tiles are ready! Here are the best ${MIXTILES_PHOTO_COUNT:-4} photos from last month. Tap to customize and order: $CART_URL"
```

## 错误处理

- 如果 `collect-photos.sh` 没有找到任何照片：报告该时间段内没有找到图片，并跳过整个处理流程。
- 如果符合筛选条件的照片数量少于 `$MIXTILES_PHOTO_COUNT`：仍会发送所有符合条件的照片（即使只有 1 张）。
- 如果某张照片上传到 Cloudinary 失败：跳过该照片，继续处理剩余的照片。
- 如果 `wacli send` 命令失败：打印购物车链接，以便用户可以手动发送。

## 手动触发方式

若需在非每月固定时间运行此流程，可以执行以下操作：

> 运行 `mixtiles-monthly` 技能：从家庭群组中收集上个月的照片，筛选出最佳照片，生成多张照片的购物车链接，并发送出去。