---
name: snaprender
description: 让你的代理能够“看”到网络上的内容：直观地查看任何网站，分析页面布局，比较不同设备上的显示效果，监控页面的变化，并生成可视化报告。
metadata: {"openclaw": {"requires": {"bins": ["curl"], "env": ["SNAPRENDER_API_KEY"]}}}
---
# SnapRender：让你的智能助手“看”到网页内容

你可以查看任何网站。当用户要求你查看某个页面、检查页面布局、分析设计、监控页面动态或进行任何形式的网页视觉分析时，可以使用 SnapRender 来捕捉该页面的图像，并利用你的视觉处理能力对其进行分析。

## 使用方法

使用 bash 和 curl 命令：

```bash
curl -s "https://app.snap-render.com/v1/screenshot?url=URL&response_type=json&block_ads=true&block_cookie_banners=true" \
  -H "X-API-Key: $SNAPRENDER_API_KEY"
```

请将 `URL` 替换为你要查看的目标网址（必须包含 `https://`）。

响应结果将以 JSON 格式返回，其中包含一个 `image` 字段，该字段包含一个 Base64 编码的图像数据 URI。将这个图像数据传递给你的视觉处理系统，以便进行查看和分析。

## 参数设置

| 参数            | 可选值            | 默认值            | 作用                                      |
|-----------------|------------------|------------------|----------------------------------------|
| url             | 任意公共网址           | 必填             | 要查看的网页地址                               |
| format           | png, jpeg, webp, pdf       | png             | 输出图像格式                               |
| device          | iphone_14, iphone_15_pro, pixel_7, ipad_pro, macbook_pro | desktop           | 以指定设备显示页面                         |
| dark_mode         | true, false           | false             | 显示页面的暗黑模式版本                         |
| full_page         | true, false           | false             | 显示整个可滚动页面                         |
| block_ads         | true, false           | true             | 隐藏广告以获得更清晰的视图                         |
| block_cookie_banners | true, false           | true             | 隐藏 cookie 弹窗                             |
| response_type     | json             | json             | 始终使用 JSON 格式返回响应                   |
| width            | 320-3840             | 1280             | 视口宽度                               |
| height           | 200-10000             | 800             | 视口高度                               |
| quality          | 1-100             | 90               | 图像质量（JPEG/WebP）                           |
| delay            | 0-10000             | 0               | 页面加载后的延迟时间（毫秒）                         |

## 可以实现的功能

- **查看任意网站**：例如：“stripe.com 是什么样子的？”“显示 competitor.com 的首页”
- **检查移动设备布局**：使用 `device=iphone_15_pro` 或 `device=pixel_7` 来查看页面在手机上的显示效果
- **比较不同设备上的显示效果**：分别调用该接口获取桌面和移动设备的页面数据，然后进行对比
- **比较暗黑模式和正常模式**：通过设置 `dark_mode=true` 和 `dark_mode=false` 来获取两种模式的页面显示效果
- **查看完整页面内容**：使用 `full_page=true` 来查看页面的所有内容
- **视觉质量检查**：检查页面是否显示异常、元素是否对齐正确、文本是否可读
- **监控页面变化**：捕捉页面变化并记录观察结果，与之前的记录进行对比
- **分析网站设计**：研究竞争对手的页面布局、价格展示方式等

## 使用说明

1. 为了进行视觉分析，请务必使用 `response_type=json` 以获取 Base64 编码的图像数据。
2. 收到截图后，请仔细观察图像并详细描述你所看到的内容。
3. 在进行对比时，需要分别调用该接口并分析每张截图。
3. 该工具默认会屏蔽广告和 cookie 弹窗，因此你将看到页面的实际内容。

## 获取 API 密钥

请访问 [https://app.snap-render.com/auth/signup](https://app.snap-render.com/auth/signup) 免费注册（每月可获取 50 张免费截图，无需信用卡）。