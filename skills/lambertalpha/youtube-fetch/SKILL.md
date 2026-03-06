**名称：youtube-fetch**  
**描述：** 用于获取YouTube视频内容以进行摘要和分析。当用户分享YouTube链接或请求对视频进行摘要/分析时使用该功能。支持提取字幕（优先选择）；若字幕不存在，则自动切换为使用视频描述。  

## YouTube内容获取工具  

### 快速入门  
```bash
python3 scripts/youtube_fetch.py "https://www.youtube.com/watch?v=VIDEO_ID" --proxy socks5h://127.0.0.1:1080
```  

### 策略：**先尝试获取字幕，若无法获取则使用视频描述**  
1. **尝试通过`youtube-transcript-api`获取字幕**——这是最准确的逐字稿内容。  
2. **如果无法获取字幕**，则访问视频页面并从HTML元数据中提取视频描述。  
3. **务必告知用户数据来源**——仅使用视频描述时，需明确说明这不是完整的字幕内容。  

### 使用方法  
```bash
# Basic (with proxy for geo-blocked regions)
python3 scripts/youtube_fetch.py VIDEO_URL --proxy socks5h://127.0.0.1:1080

# Specify languages (default: zh-Hans,zh-Hant,zh,en)
python3 scripts/youtube_fetch.py VIDEO_URL --langs "en,ja" --proxy PROXY

# JSON output (includes source metadata)
python3 scripts/youtube_fetch.py VIDEO_URL --json --proxy PROXY

# Save to file
python3 scripts/youtube_fetch.py VIDEO_URL --output /tmp/transcript.txt --proxy PROXY
```  

### 所需依赖库  
- `youtube-transcript-api`（通过pip安装）：用于获取字幕  
- `requests`（通过pip安装）：用于在无法获取字幕时获取视频描述  
- 如果从被地理封锁的地区（如中国大陆）运行该工具，需要配置SOCKS5或HTTP代理：  
  - SOCKS5代理：`socks5h://127.0.0.1:1080`  
  - HTTP代理：`http://127.0.0.1:1081`  

**注意：** 使用居民区IP地址的代理。YouTube会屏蔽数据中心/云服务器的IP地址。使用居民区宽带IP（例如香港的家庭宽带）通常可以正常访问；VPS/云服务器的IP地址可能会被屏蔽。建议仅允许YouTube相关域名通过代理访问。  

### 在进行摘要时需要注意的事项：  
- **字幕来源**：可以直接使用字幕内容进行摘要，因为这是完整的音频内容。  
- **视频描述来源**：需告知用户这是创作者撰写的摘要，并非完整的视频内容；摘要的准确性和完整性取决于创作者对视频描述的详细程度。  
- 对于字幕长度超过50,000个字符的视频，建议将其分段后再进行摘要处理。