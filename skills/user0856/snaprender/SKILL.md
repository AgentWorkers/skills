---
name: snaprender
description: "让你的代理“看”遍整个网络——将任何 URL 作为图像文件截图。支持设备模拟（iPhone、iPad、Pixel、MacBook）、暗黑模式、全页滚动以及广告拦截功能。使用 `curl` 和 `exec` 工具进行操作（绝不要使用浏览器自身的截图功能）。`$SNAPRENDER_API_KEY` 已经预先设置好了。具体使用方法请参见下方说明。"
metadata: {"openclaw": {"requires": {"bins": ["curl", "jq"], "env": ["SNAPRENDER_API_KEY"]}}}
---
# SnapRender — 为您的代理程序提供“视觉”功能

您的代理程序可以浏览网页，但无法“看到”实际的内容。只需一个命令，它就能在几秒钟内捕获到任何网站、任何设备上的高精度截图。

“获取stripe.com在iPhone上的截图”、“比较桌面和移动端的显示效果”、“捕获全屏的暗黑模式画面”——一切都可以轻松实现。

**免费 tier：**每月500张截图，无需信用卡。[获取 API 密钥 →](https://snap-render.com/auth/signup)

---

**重要提示：**请使用 `exec` 工具配合 `curl` 来执行截图操作。**绝对不要使用 `browser` 工具来获取截图。**

## 捕获截图的方法

通过 `exec` 工具运行以下命令。将 `ENCODED_URL` 替换为经过 URL 编码的目标网址（例如：`https%3A%2F%2Fstripe.com`）：

```bash
curl -s "https://app.snap-render.com/v1/screenshot?url=ENCODED_URL&response_type=json&format=jpeg&quality=60&block_ads=true&block_cookie_banners=true" \
  -H "X-API-Key: $SNAPRENDER_API_KEY" \
  | tee /tmp/snap_response.json \
  | jq -r '.image' | sed 's|data:image/[^;]*;base64,||' | base64 -d > /tmp/screenshot.jpg \
  && jq '{url, format, size, cache, responseTime, remainingCredits}' /tmp/snap_response.json
```

该命令会将截图保存到 `/tmp/screenshot.jpg` 文件中，并同时输出元数据。

## 使用规则

1. **仅使用 `exec` 工具**，切勿使用 `browser` 工具。
2. **`$SNAPRENDER_API_KEY` 已经设置好**，请直接在命令中使用该密钥，切勿替换。
3. **对目标网址进行 URL 编码**（例如：`https://stripe.com` 应编码为 `https%3A%2F%2Fstripe.com`）。
4. **务必使用 `format=jpeg&quality=60`**，以确保截图文件大小适中，便于代理程序处理。
5. **务必将截图内容通过管道（pipe）保存到文件中**，因为 Base64 编码后的截图文件体积过大，无法直接在页面上显示。
6. **向用户报告截图的元数据**，包括文件大小、获取时间、缓存状态以及剩余的截图次数。

## 参数设置

您可以通过在 URL 中添加查询参数来调整截图的配置：

| 参数          | 值           | 默认值       |
|---------------|--------------|-----------|
| url            | 经过 URL 编码的目标网址 | 必填       |
| response_type     | json          | json        |
| format          | jpeg, png, webp, pdf     | jpeg       |
| quality         | 1-100          | 60         |
| device         | iphone_14, iphone_15_pro, pixel_7, ipad_pro, macbook_pro | desktop     |
| dark_mode        | true, false       | false        |
| full_page        | true, false       | false        |
| block_ads        | true, false       | true        |
| block_cookie_banners | true, false       | true        |
| width           | 320-3840         | 1280        |
| height          | 200-10000        | 800        |
| delay           | 0-10000         | 0          | （页面加载后的等待时间，单位：毫秒） |
| cache           | true, false       | true        | （设置为 false 可强制重新捕获） |
| cache_ttl        | 0-2592000        | 86400       | （缓存时间，上限受计划限制） |
| hide_selectors     | CSS 选择器       | none        | （逗号分隔，用于隐藏截图前的元素） |
| click_selector     | CSS 选择器       | none        | （点击指定元素后再进行截图） |
| user_agent       | 字符串         | 默认为 Chrome 用户代理 |

## 示例

- **获取 stripe.com 的桌面截图**：
  ```bash
curl -s "https://app.snap-render.com/v1/screenshot?url=https%3A%2F%2Fstripe.com&response_type=json&format=jpeg&quality=60&block_ads=true&block_cookie_banners=true" -H "X-API-Key: $SNAPRENDER_API_KEY" | tee /tmp/snap_response.json | jq -r '.image' | sed 's|data:image/[^;]*;base64,||' | base64 -d > /tmp/screenshot.jpg && jq '{url, format, size, cache, responseTime, remainingCredits}' /tmp/snap_response.json
```

- **获取移动设备（iPhone 15 Pro）的截图**：在 URL 中添加 `&device=iphone_15_pro`。
- **获取可滚动页面的截图**：在 URL 中添加 `&full_page=true`。
- **获取暗黑模式下的截图**：在 URL 中添加 `&dark_mode=true`。
- **比较桌面和移动端的显示效果**：分别执行两次截图操作，将结果保存为 `/tmp/screenshot_desktop.jpg` 和 `/tmp/screenshot_mobile.jpg`。

## 捕获截图后的操作

1. 告知用户截图已保存在 `/tmp/screenshot.jpg` 文件中（或您指定的文件路径）。
2. 向用户报告截图的元数据：文件大小、获取时间、缓存状态以及剩余的截图次数。
- 如果需要比较不同设备或模式的显示效果，请将截图保存为不同的文件名。

## 可能出现的错误

- **401**：API 密钥无效——请检查 `SNAPRENDER_API_KEY` 是否正确。
- **429**：达到使用频率限制或超出配额——请等待或升级套餐。
- **Timeout**：目标网站响应缓慢——可以在 URL 中添加 `&delay=3000` 以延长等待时间。
- **Empty response**：目标网址无法访问或被屏蔽。

## 获取 API 密钥

免费获取方式：[https://snap-render.com/auth/signup](https://snap-render.com/auth/signup)——每月 500 张截图，无需信用卡。