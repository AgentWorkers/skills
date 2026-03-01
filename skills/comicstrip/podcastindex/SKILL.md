**名称：Podcast Index**  
**描述：** 使用 Podcast Index API 访问和搜索播客信息，包括搜索播客、剧集以及获取详细信息。  
**主页：** https://podcastindex.org/api/docs  

**元数据：**  
```json
{
  "openclaw": {
    "requires": {
      "env": ["PODCASTINDEX_API_KEY", "PODCASTINDEX_API_SECRET"]
    },
    "primaryEnv": "PODCASTINDEX_API_KEY",
    "emoji": "🎙️"
  }
}
```

**功能说明：**  
该功能允许您通过 Podcast Index API 进行操作，例如搜索播客、获取播客及剧集的详细信息等。当用户请求播客推荐、剧集信息或与播客相关的搜索内容时，可以使用此功能。  

**先决条件：**  
- 确保 `PODCASTINDEX_API_KEY` 和 `PODCASTINDEX_API_SECRET` 已在环境变量或配置文件中设置。  
- 所有请求都必须使用特定的请求头进行身份验证。  
- 基础 URL：`https://api.podcastindex.org/api/1.0`  

**身份验证方式：**  
1. 获取当前的 Unix 时间戳：  
   ```javascript
   const unixTime = Math.floor(Date.now() / 1000);
   ```  
2. 计算 SHA-1 哈希值：  
   ```javascript
   const hash = crypto.createHash('sha1').update(PODCASTINDEX_API_KEY + PODCASTINDEX_API_SECRET + unixTime.toString()).digest('hex');
   ```  
3. 在每个请求中包含以下请求头：  
   ```javascript
   {
     "User-Agent": "OpenClaw/1.0"  // 或其他合适的标识符
     "X-Auth-Key": PODCASTINDEX_API_KEY
     "X-Auth-Date": unixTime
     "Authorization": hash
   }
   ```  

**常用 API 端点及使用方法：**  
- **按关键词搜索播客：**  
  ```javascript
  GET /search/byterm?q=[查询参数]  // 例如：/search/byterm?q=AI （搜索标题中包含“AI”的播客）
  ```  
- **按标题搜索播客：**  
  ```javascript
  GET /search/bytitle?q=[查询参数]  // 例如：/search/bytitle?q=人工智能
  ```  
- **按作者搜索剧集：**  
  ```javascript
  GET /search/byperson?q=[作者名称]
  ```  
- **通过 Feed ID 获取播客详情：**  
  ```javascript
  GET /podcasts/byfeedid?id=[feedId]
  ```  
- **通过 RSS Feed URL 获取播客详情：**  
  ```javascript
  GET /podcasts/byfeedurl?url=[编码后的 RSS Feed URL]
  ```  
- **获取特定 Feed 的剧集列表：**  
  ```javascript
  GET /episodes/byfeedid?id=[feedId]&max=10
  ```  
- **获取单集元数据：**  
  ```javascript
  GET /episodes/byid?id=[episodeId]
  ```  
- **获取热门播客：**  
  ```javascript
  GET /podcasts/trending?[cat=technology&max=10]
  ```  
- **获取最新发布的剧集：**  
  ```javascript
  GET /recent/episodes?max=10
  ```  

**注意事项：**  
- 必须解析 JSON 响应内容，并为用户提供相关信息。  
- 如果请求失败，请检查身份验证信息并重试。  
- 在测试期间，可以在 URL 后添加 `?pretty` 参数以获得更易读的输出格式。