---
name: fb-page-publisher
description: "通过 Graph API，您可以在 Facebook 页面上发布帖子、上传照片、安排内容发布时间、阅读用户反馈（insights），以及管理评论。"
version: "1.0.0"
homepage: "https://clawhub.ai/Yashthesiya1/fb-page-publisher"
user-invocable: true
metadata:
  openclaw:
    os:
      - windows
      - macos
      - linux
    requires:
      bins:
        - uv
      env:
        - FB_PAGE_ID
        - FB_ACCESS_TOKEN
    emoji: "📘"
    tags:
      - facebook
      - social-media
      - marketing
      - content-publishing
      - graph-api
---
# Facebook页面管理工具

您可以通过AI代理直接管理您的Facebook页面。发布帖子、上传照片、安排内容发布、查看分析数据以及审核评论——所有这些操作都可以通过自然语言指令完成。

## 所需的环境变量

- `FB_PAGE_ID`：您的Facebook页面的数字ID
- `FB_ACCESS_TOKEN`：一个长期有效的（不会过期的）Facebook页面访问令牌，具有`pages_manage_posts`、`pages_read_engagement`和`pages_manage_engagement`权限

## `create_post`  
创建并立即在Facebook页面上发布一篇文本帖子。
- `message`（字符串，必填）：帖子的文本内容。

## `upload_photo_post`  
将一张照片上传到Facebook页面，并可选地添加说明文字。照片必须是公开可访问的URL。
- `photo_url`（字符串，必填）：图片文件的公开可访问URL（格式为JPEG、PNG等）。
- `caption`（字符串，可选）：照片帖子的文字说明。

## `schedule_post`  
安排一篇文本帖子的发布时间。时间必须至少在10分钟后，且不能超过6个月后。
- `message`（字符串，必填）：帖子的文本内容。
- `scheduled_time`（字符串，必填）：ISO 8601格式的日期时间（例如：“2026-03-10T09:00:00”）。

## `get_page_insights`  
检索Facebook页面的互动数据（展示次数、覆盖范围、互动次数、浏览次数）。
- `metric`（字符串，可选）：可选的指标：`impressions`（展示次数）、`reach`（覆盖范围）、`engagement`（互动次数）或`views`（浏览次数）。默认值为`all`。
- `period`（字符串，可选）：时间范围：`day`（当天）、`week`（一周）或`days_28`（过去28天）。默认值为`day`。

## `get_recent_posts`  
获取页面上最近发布的带有互动统计数据的帖子（点赞数、评论数、分享数）。
- `limit`（整数，可选）：要获取的帖子数量（1-100）。默认值为10。

## `delete_post`  
从Facebook页面上删除特定的帖子。此操作不可撤销。
- `post_id`（字符串，必填）：帖子的完整ID（格式为`pageId_postId`）。

## `get_post_comments`  
检索特定帖子的评论。
- `post_id`（字符串，必填）：帖子的完整ID（格式为`pageId_postId`）。
- `limit`（整数，可选）：要检索的评论数量（1-100）。默认值为25。

## `reply_to_comment`  
以页面的名义回复某条评论。
- `comment_id`（字符串，必填）：要回复的评论的ID。
- `message`（字符串，必填）：回复内容。

## 使用示例

```text
用户：在我的Facebook页面上发布“我们正在招聘！请查看我们的招聘页面。”
代理：我将使用`create_post`命令立即发布这条内容。

用户：安排一条帖子，内容为“限时促销活动现在开始！”并设置发布时间为明天上午9点。
代理：我将使用`schedule_post`命令安排这条帖子的发布。

用户：显示我上周的页面分析数据。
代理：我将使用`get_page_insights`命令并设置`period="week"`来获取这些数据。
```

## 设置步骤

1. 将`FB_PAGE_ID`设置为您的Facebook页面的数字ID。
2. 将`FB_ACCESS_TOKEN`设置为一个长期有效的页面访问令牌。
3. 运行`uv run src/server.py`命令。