---
name: meshy-ai
description: "使用 Meshy.ai 的 REST API 生成资产：  
(1) 将文本转换为 2D 图像（Meshy 的文本到图像功能）；  
(2) 将图像转换为 3D 模型，然后将其下载到本地。  
此功能适用于用户需要 Meshy 生成结果、希望执行异步任务，尤其是当用户希望将生成的 OBJ 文件保存到磁盘时。  
使用此功能前，需确保环境变量中已设置 `MESHY_API_KEY`。"
---

# Meshy.ai

通过 API 生成 Meshy 资源，并将输出结果保存到本地。

## 设置

- 添加环境变量：`MESHY_API_KEY=msy-...`
- 可选：`MESHY_BASE_URL`（默认值为 `https://api.meshy.ai`）

## 文本转换为 2D 图像（Text to Image）

使用 `scripts/text_to_image.py` 脚本。

```bash
python3 skills/public/meshy-ai/scripts/text_to_image.py \
  --prompt "a cute robot mascot, flat vector style" \
  --out-dir ./meshy-out
```

- 如果需要多视图图像，脚本会将生成的图像下载到 `./meshy-out/text-to-image_<taskId>_<slug>/` 目录下。

## 图像转换为 3D 模型（始终保存为 OBJ 格式）

使用 `scripts/image_to_3d_obj.py` 脚本。

### 本地保存的图像

```bash
python3 skills/public/meshy-ai/scripts/image_to_3d_obj.py \
  --image ./input.png \
  --out-dir ./meshy-out
```

### 公共 URL 下的图像

```bash
python3 skills/public/meshy-ai/scripts/image_to_3d_obj.py \
  --image-url "https://.../input.png" \
  --out-dir ./meshy-out
```

- 系统会自动将生成的 `model.obj` 文件（以及 Meshy 提供的 `model.mtl` 文件，如果有的话）下载到 `./meshy-out/image-to-3d_<taskId>_<slug>/` 目录下。

## 注意事项

- Meshy 的任务是异步执行的：创建模型 → 监听任务状态直到状态变为 `SUCCEEDED` → 然后下载相应的文件。
- 有关此功能的 API 参考，请参见 `references/api-notes.md`。