---
name: facebook-page
description: 通过 Meta Graph API 管理 Facebook 页面。可以发布内容（文本、图片、链接），查看页面上的帖子，以及管理评论（列出、回复、隐藏或删除评论）。适用于用户需要向 Facebook 页面发布内容、查看页面帖子或处理评论的场景。
---

# Facebook页面管理技能

通过Meta Graph API管理Facebook页面的相关技能。

## 功能
- 列出用户管理的所有页面
- 发布帖子（文本、图片、链接）
- 查看页面的帖子列表
- 查看/回复/隐藏/删除评论

## 一次性的设置步骤

### 1. 创建Meta应用
1. 访问 https://developers.facebook.com/apps/ → 点击“Create App”
2. 选择“Other” → 根据实际需求选择“Business”或“Consumer”
3. 填写应用名称和电子邮件地址
4. 进入“App settings > Basic”，获取“App ID”和“App Secret”

### 2. 配置OAuth
1. 点击“Add Product”，然后添加“Facebook Login”
2. 在“Facebook Login > Settings”中：
   - 将“Valid OAuth Redirect URIs”留空（使用手动代码流程）
3. 进入“App Roles”，将用户添加为Admin/Developer角色

### 3. 配置.env文件
```bash
cd skills/facebook-page
cp .env.example .env
# Edit .env với App ID và Secret
```

### 4. 安装依赖并获取Token
```bash
cd scripts
npm install
node auth.js login
```
脚本会：
1. 输出一个URL，用户需要使用浏览器访问该URL进行登录并授权
2. 用户授权成功后，会得到一个包含`code=...`的URL
3. 将该URL粘贴到终端中
4. 脚本会使用该URL交换代码，以获取长期有效的Token（long-lived token）和页面Token（page token）
5. 将Token保存到`~/.config/fbpage/tokens.json`文件中

## 常用命令

### 列出页面
```bash
node cli.js pages
```

### 发布文本帖子
```bash
node cli.js post create --page PAGE_ID --message "Hello world"
```

### 发布带图片的帖子
```bash
node cli.js post create --page PAGE_ID --message "Caption" --photo /path/to/image.jpg
```

### 发布带链接的帖子
```bash
node cli.js post create --page PAGE_ID --message "Check this out" --link "https://example.com"
```

### 查看帖子列表
```bash
node cli.js post list --page PAGE_ID --limit 10
```

### 查看帖子的评论列表
```bash
node cli.js comments list --post POST_ID
```

### 回复评论
```bash
node cli.js comments reply --comment COMMENT_ID --message "Thanks!"
```

### 隐藏评论
```bash
node cli.js comments hide --comment COMMENT_ID
```

### 删除评论
```bash
node cli.js comments delete --comment COMMENT_ID
```

## 所需的权限
- `pages_show_list`：列出页面
- `pages_read_engagement`：读取帖子和评论
- `pages_manage_posts`：发布/编辑/删除帖子
- `pages_manage_engagement`：管理评论

## 注意事项
- 如果使用长期有效的用户Token（long-lived user token）获取的Token是永久有效的
- 请勿将Token输出到控制台或日志中
- 应用处于测试模式（Testing mode）时，仅对具有管理员/开发者角色的用户有效