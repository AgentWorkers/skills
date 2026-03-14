---
name: linkedin-management
description: 该工具通过利用浏览器捕获的会话cookie以及网络请求数据，自动化执行在LinkedIn上的各种操作，包括发布内容、编辑帖子、删除帖子以及对帖子进行评论等。
---
# LinkedIn管理技能

该技能允许代理通过拦截LinkedIn的内部API请求（Voyager和SDUI），并使用Python的`requests`库来模拟这些请求，从而实现与LinkedIn的自动化交互。

## 何时使用此技能
当您需要以编程方式执行以下操作时，请使用此技能：
- 在LinkedIn上创建文本或图片帖子。
- 编辑现有帖子。
- 删除帖子。
- 对帖子做出反应（点赞、庆祝、支持、喜爱、表示赞同或评论）。
- 在帖子下发表评论。

## 工作原理
LinkedIn结合使用了GraphQL（Voyager）和Server-Driven UI（SDUI）端点。身份验证主要通过cookies（`li_at`、`JSESSIONID`）和请求头来完成。

**重要提示**：此技能使用占位符来表示所有会话数据。您**必须**提供自己的`linkedin_cookies.json`文件以及特定于会话的请求头。

### 收集Cookies和会话数据
要使用此技能，您需要手动收集以下数据：
1. **Cookies**：使用Chrome扩展程序（如“Cookie-Editor”）或DevTools的应用程序选项卡来导出`li_at`和`JSESSIONID`。使用提供的模板将这些数据保存到`linkedin_cookies.json`文件中。
2. **会话请求头**：在执行LinkedIn操作时，使用随附的`advanced-network-capture`扩展程序来获取`x-li-page-instance`值。请将此值更新到`li_interact.py`文件中。

## 包含的脚本

脚本位于`scripts/`目录中：

### 1. `capture_session.py`
使用Playwright打开LinkedIn会话，允许用户手动登录并执行操作。该脚本会捕获Cookies和网络日志。
**使用方法：**
```bash
python scripts/capture_session.py
```

### 2. `li_interact.py`
这是一个全面的工具类`LinkedInBot`，用于处理自动化操作。
**支持的操作：**
- `create_post(text, media_urn=None)`：创建帖子
- `edit_post(share_urn, activity_id, text)`：编辑帖子
- `delete_post(activity_id)`：删除帖子
- `react_to_post(activity_id, reaction_type)`：对帖子做出反应
- `create_comment(activity_id, text)`：在帖子下发表评论
- `upload_image(image_path)`：上传图片

**通过Python使用方法：**
```python
from scripts.li_interact import LinkedInBot

bot = LinkedInBot(cookies_file="linkedin_cookies.json")
bot.create_post("Hello from automated LinkedIn bot!")
```

## 设置要求
- Python版本 >= 3.10
- 需要安装的包：`requests`、`playwright`
- 必须提供`li_at`和`JSESSIONID` Cookies。

> [!警告！]
> LinkedIn对自动化操作有严格的规定。请谨慎使用此技能，并避免频繁进行自动化操作，以防账户被暂停。