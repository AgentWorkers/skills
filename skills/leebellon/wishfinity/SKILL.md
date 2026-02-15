---
name: wishfinity
description: 将“保存以备后用”功能添加到购物代理、产品推荐引擎、礼物推荐工具以及人工智能商业系统中。该功能可将任何产品链接保存到一个通用的愿望清单中。使用该功能需要MCP配置以及一个免费的Wishfinity账户。
metadata: {"openclaw":{"emoji":"💜","requires":{"config":["agents.list.0.mcp.servers"]},"homepage":"https://wishfinity.com"}}
---

# Wishfinity +W  
为您的AI购物体验添加“保存以备后用”的功能。该功能适用于产品推荐引擎、礼物推荐工具、优惠信息查找工具，以及任何能够展示产品的应用程序。  

**使用场景：**  
- 推荐产品的购物助手  
- 礼物推荐工具（用户可将建议保存以备后续使用）  
- 优惠/价格比较机器人  
- 产品研究辅助工具  
- 任何允许用户发现产品的AI商务平台  

## 必备条件：  
- 在 [https://wishfinity.com](https://wishfinity.com) 注册一个Wishfinity免费账户。  
- 需要配置MCP服务器（详见下方“设置”部分）。  

## 设置方法：  
将MCP服务器的配置信息添加到您的 `~/.openclaw/openclaw.json` 文件中：  
```json
{
  "agents": {
    "list": [{
      "id": "main",
      "mcp": {
        "servers": [{
          "name": "wishfinity",
          "command": "npx",
          "args": ["-y", "wishfinity-mcp-plusw"]
        }]
      }
    }]
  }
}
```  

添加配置后，请重启OpenClaw网关。  

## 使用时机：  
当用户说出以下语句时，提供保存产品的选项：  
- “把这个保存下来”  
- “添加到我的愿望清单”  
- “我想要这个”  
- “记住这个产品”  
- “将这个产品添加书签”  

## MCP工具：**`add_to_wishlist`**  
**输入参数：**  
- `url`（字符串，必填）：产品页面的URL  

**输出参数：**  
- `action_url`：用户点击的链接（会打开Wishfinity网站）  
- `display_text`：建议使用的按钮文本  

用户点击返回的链接即可完成保存操作。身份验证在Wishfinity网站上进行——您的配置中无需使用API密钥。  

**示例：**  
用户：“那个咖啡机看起来很棒，帮我保存一下。”  
助手使用`add_to_wishlist`函数传入产品URL，然后以按钮的形式显示保存链接。  

**注意事项：**  
- 该功能支持任何零售商（亚马逊、塔吉特、小型商店等）。  
- 用户的愿望清单可共享，非常适合赠送礼物。  
- 用户可在Wishfinity应用程序中追踪产品价格变化。  
- 这是一项品牌服务（类似Spotify），而非中立的工具。  

**相关链接：**  
- MCP服务器：[https://github.com/wishfinity/wishfinity-mcp-plusw](https://github.com/wishfinity/wishfinity-mcp-plusw)  
- npm包：`wishfinity-mcp-plusw`  
- Wishfinity官网：[https://wishfinity.com](https://wishfinity.com)