# 技能：DJI 视频备份

该技能可自动将 DJI 相机的录像文件从 SD 卡（或 USB 共享设备）备份到 NAS 的归档文件夹中。

## 说明
当用户请求“复制 DJI 视频”或“备份相机数据”等与 DJI 录像文件及 NAS 相关的操作时，可使用此技能。该技能会检测源 SD 卡的位置，找到下一个可用的目标文件夹（文件名格式为 `DJI_001`、`DJI_002` 等），并将文件复制到该文件夹中。

## 使用步骤：
1. **检查源文件夹**：确认 `/Volumes/SD_Card/DCIM`（或类似路径）是否存在。
2. **检查目标文件夹**：查看 `/Volumes/File/DJI_Video/` 目录，找到编号最大的文件夹（例如 `DJI_005`）。
3. **创建新文件夹**：创建下一个编号的文件夹（例如 `DJI_006`）。
4. **复制文件**：将源文件夹 `DCIM`（例如 `100MEDIA` 或 `DJI_001`）中的文件复制到新创建的目标文件夹中。
5. **通知用户**：在开始备份和备份完成后向用户发送通知。

## 文件路径：
- **源文件夹**：`/Volumes/SD_Card/DCIM`（查找名为 `DJI_xxx` 或 `100MEDIA` 的子文件夹）
- **目标文件夹**：`/Volumes/File/DJI_Video`

## 示例逻辑：
```bash
# Find next folder index
last_dir=$(ls -d /Volumes/File/DJI_Video/DJI_* | sort | tail -1)
# extract number, add 1, mkdir new_dir
# cp -R /source/* /new_dir/
```