---
name: pixiv
description: 您可以通过 Pixiv 搜索插画、漫画，并查看排行榜。支持通过关键词进行搜索，同时可以查看每日/每周/每月的排行榜。
---

# Pixiv Skill

此技能允许用户搜索和浏览 Pixiv 上的插画。

## 设置

在使用之前，您必须拥有有效的 Pixiv 更新令牌（Refresh Token）。该令牌存储在技能目录下的 `config.json` 文件中。

配置方法如下：
1. 向用户索取他们的 Pixiv 更新令牌。
2. 运行以下命令：`node skills/pixiv/scripts/pixiv-cli.js login <REFRESH_TOKEN>`

## 使用方法

### 搜索插画

**按关键词搜索插画：**

```bash
node skills/pixiv/scripts/pixiv-cli.js search "KEYWORD" [PAGE]
```

示例：
```bash
node skills/pixiv/scripts/pixiv-cli.js search "miku" 1
```

返回一个包含插画详细信息的 JSON 数组（标题、网址、标签、作者等）。

### 查看排名

**查看插画排名：**

```bash
node skills/pixiv/scripts/pixiv-cli.js ranking [MODE] [PAGE]
```

可选模式：`day`（当天）、`week`（本周）、`month`（本月）、`day_male`（男性作者）、`day_female`（女性作者）、`week_original`（原创作者）、`week_rookie`（新注册用户）、`day_ai`（AI 生成的作品）。
默认模式为 `day`。

示例：
```bash
node skills/pixiv/scripts/pixiv-cli.js ranking day
```

### 查看用户资料

**查看用户资料：**

```bash
node skills/pixiv/scripts/pixiv-cli.js user <USER_ID>
```

示例：
```bash
node skills/pixiv/scripts/pixiv-cli.js user 11
```

### 查看当前登录用户的资料

**查看当前登录账户的资料：**

```bash
node skills/pixiv/scripts/pixiv-cli.js me
```

### 查看关注的用户

**查看当前登录账户关注的用户：**

```bash
node skills/pixiv/scripts/pixiv-cli.js following [PAGE]
```

### 查看关注用户的最新作品

**查看被关注用户的最新插画：**

```bash
node skills/pixiv/scripts/pixiv-cli.js feed [RESTRICT] [PAGE]
```

`RESTRICT` 参数可选值：`all`（全部）、`public`（公开）、`private`（私密）。默认值为 `all`。

### 下载插画

**下载插画：**

- 单张图片
- 漫画集
- 或者压缩文件（ugoira 格式）

```bash
node scripts/pixiv-cli.js download <ILLUST_ID>
```

下载后的文件将保存在 `downloads/<ILLUST_ID>/` 目录下。
返回一个包含已下载文件列表的 JSON 数据。

### 发布插画

**使用 AppAPI v2 直接在 Pixiv 上发布新插画（无需浏览器）：**

```bash
node scripts/pixiv-cli.js post <FILEPATH> "<TITLE>" "[TAGS_COMMA_SEPARATED]" [VISIBILITY]
```

- **可见性设置**：`public`（公开）、`login_only`（仅限登录用户查看）、`mypixiv`（仅限用户本人查看）或 `private`（私密）。
- 系统会自动为插画添加 AI 生成的标签（`illust_ai_type: 2`）。

示例：
```bash
node scripts/pixiv-cli.js post "./output.png" "My New Art" "Original, Girl, AI" private
```

## 如何获取令牌（针对用户）

如果用户询问如何获取令牌：
1. 建议他们搜索“Pixiv 更新令牌”，或使用像 `gppt` 这样的工具来获取令牌。
2. 或者让他们在浏览器中登录 Pixiv，然后在本地存储或 Cookie 中查找 `refresh_token`（不过 OAuth 更新令牌更为安全）。
3. 对于非技术用户来说，最简单的方法是使用辅助脚本来获取令牌，但本文档中未提供相关脚本。请让他们直接提供令牌即可。