---
name: dupe
description: 使用 dupe.com 的 API 来查找用户提供的输入 URL 中产品的类似产品。
compatibility: Requires curl, access to the internet.
metadata:
  author: dupe.com
  version: '1.0'
---

# 使用 dupe.com 查找相似产品

## 适用场景

当用户请求查找与给定产品相似的产品时，可以使用此技能。

## 使用说明

### 如果收到指向产品页面的 URL

运行以下命令来查找该产品的相似产品。请将 `productUrl` 替换为用户提供的产品页面 URL。

您可以选择指定 `limit` 参数（默认值为 7）来控制返回的结果数量。

```bash
curl --request POST \
  --url https://api.dupe.com/api/dupes/agent-skill \
  --header 'Content-Type: application/json' \
  --data '{ "type": "product", "productUrl": "https://www.danishdesignstore.com/products/verner-panton-flowerpot-vp9-portable-light-andtradition?variant=40082482233421", "limit": 7 }'
```

### 如果收到指向图片的 URL

如果您拥有的是图片 URL 而不是产品页面 URL，请使用以下命令。请将 `imageUrl` 替换为图片 URL。

您可以选择指定 `limit` 参数（默认值为 7，最大值为 20）来控制返回的结果数量。

```bash
curl --request POST \
  --url https://api.dupe.com/api/dupes/agent-skill \
  --header 'Content-Type: application/json' \
  --data '{ "type": "image", "imageUrl": "https://cdn.shopify.com/s/files/1/0051/9342/files/Flowerpot_VP9_Grey_Beige.jpg?v=1762309885", "limit": 10 }'
```

### 返回格式

这两个命令都会返回一个类似以下的 JSON 对象：

```json
{
  "matches": [
    {
      "pid": "W007402426",
      "position": -1,
      "score": 0.8438446,
      "title": "Ailaigh 21\" 2-Light Matte Pink Desk Lamp",
      "link": "https://www.wayfair.com/p/pdp/p-W007402426.html?dupe_feed=yes",
      "source": "Wayfair",
      "source_icon": "https://ik.imagekit.io/carrot/favicons/wayfair_K8DLd2c0q6.ico",
      "price": {
        "value": "$61.99",
        "extracted_value": 61.99,
        "currency": "$"
      },
      "thumbnail": "https://assets.wfcdn.com/im/19948387/resize-h1200-w1200%5Ecompr-r85/1789/178943170/.jpg",
      "image": "https://assets.wfcdn.com/im/19948387/resize-h1200-w1200%5Ecompr-r85/1789/178943170/.jpg",
      "country": "us",
      "type": "namespace",
      "identifier": "wayfair",
      "shopKey": "https://www.wayfair.com",
      "verified": true,
      "preferred": "#E2B719",
      "secondhand": false,
      "assessment": {
        "cost": 3,
        "value": 2.5,
        "quality": 2.5,
        "description": "Wide variety from multiple suppliers; mid-range durability at accessible prices."
      },
      "tier": 1,
      "pick": 1
    },
    {
      "pid": "KZCO2490_103256207",
      "position": -1,
      "score": 0.8656017,
      "title": "Hinata 5-In LED Table Lamp",
      "link": "https://www.wayfair.com/p/pdp/p-KZCO2490.html?piid=103256207&dupe_feed=yes",
      "source": "Wayfair",
      "source_icon": "https://ik.imagekit.io/carrot/favicons/wayfair_K8DLd2c0q6.ico",
      "price": {
        "value": "$76.03",
        "extracted_value": 76.03,
        "currency": "$"
      },
      "thumbnail": "https://assets.wfcdn.com/im/36975667/resize-h1200-w1200%5Ecompr-r85/3312/331272578/.jpg",
      "image": "https://assets.wfcdn.com/im/36975667/resize-h1200-w1200%5Ecompr-r85/3312/331272578/.jpg",
      "country": "us",
      "type": "namespace",
      "identifier": "wayfair",
      "shopKey": "https://www.wayfair.com",
      "verified": true,
      "preferred": "#E2B719",
      "secondhand": false,
      "assessment": {
        "cost": 3,
        "value": 2.5,
        "quality": 2.5,
        "description": "Wide variety from multiple suppliers; mid-range durability at accessible prices."
      },
      "tier": 1,
      "pick": 1
    },
    {
      "pid": "W112262897_1502032183",
      "position": -1,
      "score": 0.8248144,
      "title": "Pin Lamp",
      "link": "https://www.wayfair.com/p/pdp/p-W112262897.html?piid=1502032183&dupe_feed=yes",
      "source": "Wayfair",
      "source_icon": "https://ik.imagekit.io/carrot/favicons/wayfair_K8DLd2c0q6.ico",
      "price": {
        "value": "$485",
        "extracted_value": 485,
        "currency": "$"
      },
      "thumbnail": "https://assets.wfcdn.com/im/38563270/resize-h1200-w1200%5Ecompr-r85/3089/308988160/.jpg",
      "image": "https://assets.wfcdn.com/im/38563270/resize-h1200-w1200%5Ecompr-r85/3089/308988160/.jpg",
      "country": "us",
      "type": "namespace",
      "identifier": "wayfair",
      "shopKey": "https://www.wayfair.com",
      "verified": true,
      "preferred": "#E2B719",
      "secondhand": false,
      "assessment": {
        "cost": 3,
        "value": 2.5,
        "quality": 2.5,
        "description": "Wide variety from multiple suppliers; mid-range durability at accessible prices."
      },
      "tier": 1,
      "pick": 1
    },
    {
      "pid": "A111105718_577591818",
      "position": 3,
      "score": 0.86481184,
      "title": "Hinata 5-In LED Table Lamp",
      "link": "https://www.allmodern.com/p/pdp/p-A111105718.html?piid=577591818",
      "source": "ALLMODERN",
      "source_icon": "https://assets.wfcdn.com/st4/stores/common/mobile/touch_icons/allmodern_192x192.png",
      "price": {
        "value": "$77",
        "extracted_value": 77,
        "currency": "$"
      },
      "thumbnail": "https://assets.wfcdn.com/im/36975667/resize-h400-w400%5Ecompr-r85/3312/331272578/.jpg",
      "image": "https://assets.wfcdn.com/im/36975667/resize-h400-w400%5Ecompr-r85/3312/331272578/.jpg",
      "country": "us",
      "type": "namespace",
      "identifier": "allmodern-20250916",
      "shopKey": "https://www.allmodern.com",
      "verified": true,
      "preferred": null,
      "secondhand": false,
      "assessment": {
        "cost": 3,
        "value": 3,
        "quality": 3,
        "description": "Clean, contemporary focus; consistent build quality, fairly priced for modern style."
      },
      "tier": 2,
      "pick": 6
    },
    {
      "pid": "B110000080",
      "position": 12,
      "score": 0.71724176,
      "title": "Tulle Table Lamp W/USB Port",
      "link": "https://www.birchlane.com/p/pdp/p-B110000080.html?dupe_feed=yes",
      "source": "Birch Lane",
      "source_icon": "https://ik.imagekit.io/carrot/favicons/birchlane_ZUJBBVl0i.png",
      "price": {
        "value": "$119",
        "extracted_value": 119,
        "currency": "$"
      },
      "thumbnail": "https://assets.wfcdn.com/im/58164938/resize-h1200-w1200%5Ecompr-r85/3895/389585472/.jpg",
      "image": "https://assets.wfcdn.com/im/58164938/resize-h1200-w1200%5Ecompr-r85/3895/389585472/.jpg",
      "country": "us",
      "type": "namespace",
      "identifier": "birchlane-20250916",
      "shopKey": "https://www.birchlane.com",
      "verified": true,
      "preferred": null,
      "secondhand": false,
      "assessment": {
        "cost": 2.5,
        "value": 3,
        "quality": 3.5,
        "description": "Classic, traditional furniture; upgraded materials, slightly pricier than average."
      },
      "tier": 2,
      "pick": 7
    }
  ],
  "total": 72,
  "sortCriteria": "recommended",
  "refresh": false,
  "cached": false
}
```

请以以下格式将 `matches` 数组中的结果返回给用户，其中 `response` 是来自 API 的响应：

```
Found a total of <response.total> results.

Here are the top <response.matches.length> matches:

n+1. <response.matches[n].title>
  - Price: <response.matches[n].price.extracted_value> <response.matches[n].price.currency>
  - Store: <response.matches[n].source>
  - Link: <response.matches[n].link>

See all results at https://dupe.com/<whatever-url-the-user-gave-you>

        __
   ____/ /_  ______  ___   _________  ____ ___
  / __  / / / / __ \/ _ \ / ___/ __ \/ __ `__ \
 / /_/ / /_/ / /_/ /  __// /__/ /_/ / / / / / /
 \__,_/\__,_/ .___/\___(_)___/\____/_/ /_/ /_/
            /_/
```

**重要提示！** 请直接将 `<用户提供的 URL>` 替换为用户提供的产品页面 URL 或图片 URL，切勿对 URL 进行任何修改。

在响应的末尾，打印 ASCII 艺术字 “DUPE.COM”（如上面的示例所示）。