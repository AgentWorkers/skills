---
name: baoyu-post-to-x
description: 将内容及文章发布到 X（Twitter）。支持发布带有图片/视频的普通帖子，以及采用长格式 Markdown 编写的 X 文章（X Articles）。使用真实的 Chrome 浏览器，并结合 CDP（Chrome Data Platform）来规避反自动化检测机制。适用于用户要求“发布到 X”、“在 Twitter 上发推文”或“在 X 上分享”的场景。
---

# 在 X（Twitter）上发布内容

您可以使用真实的 Chrome 浏览器在 X（Twitter）上发布文本、图片、视频和长篇文章（绕过反机器人检测机制）。

## 脚本目录

**重要提示**：所有脚本都位于该技能的 `scripts/` 子目录中。

**代理执行说明**：
1. 将此 SKILL.md 文件所在的目录路径设置为 `SKILL_DIR`。
2. 脚本路径的格式为：`${SKILL_DIR}/scripts/<脚本名称>.ts`。
3. 请将文档中的所有 `${SKILL_DIR}` 替换为实际的路径。

**脚本参考**：
| 脚本          | 功能                |
|---------------|-------------------|
| `scripts/x-browser.ts` | 发布普通帖子（文本 + 图片）       |
| `scripts/x-video.ts` | 发布视频帖子（文本 + 视频）       |
| `scripts/x-quote.ts` | 引用推文并添加评论           |
| `scripts/x-article.ts` | 发布长篇 Markdown 文章       |
| `scripts/md-to-html.ts` | 将 Markdown 转换为 HTML         |
| `scripts/copy-to-clipboard.ts` | 将内容复制到剪贴板           |
| `scripts/paste-from-clipboard.ts` | 执行实际的粘贴操作           |

## 预设设置（EXTEND.md）

使用 Bash 命令检查 EXTEND.md 文件是否存在（优先级顺序如下）：

```bash
# Check project-level first
test -f .baoyu-skills/baoyu-post-to-x/EXTEND.md && echo "project"

# Then user-level (cross-platform: $HOME works on macOS/Linux/WSL)
test -f "$HOME/.baoyu-skills/baoyu-post-to-x/EXTEND.md" && echo "user"
```

┌──────────────────────────────────────────────────┬───────────────────┐
│                       路径                        │          位置                │
├──────────────────────────────────────────────────┼───────────────────┤
│ .baoyu-skills/baoyu-post-to-x/EXTEND.md          │ 项目目录              │
├──────────────────────────────────────────────────┼───────────────────┤
│ $HOME/.baoyu-skills/baoyu-post-to-x/EXTEND.md    │ 用户主目录              │
└──────────────────────────────────────────────────┴───────────────────┘

┌───────────┬───────────────────────────────────────────────────────────────────┐
│                结果                        |                      执行操作                │
├───────────┼───────────────────────────────────────────────────────────┤
│                找到                     | 读取、解析并应用预设设置        │
├───────────┼───────────────────────────────────────────────────────────┤
│                未找到                     | 使用默认设置            │
└───────────┴───────────────────────────────────────────────────────────┘

**EXTEND.md 支持的设置**：
- 默认 Chrome 配置文件
- 自动提交功能

## 先决条件**

- Google Chrome 或 Chromium 浏览器
- `bun` 运行时环境
- 首次使用前需手动登录 X（会保存会话）

## 参考资料**

- **普通帖子**：请参阅 `references/regular-posts.md` 以获取手动操作流程、故障排除方法和技术细节。
- **X 文章**：请参阅 `references/articles.md` 以获取长篇文章的发布指南。

---

## 发布普通帖子

可以发布文本以及最多 4 张图片。

```bash
npx -y bun ${SKILL_DIR}/scripts/x-browser.ts "Hello!" --image ./photo.png          # Preview
npx -y bun ${SKILL_DIR}/scripts/x-browser.ts "Hello!" --image ./photo.png --submit  # Post
```

**参数**：
| 参数            | 描述                        |
|-----------------|---------------------------|
| `<text>`          | 发布内容                      |
| `--image <路径>`       | 图片文件路径（可重复使用，最多 4 张）     |
| `--submit`        | 发布内容（默认为预览模式）          |
| `--profile <目录>`     | 自定义 Chrome 配置文件路径         |

---

## 发布视频帖子

可以发布文本和视频文件。

```bash
npx -y bun ${SKILL_DIR}/scripts/x-video.ts "Check this out!" --video ./clip.mp4          # Preview
npx -y bun ${SKILL_DIR}/scripts/x-video.ts "Amazing content" --video ./demo.mp4 --submit  # Post
```

**参数**：
| 参数            | 描述                        |
|-----------------|---------------------------|
| `<text>`          | 发布内容                      |
| `--video <路径>`       | 视频文件路径（MP4、MOV、WebM 格式）     |
| `--submit`        | 发布内容（默认为预览模式）          |
| `--profile <目录>`     | 自定义 Chrome 配置文件路径         |

**限制**：
- 普通帖子时长限制为 140 秒；
- 高级账户支持发布时长长达 60 分钟；
- 处理时间约为 30-60 秒。

---

## 引用推文并添加评论

可以引用现有的推文并添加评论。

```bash
npx -y bun ${SKILL_DIR}/scripts/x-quote.ts https://x.com/user/status/123 "Great insight!"          # Preview
npx -y bun ${SKILL_DIR}/scripts/x-quote.ts https://x.com/user/status/123 "I agree!" --submit       # Post
```

**参数**：
| 参数            | 描述                        |
|-----------------|---------------------------|
| `<tweet-url>`       | 要引用的推文链接                |
| `<comment>`        | 评论内容（可选）                   |
| `--submit`        | 发布内容（默认为预览模式）          |
| `--profile <目录>`     | 自定义 Chrome 配置文件路径         |

---

## 发布长篇 Markdown 文章

需要 X 的高级账户才能使用此功能。

```bash
npx -y bun ${SKILL_DIR}/scripts/x-article.ts article.md                        # Preview
npx -y bun ${SKILL_DIR}/scripts/x-article.ts article.md --cover ./cover.jpg    # With cover
npx -y bun ${SKILL_DIR}/scripts/x-article.ts article.md --submit               # Publish
```

**参数**：
| 参数            | 描述                        |
|-----------------|---------------------------|
| `<markdown>`       | Markdown 文件内容                |
| `--cover <路径>`       | 封面图片路径                   |
| `--title <文本>`       | 自定义标题                     |
| `--submit`        | 发布内容（默认为预览模式）          |

**前置内容**：支持在 YAML 格式的前置内容中设置 `title` 和 `cover_image`。

---

**注意事项**

- 首次使用前需手动登录 X（会保存会话）。
- 发布前务必预览内容。
- 支持跨平台使用：macOS、Linux、Windows。

## 扩展功能支持

通过 EXTEND.md 文件进行自定义配置。具体路径和可用选项请参阅 **预设设置** 部分。