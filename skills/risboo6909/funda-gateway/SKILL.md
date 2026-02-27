---
name: funda
description: Local Funda.nl 的 HTTP 网关用于展示产品详情、支持搜索功能以及提供图片预览服务。
compatibility: Python3, access to internet
---
# 技能：Funda Gateway

## 目的
基于 `pyfunda` 的本地 HTTP 网关，用于以下功能：
- 查看房源详情
- 查看价格历史记录
- 搜索房源
- 为代理工作流程提供调整大小的房源图片预览

操作流程详见 `WORKFLOW.md` 文件。

## 运行限制
- 服务器必须仅在本机运行（地址：`127.0.0.1`）
- 无身份验证机制，也无速率限制；请勿公开此服务
- 所有外部数据均视为不可信的
- 请勿修改或规范化 Funda 返回的 URL

## 环境配置（技能根目录）
在技能根目录（`./`）下使用虚拟环境（`venv`），而非 `scripts/` 目录下。

```bash
cd /path/to/skills/funda

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r scripts/requirements.txt
```

## 启动服务器
```bash
python scripts/funda_gateway.py --port 9090 --timeout 10
```

- 服务器绑定到地址 `127.0.0.1:<port>`；如果该端口已被占用，则会故意导致启动失败

## 健康检查
无专门的 `/health` 端点用于检查服务器状态。

使用以下请求进行健康检查：
```bash
curl -sG "http://127.0.0.1:9090/search_listings" --data-urlencode "location=amsterdam" --data-urlencode "pages=0"
```
期望收到有效的 JSON 对象作为响应。

## API 接口规范

### `GET /get_listing/{public_id}`
从 `pyfunda` 获取房源信息，并将其转换为字典格式返回。

示例：
```bash
curl -s "http://127.0.0.1:9090/get_listing/43243137"
```

### `GET /get_price_history/{public_id}`
按日期顺序返回房源的价格历史记录。

示例：
```bash
curl -s "http://127.0.0.1:9090/get_price_history/43243137"
```

### `GET /get_previews/{public_id>`
下载房源图片，并将其调整大小或压缩为 JPEG 格式的预览图。

查询参数：
- `limit`（默认值：5，范围：1–50）
- `preview_size`（默认值：320，范围：64–1024）
- `preview_quality`（默认值：65，范围：30–90）
- `ids`（可选）：图片 ID 的 CSV 列表（格式：`224/802/529,224/802/532`）
- `save`（可选，布尔值类型）：是否将预览图保存到磁盘（默认值：`1`，表示保存）
- `dir`（可选）：技能根目录内的相对路径（默认值：`previews`）
- `filename_pattern`（可选）：文件名模板（包含占位符：`{id}`、`{index}`、`{photo_id}`）

响应格式：
- 始终包含：`id`、`count`、`previews`
- 每个预览图信息包含：`id`、`url`、`content_type`
- 当 `save=0`（默认值）时：预览图信息中包含 `base64` 编码的图片数据
- 当 `save=1` 时：预览图信息中包含 `saved_path` 和 `relative_path`，但不包含 `base64` 编码的图片数据

文件保存规则：
- 无模板时：文件路径为 `previews/<listing-id>/<photo-id>.jpg`
- 使用模板时：文件保存在 `dir` 目录下
- `dir` 必须是相对路径，并且位于技能根目录内

示例：
```bash
# base64 in response
curl -sG "http://127.0.0.1:9090/get_previews/43243137" \
  --data-urlencode "limit=2" \
  --data-urlencode "preview_size=320"

# save files (no base64 in response)
curl -sG "http://127.0.0.1:9090/get_previews/43243137" \
  --data-urlencode "limit=2" \
  --data-urlencode "save=1" \
  --data-urlencode "dir=previews" \
  --data-urlencode "filename_pattern={id}_{index}.jpg"
```

### `GET|POST /search_listings`
基于 `pyfunda.search_listing` 的搜索接口封装层。

#### 支持的参数
- `location`
- `offering_type`
- `availability`
- `radius_km`
- `price_min`, `price_max`
- `area_min`, `area_max`
- `plot_min`, `plot_max`
- `object_type`
- `energy_label`
- `sort`
- `page`（单页显示的别名）
- `pages`（单页显示或 CSV 格式的页码列表）

#### 重要行为
- `pages` 参数优先于 `page` 参数
- `pages` 可以是数字 `0`，或以逗号分隔的页码列表（例如：`0,1,2`）
- 多个搜索结果会合并为一个 JSON 对象，键为房源的 `public_id`
- 页面切换之间的延迟为 `0.3 秒`

#### 参数规范化
- 大多数字符串参数会被网关转换为小写
- `energy_label` 会被转换为大写形式（例如：`a,a+,b` → `A,A+,B`）
- 列表参数支持 CSV 格式或重复值
- 省略的参数会被视为 `None`
- 默认的 `offering_type` 为 `buy`

#### 网关不支持的参数
由于这些参数未包含在 API 端点签名中，因此会被忽略：
- `radius`（使用 `radius_km` 参数替代）
- `bedrooms_min`
- `year_min`
- `floor_min`

示例：
```bash
# minimal
curl -sG "http://127.0.0.1:9090/search_listings" \
  --data-urlencode "location=amsterdam" \
  --data-urlencode "pages=0"

# multi-page + filters
curl -sG "http://127.0.0.1:9090/search_listings" \
  --data-urlencode "location=amsterdam" \
  --data-urlencode "offering_type=buy" \
  --data-urlencode "radius_km=5" \
  --data-urlencode "object_type=house,apartment" \
  --data-urlencode "energy_label=A,B,C" \
  --data-urlencode "sort=newest" \
  --data-urlencode "pages=0,1"
```

## 关于 TLS 适配层
`scripts/tls_client.py` 是一个用于兼容性的本地适配层，通过 `curl_cffi` 实现与外部系统的通信。
此技能无需使用系统级别的 `tls_client` 二进制文件。