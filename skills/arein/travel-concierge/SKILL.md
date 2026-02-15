---
name: travel-concierge
description: 查找住宿房源的联系方式（Airbnb、Booking.com、VRBO、Expedia）
version: 1.0.0
triggers:
  - find contact
  - hotel contact
  - accommodation contact
  - property contact
  - airbnb contact
  - booking contact
  - vrbo contact
  - expedia contact
  - direct booking
  - property email
  - property phone
---

# 旅行礼宾服务

本工具可帮助您获取住宿信息的联系方式（电话、电子邮件、WhatsApp、Instagram等），以便直接进行预订。

## 使用方法

当用户提供预订链接或请求获取住宿的联系方式时，请按照以下步骤操作：

1. 运行命令行工具（CLI）以提取联系方式：
   ```bash
   travel-concierge find-contact "<url>"
   ```

2. 将提取到的所有联系方式展示给用户。

## 支持的平台

- **Airbnb**: `airbnb.com/rooms/...`
- **Booking.com**: `booking.com/hotel/...`
- **VRBO**: `vrbo.com/...`
- **Expedia**: `expedia.com/...Hotel...`

## 示例

### 获取Airbnb房源的联系方式
用户：「请获取这个Airbnb房源的联系方式：https://www.airbnb.com/rooms/12345」

操作：运行 `travel-concierge find-contact "https://www.airbnb.com/rooms/12345"`

### 获取Booking.com酒店的联系方式
用户：「我该如何直接联系这家酒店？」（提供Booking.com链接）

操作：运行 `travel-concierge find-contact "<booking-url>"`

## 脚本使用的JSON输出格式
```bash
travel-concierge find-contact --json "https://..."
```

## 详细输出（用于查看搜索进度）
```bash
travel-concierge find-contact --verbose "https://..."
```

## 配置说明

该工具无需使用API密钥，通过网页抓取技术来获取信息。如需更精确的结果，可配置以下可选API：

```bash
# Set Google Places API key for verified phone/website data
travel-concierge config set googlePlacesApiKey "your-key"

# View current config
travel-concierge config show
```

## 输出格式

命令行工具返回的联系方式文件包含以下内容：
- **房源信息**：名称、平台、位置、房东名称
- **联系方式**：
  - 电话号码
  - 电子邮件地址
  - WhatsApp（如可用）
  - Instagram账号
  - Facebook页面
  - 网站链接
  - Google地图链接
- **来源**：每条联系方式的获取途径及可信度等级

## 注意事项

- 该工具仅提取公开可用的信息。
- 对于通过JavaScript渲染的房源页面，可能需要使用浏览器自动化工具（如`agent-browser`）。
- 部分平台对抓取行为有严格限制，因此搜索结果可能有所不同。
- 配置Google Places API后，可获取最可靠的联系方式数据。