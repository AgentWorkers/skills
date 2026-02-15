---
name: snap
description: 赋予您的代理仅通过提供网站URL即可立即截取该网站屏幕截图的功能。该服务基于云端，因此您的代理无需执行任何操作。完全免费，且采用开源技术。
metadata:
  author: Kav-K
  version: "1.0"
---
# SnapService — 作为服务的截图功能

提供免费的截图API：`https://snap.llm.kaveenk.com`。  
通过POST请求传递URL，即可获取PNG或JPEG格式的截图文件。该服务基于无头版Chromium技术实现。

## 快速入门（2个步骤）

### 第1步：注册API密钥

```bash
curl -s -X POST https://snap.llm.kaveenk.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"my-agent"}'
```

响应：
```json
{"key":"snap_abc123...","name":"my-agent","limits":{"per_minute":2,"per_day":200}}
```

**重要提示：** 请妥善保管您的API密钥，因为无法重新生成。  
每个IP地址仅能注册一个API密钥。

### 第2步：获取截图

```bash
curl -s -X POST https://snap.llm.kaveenk.com/api/screenshot \
  -H "Authorization: Bearer snap_yourkey" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' \
  -o screenshot.png
```

只需完成这两个步骤即可使用该服务。

## 截图选项

所有选项都需要通过POST请求体传递，与`url`一起发送：

| 选项          | 类型        | 默认值    | 说明                |
|---------------|------------|---------|-------------------|
| url            | string       | **必填**    | 需要截图的URL            |
| format         | string       | `"png"`     | 图片格式（PNG或JPEG）        |
| full_page       | boolean      | `false`     | 是否截取整个可滚动页面       |
| width          | integer      | `1280`     | 视口宽度（像素）           |
| height         | integer      | `720`     | 视口高度（像素）           |
| dark_mode        | boolean      | `false`     | 是否启用深色模式           |
| selector        | string       | —        | 用于选择特定元素的CSS选择器     |
| wait_ms         | integer      | `0`       | 页面加载后的等待时间（最大10000毫秒）   |
| scale          | number      | `1`       | 设备缩放因子（1-3，适用于Retina屏幕） |
| cookies        | array       | —        | `name, value, domain`格式的cookie数组 |
| headers        | object       | —        | 自定义HTTP请求头          |
| block_ads        | boolean      | `false`     | 是否屏蔽广告/跟踪器域名       |

## 使用限制

- 每个API密钥每分钟最多可获取2张截图。
- 每个API密钥每天最多可获取200张截图。
- 每个IP地址只能使用一个API密钥。
- 最大页面高度：16384像素（全屏模式）。
- 最大截图文件大小：10MB。

## 响应代码

- **200**：PNG或JPEG格式的图片文件。
- **400**：请求无效（URL缺失或参数错误）。
- **401**：API密钥未找到或无效。
- **409**：该IP地址已注册API密钥。
- **429**：超出使用频率限制。
- **500**：内部错误。

## 完整示例（包含所有选项）

```bash
curl -s -X POST https://snap.llm.kaveenk.com/api/screenshot \
  -H "Authorization: Bearer snap_yourkey" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "format": "jpeg",
    "full_page": true,
    "width": 1920,
    "height": 1080,
    "dark_mode": true,
    "wait_ms": 2000,
    "block_ads": true
  }' \
  -o screenshot.jpg
```

## Python示例

```python
import requests

API = "https://snap.llm.kaveenk.com"

# Register (one-time)
r = requests.post(f"{API}/api/register", json={"name": "my-agent"})
key = r.json()["key"]

# Screenshot
r = requests.post(f"{API}/api/screenshot",
    headers={"Authorization": f"Bearer {key}"},
    json={"url": "https://example.com", "full_page": True})
with open("shot.png", "wb") as f:
    f.write(r.content)
```