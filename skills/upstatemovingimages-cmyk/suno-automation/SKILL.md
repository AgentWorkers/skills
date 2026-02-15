# Suno 技能

该技能允许代理通过 OpenClaw 管理浏览器来控制 Suno（suno.com）网站，从而生成音乐。

## 先决条件

1. **OpenClaw 浏览器：** 必须已启动（使用 `openclaw browser start` 命令）。
2. **登录：** 用户必须在管理浏览器中登录到 Suno 账户（使用 `openclaw` 命令）。

## 使用方法

1. **打开 Suno 网站：`browser open https://suno.com/create``
2. **获取元素引用：`browser snapshot`（用于获取页面元素的引用）。
3. **输入歌词：`browser act type <ref> "你的歌词..."`
4. **输入歌曲风格：`browser act type <ref> "歌曲风格描述..."`
5. **设置歌曲标题：`browser act type <ref> "歌曲标题"``
6. **创建新歌曲：`browser act click <create_button_ref>`
7. **等待并播放：** 等待新歌曲出现在列表中，然后点击 `play_button_ref` 播放歌曲。

## 示例（代理的操作流程）

1. `browser action=start profile=openclaw`
2. `browser action=open profile=openclaw url=https://suno.com/create`
3. （如果用户尚未登录，则手动登录）
4. `browser action=snapshot` → 获取歌词框（例如 `e1953`）、风格框（`e1976`）、歌曲标题框（`e2104`）以及创建按钮（`e299`）的引用。
5. `browser action=act kind=type ref=e1953 text="..."`（输入歌词）
6. `browser action=act kind=click ref=e299`（点击创建按钮）
7. `browser action=snapshot` → 查找新生成的歌曲行并点击播放按钮（`e2172`）。
8. `browser action=act kind=click ref=e2172`（播放歌曲）

## 注意事项

- **元素引用会变化：** 每次执行 `snapshot` 命令后，元素引用（如 `e123`）都会发生变化。因此，请在操作前务必先执行 `snapshot` 命令。
- **建议使用 v5 版本：** 为获得最佳效果，请确保选择 v5 版本的 OpenClaw。
- **自定义模式：** 可以切换到“自定义”模式来输入特定的歌词内容。