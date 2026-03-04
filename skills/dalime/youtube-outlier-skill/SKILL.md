# youtube-outlier-skill

该技能能够根据特定主题关键词（niche）查找YouTube上的异常视频或热门视频，分析这些视频的主要内容，并将分析结果存储到Google Sheets中。同时，还会将分析摘要发布到Discord上。

## 支持的参数
- `niche`（单个关键词或用逗号分隔的关键词列表）

## 使用方式
可以通过Discord或API调用来使用该技能：

```
/ytoutlier AI news
```

## Discord命令注册
请将以下代码添加到您的Discord/OpenClaw配置文件中，或直接复制到您的技能配置文件中：

```yaml
commands:
  - name: ytoutlier
    description: Find trending YouTube outlier videos in a niche.
    usage: /ytoutlier <niche>
    handler: youtube-outlier-skill
```

## 所需条件
- Google Sheets API的访问权限（需要具有编辑目标工作表的权限）
- Discord机器人的Token和频道ID
- YouTube Data API密钥（如果该功能不由`youtube-api-skill`提供）

## 环境变量
请查看`.env.example`文件以获取所有所需的环境变量。

---

该技能由Soma 🧘‍♂️为Danny创建（使用OpenClaw开发）