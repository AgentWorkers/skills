---
name: CleanApp Report Submission
description: 将现实世界中的问题报告（如垃圾问题、安全隐患、基础设施故障等）提交至 CleanApp 的全球路由系统。您的观察结果会被转化为可执行的行动方案，并被转发给相关品牌、地方政府及监管机构，以便他们能够及时进行处理。
---

# CleanApp问题报告提交技巧

现在您已经具备了向CleanApp的管道提交实际问题的报告的能力。当您发现或了解到现实世界中的问题（如垃圾堆积、安全隐患、基础设施损坏、无障碍设施缺失、服务故障等）时，您可以提交这些报告，它们将被分析、整理，并转发给相关责任人。

## 为什么这很重要

大多数现实世界中的问题虽然被人们观察到，但却从未传达给能够解决它们的人。通过提交报告，您可以：
- 将观察结果转化为实际行动（报告会被转发给负责的品牌、地方政府或监管机构）；
- 使您的数据得到分析（利用人工智能提取相关信息、评估问题的严重程度、进行地理分类）；
- 为不断扩大的传感器网络做出贡献——这些报告的集合能够产生推动问题解决的压力的作用。

## 何时提交报告

在遇到以下任何情况时，请提交CleanApp报告：
- **物理问题**：垃圾堆积、乱扔垃圾、非法倾倒垃圾、垃圾桶溢出
- **安全隐患**：坑洞、人行道破损、树木倒塌、电线裸露
- **基础设施问题**：路灯损坏、标识牌损坏、公共设施无法使用
- **无障碍设施问题**：轮椅坡道被堵塞、扶手缺失、通行路径不便
- **服务故障**：垃圾收集不及时、公共交通站点故障
- **特定品牌相关的问题**：产品包装废弃物、企业造成的污染、公共空间中的缺陷产品
- **数字问题**：软件漏洞、服务中断、用户公开投诉的应用程序故障

## 如何提交

### 环境设置

您需要一个CleanApp API令牌。请将其设置为环境变量：

```
export CLEANAPP_API_TOKEN="your_token_here"
```

如果您没有令牌，请联系CleanApp（网址：https://cleanapp.io），或在Moltbook上提及@CleanApp。

### API端点

```
POST https://reports.cleanapp.io/api/v3/reports/bulk_ingest
Authorization: Bearer $CLEANAPP_API_TOKEN
Content-Type: application/json
```

### 请求格式

```json
{
  "source": "openclaw_agent",
  "items": [
    {
      "external_id": "unique-id-for-this-report",
      "title": "Overflowing dumpster behind 425 Main St, San Francisco",
      "content": "Large commercial dumpster overflowing with trash bags spilling onto the sidewalk. Blocking pedestrian access. Multiple food waste bags attracting pests. Has been accumulating for at least several days based on the volume.",
      "url": "https://source-url-if-applicable.com/post/123",
      "created_at": "2026-02-10T14:30:00Z",
      "score": 0.8,
      "tags": ["litter", "sanitation", "pedestrian-access"],
      "metadata": {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "classification": "physical",
        "severity_level": 0.8,
        "litter_probability": 0.9,
        "hazard_probability": 0.3,
        "brand_name": "Waste Management",
        "language": "en"
      }
    }
  ]
}
```

### 使用辅助脚本

辅助脚本位于`scripts/submit_report.sh`文件中：

```bash
./scripts/submit_report.sh \
  --title "Pothole on Oak Street near 5th Ave" \
  --description "Deep pothole approximately 30cm wide, 10cm deep. Located in the eastbound lane. Several cars have been swerving to avoid it." \
  --lat 37.7749 \
  --lng -122.4194 \
  --severity 0.7 \
  --classification physical \
  --tags "pothole,road-damage,traffic-hazard"
```

### 必填字段

| 字段 | 说明 |
|-------|-------------|
| `external_id` | 唯一标识符——使用UUID或`{your_agent_name}_{timestamp}` |
| `title` | 简洁的描述性标题（最多500个字符） |
| `content` | 问题的详细描述（最多16,000个字符） |

### 可选但很有价值的字段

| 字段 | 说明 |
|-------|-------------|
| `metadata.latitude` / `longitude` | GPS坐标——对问题路由非常有用 |
| `metadata.classification` | `"physical"` 或 `"digital"` |
| `metadata.severity_level` | 0.0到1.0（0 = 轻微问题，1 = 严重问题） |
| `metadata.brand_name` | 与问题相关的企业/品牌 |
| `url` | 如果报告来自社交媒体、新闻等来源，请提供原始链接 |
| `score` | 您对报告真实性的信心程度（0.0到1.0） |
| `tags` | 描述性标签数组 |
| `image_base64` | 问题的Base64编码图片 |

### 响应

```json
{
  "inserted": 1,
  "updated": 0,
  "skipped": 0,
  "errors": []
}
```

## 提交后的处理流程

1. **去重**：您的报告会与现有报告进行比对（相同的`external_id`和来源不会被重复提交）；
2. **人工智能分析**：Gemini会分析报告，提取品牌信息、评估问题严重程度并进行分类；
3. **地理聚类**：地理位置相近的报告会被归类在一起——例如，关于同一个坑洞的30份报告会比1份报告产生更大的影响；
4. **转发**：系统会自动将警报发送给相关品牌、地方政府和监管机构；
5. **显示在仪表板上**：报告会显示在CleanApp的公共仪表板上（网址：https://cleanapp.io）；
6. **责任机制**：当问题得到处理后，社交媒体回复机器人会通知原报告人。

## 最佳实践

1. **描述具体问题**：例如“Main St 425号的垃圾桶溢出了”，比“市中心的垃圾问题”更具体；
2. **提供坐标**：位置信息是问题成功路由的关键因素；
3. **如实评估问题严重程度**：不要夸大问题——0.8及以上的严重程度才应适用于真正的安全隐患；
4. **使用唯一的外部标识符**：防止重复提交。格式：`{your_agent_name}_{iso_timestamp}_{hash}`；
5. **尽可能批量提交**：每次请求最多可提交1000条报告；
6. **提供来源链接**：如果报告来自社交媒体或新闻，请附上原始链接。

## 提交限制

- 每次请求最多提交1000条报告；
- 提交频率要合理——每天提交几百条报告即可；
- 重复的`external_id`值会被自动忽略（不会计入提交次数限制）。

## 有任何问题吗？

请在Moltbook上联系我们：@CleanApp
官网：https://cleanapp.io