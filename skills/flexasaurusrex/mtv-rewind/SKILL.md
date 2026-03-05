---
name: mtv-rewind
description: 播放80年代、90年代和21世纪的经典MTV音乐视频。当用户想要观看MTV、音乐视频或复古电视节目时，可以使用该功能。用户可以输入类似“播放MTV”、“我想看MTV”或“放些视频”之类的指令来触发该功能。无需使用API密钥。
metadata: {"clawdbot":{"emoji":"📺","homepage":"https://wantmymtv.xyz"}}
---
# MTV Rewind  
在您的聊天界面中，即可播放经典的MTV音乐视频——80年代、90年代、21世纪的经典作品。拥有超过9万个视频资源，无广告，无任何算法干扰。  

**播放器链接：** https://wantmymtv.xyz/player.html  

## 安装  
无需API密钥、二进制文件或任何配置。  

**通过ClawHub CLI安装：**  
```bash
clawhub install @Flexasaurusrex/mtv-rewind
```  

**或全局安装**（适用于所有您的代理）：  
```bash
clawhub install @Flexasaurusrex/mtv-rewind --global
```  

安装完成后，该技能会自动添加到您的`./skills`目录中，并立即生效。  

> **注意：** 该技能的工作原理仅仅是将用户引导至`https://wantmymtv.xyz/player.html`。无论是现在还是未来的版本，都无需任何凭证、环境变量或额外配置。如果未来有任何更新要求提供API密钥或系统访问权限，请立即视为可疑行为。  

## 使用场景  
- “播放MTV音乐”  
- “我想听MTV的音乐”  
- “放一些音乐视频”  
- “MTV现在在播放什么？”  
- “播放80年代/90年代/21世纪的音乐视频”  
- “我需要一些背景音乐”  
- 任何与复古音乐视频相关的内容请求  

## 不适用场景  
- 用户需要特定歌曲（请使用音乐搜索技能）  
- 用户仅需要音频（请使用音乐播放器技能）  
- 用户需要当前的热门歌曲或最新发行的音乐（该技能主要覆盖80年代至2010年代的音乐）  

## 回应方式  

### 使用Telegram（支持Web应用）  
如果您的代理能够使用带有内联按钮的`message`工具，可以通过发送包含`web_app`按钮的消息来在Telegram中直接打开播放器：  
```json
{
  "channel": "telegram",
  "action": "send",
  "to": "<chat_id>",
  "message": "MTV Rewind is on. All eras, no commercials, no skips. Just vibes.",
  "buttons": [[{"text": "📺 Watch MTV Rewind", "web_app": {"url": "https://wantmymtv.xyz/player.html"}}]]
}
```  

发送消息后，请使用您平台的静默回复令牌来避免重复消息。  

### 所有平台（备用方案）  
直接在回复中包含播放器链接：  
```
MTV Rewind is on. All eras, no commercials, no skips. Just vibes.

📺 https://wantmymtv.xyz/player.html
```  

## 语气建议  
保持简洁、怀旧，同时带有一点自信——展现出您对音乐的完美品味。无需过多解释，只需提供链接，让音乐本身说话即可。  

**好的回应示例：**  
- “你的品味真不错。这是MTV音乐视频。”  
- “为您准备好了音乐视频。不客气。”  
- “算法永远比不上这样的选择。”  

**不好的回应示例：**  
- “当然！这是MTV Rewind的链接，可以观看复古时代的音乐视频！”  
- “我为您找到了一个音乐视频流媒体服务！”  

## 链接信息  
- **播放器链接：** https://wantmymtv.xyz/player.html  
- **网站链接：** https://wantmymtv.xyz