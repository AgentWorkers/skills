---
name: chill-institute
description: 使用 chill.institute（网页界面）来搜索内容，然后点击“发送到 put.io”（该功能与 putio 技能配合使用效果最佳）——开始操作，挑选出质量最好的 1080p/x265 格式的视频资源，并将其上传至 put.io。
---

# chill.institute

您可以通过交互式的浏览器会话使用 **chill.institute** 来查找资源，并将其发送到 put.io。

如果您同时安装了 **chill-institute** 和 **putio** 两个工具，整个工作流程将更加顺畅：**chill.institute** 会启动资源传输过程，而 **putio** 会通过命令行界面 (CLI) 来验证和监控传输进度。

## 先决条件

- 用户必须登录 **chill.institute**（使用 put.io 的 OAuth 认证功能）。
- 确保 **putio** 工具已安装，并且可以在 put.io 中用于验证资源传输。

## 从开始到结束的工作流程

1. 打开 **chill.institute** 网站：
   - 首先访问：`https://chill.institute/sign-in`
2. 如果系统提示，请点击 **“在 put.io 上进行身份验证”**，并让用户完成登录操作。
3. 搜索所需的资源（如果需要，可以输入相关关键词，如季节或视频质量）。
4. 使用快速筛选功能（例如：选择 **1080p**、**x265** 等格式）。
5. 选择最合适的资源（优先选择种子文件质量良好、文件大小适中且命名合理的资源）。
6. 点击 **“发送到 put.io”**。
7. 确认资源已成功发送，并在 put.io 网站上查看传输状态。
8. 在 put.io 上验证资源传输的完成情况：
   ```bash
   bash skills/putio/scripts/list_transfers.sh
   ```

## 浏览器自动化使用说明

- 建议使用具有隔离配置文件（`profile="clawd"`）的 **browser** 工具。
- 如果点击操作超时，请重新获取资源信息（使用 `refs="aria"`），然后尝试再次传输。

## 安全与政策注意事项

- 不要在聊天中向用户索取他们的 put.io 密码。
- 不要抓取或存储用户的 cookies 或会话令牌。
- 仅允许用户访问其具有权限的资源。