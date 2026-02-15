---
name: nlb
description: 查询贷款信息，并从新加坡国家图书馆委员会（National Library Board of Singapore）搜索相关资源。
homepage: https://www.nlb.gov.sg
metadata:
  { "clawdbot": { "emoji": "📚", "requires": { "bins": [] }, "install": [] } }
---

# NLB（国家图书馆）使用技巧

## 登录NLB

1. 打开 https://signin.nlb.gov.sg/authenticate/login
2. 使用用户名 “myLibrary” 和密码登录

## 查看借阅记录（需要登录）

1. 打开 https://www.nlb.gov.sg/mylibrary/loans
2. 查看 “当前” 标签页，了解借阅的图书及其到期日期
3. 查看 “逾期” 标签页，了解已逾期的借阅图书

## 查看推荐资源（需要登录）

1. 打开 https://www.nlb.gov.sg/mylibrary/Home

## 搜索资源

1. 对搜索查询进行 URL 编码
2. 打开搜索结果页面：https://catalogue.nlb.gov.sg/search?query={url_encoded_query}
   可选的 URL 参数过滤器：
   - &universalLimiterIds=at_library （仅显示图书馆内可借阅的图书）
   - &pageNum=0 （指定页面编号，从第 0 页开始）
   - &viewType=grid （以网格格式显示结果）
   - &materialTypeIds=1 （仅显示图书）
   - &collectionIds={collection_ids} （按特定馆藏筛选，详见下文）
   - &locationIds={location_ids} （按特定图书馆筛选，详见下文）
   - languageIds={language_ids} （按语言筛选：chi：中文，eng：英文，mal：马来文，tam：泰米尔文）

### 馆藏ID对应关系：
| 馆藏名称                          | 馆藏ID         |
| ------------------------------------ | -------------- |
| 早期读物（4-6岁）                    | 7             |
| 少儿图画书                        | 11            |
| 少儿馆藏                          | 9             |
| 早期读物（无障碍版）                    | 55            |
| 少儿简易小说                      | 12            |
| 少儿馆藏（无障碍版）                    | 8             |
| 成人馆藏                          | 3             |

### 图书馆ID对应关系：
| 图书馆名称                        | 图书馆ID         |
| --------------------------- | --------------------- |
| 多美坡图书馆                      | 23          |
| 比善图书馆                      | 6           |
   中央图书馆                      | 29          |

### 示例

搜索查询 “BookLife readers”，筛选条件为：仅显示图书、仅限于多美坡图书馆的馆藏、属于少儿图画书或少儿馆藏的图书，并以网格格式显示第一页：
https://catalogue.nlb.gov.sg/search?query=BookLife%20readers&pageNum=0&locationIds=23&universalLimiterIds=at_library&collectionIds=11,9,7&viewType=grid&materialTypeIds=1

## 打开搜索结果页面

1. 点击搜索结果链接，在浏览器中打开搜索结果页面
搜索结果页面示例：
https://catalogue.nlb.gov.sg/search/card?id=127ebe36-bad7-566c-8d81-3a32379254ad&entityType=FormatGroup