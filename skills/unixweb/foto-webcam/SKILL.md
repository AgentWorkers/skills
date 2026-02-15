---
name: foto-webcam
description: 列出并获取网络摄像头的快照（包括来自 foto-webcam.eu 的摄像头）。当 John 输入 “webcam <number>” 时，可以使用此技能指南来管理网络摄像头收藏列表；或者当需要将来自 foto-webcam.eu 摄像头的当前快照图像以 JPG 格式发送到聊天中时，也可以使用该指南。
---

# 照片-网络摄像头快照功能

**目标**：从保存的收藏列表中（根据编号访问对应的摄像头页面）获取当前图片，并发送给John。

## 数据来源（收藏列表）

工作区中的标准文件：
- `docs/webcams/favorites-muenchen.json`

**文件格式（示例）：**
- `items[]`.id` （整数）
- `items[]`.name` （字符串）
- `items[]`.page` （摄像头页面的URL）
- 可选 `items[]`.image` （图片的直接URL）

## 常见用户命令：
- `webcam 1`  
- `webcam 3+4+5`  
- `liste`  
- `liste webcams`  
- `fuege <name> <url> hinzu` （添加新的摄像头条目）

## 工作流程：获取摄像头N的图片并发送
1. 从 `docs/webcams/favorites-muenchen.json` 中加载收藏列表。
2. 查找编号为N的条目。
3. 生成快照图片：
   - 如果提供了 `image`，则加载该图片的URL；
   - 否则，使用页面URL并从中提取当前图片（格式为1200像素的JPG）。
4. 将图片保存到 `/tmp/webcamN.jpg` 文件夹中。
5. 以附件形式将图片发送到聊天中，附带图片说明（格式：`摄像头N 名称`）。

## 工作流程：获取摄像头3+4+5的多张图片
1. 将ID解析为整数列表（按顺序）。
2. 对于每个ID：
   - 获取快照图片。
   - 将图片发送到聊天中。
3. 每次请求最多发送6张图片；如果需要更多图片，则需要重新请求。

## 工作流程：将列表发送到收藏列表
发送一个纯文本列表，格式如下：
```
Webcam 1 名称
Webcam 2 名称
...
```

## 图片URL的获取方式（foto-webcam.eu）
对于像 `https://www.foto-webcam.eu/webcam/zugspitze/` 这样的摄像头页面，通常存在一个直接的“current”图片链接：
```
https://www.foto-webcam.eu/webcam/zugspitze/current/1200.jpg`
```
实际操作方法：通过发送带有用户代理的HTTP请求，然后查找 `.../current/<digits>.jpg` 的链接来获取图片。

## 脚本使用
使用以下脚本：
- `skills/public/foto-webcam/scripts/foto_webcam_snapshot.py`

**使用示例：**
- 通过收藏ID获取快照：
  ```
  python3 skills/public/foto-webcam/scripts/foto_webcam_snapshot.py --favorites docs/webcams/favorites-muenchen.json --id 4 --out /tmp/webcam4.jpg
  ```
- 通过URL获取快照：
  ```
  python3 skills/public/foto-webcam/scripts/foto_webcam_snapshot.py --url https://www.foto-webcam.eu/webcam/zugspitze/ --out /tmp/zugspitze.jpg
  ```

## 维护与更新：
- 添加新的摄像头时，更新 `favorites-muenchen.json` 文件（包含新的 `id`、`name` 和 `page`）。
- 如果某个图片来源不稳定，可以设置 `image` 为图片的直接URL。

**注意事项**：
- 聊天中的回复应仅使用纯文本（不要使用Markdown格式）。
- 音频内容应使用“clean speech”格式（避免特殊字符和格式化）。