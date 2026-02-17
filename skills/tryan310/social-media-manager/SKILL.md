# 技能：TikTok自动化（Larry风格）

## 目标
使用AI生成技术和Postiz工具，自动化创建和起草高互动性的TikTok幻灯片（共6张）。

## 工作流程
1. **研究与构思**：运用“冲突公式”（Conflict Formula）来头脑风暴创意：
   `[人物] + [冲突/疑问] -> [AI解决方案] -> [解决方案]`。
2. **图片生成**：生成6张幻灯片：
   - **尺寸**：1024x1536（竖屏格式）。
   - **图片模型**：逼真效果（例如：Nano Banana Pro / gpt-image-1.5）。
   - **幻灯片1**：展示“初始状态”或“冲突”场景，并叠加提示文字。
   - **幻灯片2-5**：展示“转变过程”或不同的风格选项。
   - **幻灯片6**：展示“最终结果”并包含行动号召。
3. **一致性检查**：确保所有幻灯片在主题和风格上保持一致。
   - *重要提示*：详细描述场景的尺寸、窗户布局等信息，并在每次生成时重复使用这些信息；仅调整图片的风格、光线和装饰。
4. **起草内容**：通过Postiz API将幻灯片以`SELF_ONLY`（草稿模式）上传到TikTok。
5. **通知用户**：发送通知，附上TikTok应用的链接，提醒用户添加音乐并发布视频。

## 项目：FastPassPhoto
- **网址**：fastpassphoto.com
- **产品**：AI护照/身份证照片生成及编辑工具。
- **价格**：15.95美元
- **使用的图片模型**：Nano Banana Pro（Gemini 3 Pro）

## 提示策略（Prompt Strategy）：
- **冲突公式**：[用户] 需要护照照片 + [常见问题] -> [FastPassPhoto的解决方案] -> [成功/获得批准]。
- **常见问题**：
  - 去实体商店（邮局或CVS）很麻烦。
  - 因光线或背景不佳被护照办理处拒绝。
  - 对自己的照片不满意。
  - 时间紧迫（需要立即出行）。

## Postiz配置
- **API地址**：`https://api.postiz.com/public/v1`
- **认证头**：`Authorization: <API_KEY>`（不需要使用Bearer认证方式）。
- **媒体上传**：必须先使用`POST /upload`请求获取图片的`id`和`path`。
- **发布方式**：上传TikTok幻灯片时始终使用`UPLOAD`方法；`DIRECT_POST`在处理多张图片时经常失败。
- **发布结构**：
  - 最顶层：`type`（如“now”）、`date`（ISO 8601格式的日期）和`posts`（数组）。
  - 单个帖子的结构：`integration: { id: "..." }`，`value: [ { content: "...", image: [ { id, path } ] } ]`。
  - 设置配置：`settings: { __type: "tiktok", content_posting_method: "UPLOAD", privacy_level: "SELF_ONLY", ... }`。

## 技术细节
- **上传媒体文件**：
  `curl -X POST {API_URL}/upload -H "Authorization: {KEY}" -F "file=@path/to/file"`
- **创建帖子**：
  `curl -X POST {API_URL}/posts -H "Authorization: {KEY}" -H "Content-Type: application/json" -d '{...}'`

## 成功日志
- **2026-02-14**：成功发布了包含6张幻灯片的TikTok视频（使用了“冲突公式”策略）。修正了API参数：`duet`/`stitch`/`comment`（布尔值）、`autoAddMusic`（“yes”/“no”）、`brand_content_toggle`/`brand_organic_toggle`（布尔值）。同时确保添加了`shortLink`（布尔值）和`tags`（数组）字段。
- **2026-02-13**：成功将上传方式改为`UPLOAD`来发布TikTok幻灯片；发现`DIRECT_POST`在处理多张图片时会导致错误。

## 失败日志
- **2026-02-13**：API认证需要使用`Authorization: <KEY>`。
- **2026-02-13**：Postiz要求在配置中设置`content_posting_method`和`privacy_level`。
- **2026-02-13**：通过Postiz上传TikTok幻灯片时，需要提供有效的媒体文件URL（格式为uploads.postiz.com）以及正确的`posts`数组结构。