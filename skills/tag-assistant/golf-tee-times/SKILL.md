---
name: golf-tee-times
description: "搜索任何地点附近的高尔夫开球时间和优惠信息。查找最便宜的高尔夫球场费用，比较不同平台上的价格，并获取折扣建议。在需要了解高尔夫相关信息（如开球时间、球场选择或预订球场服务）时，可参考本指南。"
metadata:
  openclaw:
    emoji: "⛳"
    requires:
      bins: ["curl", "python3"]
---
# 高尔夫开球时间查找器 ⛳  
使用GolfNow API（经过逆向工程实现）来查找和比较高尔夫开球时间，适用于任何地点。  

## 使用场景  
- 用户需要查询开球时间、预订高尔夫课程或进行比赛  
- 寻找便宜/折扣优惠的高尔夫活动  
- 比较特定区域内的高尔夫球场  
- 查看特定日期的球场可用性  
- 查找可抵扣费用的开球时间（如交易优惠）  

## GolfNow API（主要使用方法）  
GolfNow网站通过POST API获取开球时间信息。这是**唯一可靠的方法**；使用`web_fetch`方法时，返回的只是空壳数据（由JavaScript渲染的单页应用）。  

### API接口  
```
POST https://www.golfnow.com/api/tee-times/tee-time-results
Content-Type: application/json
Accept: application/json
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36
Origin: https://www.golfnow.com
```  

### 按球场类型搜索（SearchType: 1）—— 可用 ✅  
需要提供`FacilityId`参数。会返回该球场在指定日期的所有开球时间。  
```json
{
  "Radius": 50,
  "Latitude": 26.1224,
  "Longitude": -80.1373,
  "PageSize": 50,
  "PageNumber": 0,
  "SearchType": 1,
  "SortBy": "Date",
  "SortDirection": 0,
  "Date": "Feb 16 2026",
  "BestDealsOnly": false,
  "PriceMin": "0",
  "PriceMax": "10000",
  "Players": "2",
  "Holes": "3",
  "FacilityType": 0,
  "RateType": "all",
  "TimeMin": "10",
  "TimeMax": "42",
  "FacilityId": 5744,
  "SortByRollup": "Date.MinDate",
  "View": "Grouping",
  "ExcludeFeaturedFacilities": true,
  "TeeTimeCount": 50,
  "PromotedCampaignsOnly": "false",
  "CurrentClientDate": "2026-02-16T05:00:00.000Z"
}
```  

### 按区域搜索（SearchType: 0）—— 不可用 ❌  
如果没有`FacilityId`，该方法将返回0个结果。API需要针对具体球场进行查询。  

### 关键参数  
| 参数 | 值 | 说明 |  
|-------|--------|-------|  
| `Players` | "1"-"4" | 字符串类型，非整数 |  
| `Holes` | "1"=9洞，"2"=18洞，"3"=任意洞数 | 字符串类型 |  
| `TimeMin`/`TimeMax` | 10-42 | 时间范围（10=上午5点，42=晚上9点以后） |  
| `Date` | "2026年2月16日" | 人类可读格式 |  
| `FacilityType` | 0=任意类型，1=普通球场，2=模拟器球场 |  
| `BestDealsOnly` | true/false | 过滤优惠活动（但区域搜索时返回0个结果） |  
| `SearchType` | 1 | 必须设置为1（表示按球场类型搜索）；0/2/3无效 |  

### 响应结构  
```
ttResults.teeTimes[] → array of tee time groups
  ├── formattedTime: "7:18"
  ├── formattedTimeMeridian: "AM"
  ├── time: "2026-02-16T07:18:00"  (ISO timestamp)
  ├── displayRate: 35.0  (price per player)
  ├── multipleHolesRate: 18  (hole count)
  ├── maxPriceTransactionFee: 2.99
  ├── facility.name, facility.address.city, facility.averageRating, facility.reviewCount
  ├── facility.seoFriendlyName  (for building URLs)
  ├── facility.latitude, facility.longitude
  └── teeTimeRates[] → rate options for this time slot
       ├── rateName: "Prepaid - Online Rate" / "Hot Deal" / "Twilight" / etc.
       ├── isHotDeal: true/false  🔥
       ├── isTradeOffer: true/false  💳 (credit-bookable)
       ├── isCartIncluded: true/false
       ├── singlePlayerPrice.greensFees.value: 35.0
       └── rateSetTypeId: 1=prepaid, other=pay at course
```  

### 构建球场链接  
```
https://www.golfnow.com/tee-times/facility/{seoFriendlyName}/search
```  
示例：`https://www.golfnow.com/tee-times/facility/5744-colony-west-golf-club-glades-course/search`  

## 辅助脚本  
使用`skills/golf-tee-times/golfnow-search.py`进行批量查询。具体用法请参阅脚本。  

## 获取球场ID  
由于区域搜索不可用，因此需要手动获取球场ID：  
1. **使用已知的球场数据库**  
2. **网页搜索**：`site:golfnow.com/tee-times/facility {城市} {州}`—— 页面URL中包含球场ID  
3. **浏览器拦截**：加载球场页面后，拦截发送到`/api/tee-times/tee-time-results`的POST请求，从中提取`FacilityId`  

## Telegram输出格式  
使用以下格式展示开球时间：  
```
🏌️ *Tee Times · {Day} {Date} · {Players} Players*

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

🔥 *DEALS*

🔥 *[Course Name](url)*
City · X mi · ⭐ X.X · N reviews
▸ Time · *$XX* · 18 holes · cart 🔥

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

*[Course Name](url)*
City · X mi · ⭐ X.X · N reviews
▸ Time range · $XX
▸ Time range · $XX twilight

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

_All prices per player · cart included · via GolfNow_
```  
- 使用`▸`标记时间槽  
- 以Markdown链接的形式突出显示球场名称  
- 先显示优惠信息（🔥 优惠活动，💳 折扣优惠）  
- 按价格区间分组显示开球时间  
- 包括球场距离、评分和评论数量  
- 对于热门时间段添加特别标注（如`← AM slots`）  
- 底部提示：_每位玩家的价格 · 包含购物车服务 · 通过GolfNow预订_  

## 折扣提示：  
1. 🔥 **GolfNow优惠活动**：API中`isHotDeal`字段为`true`，表示未售出的球位有大幅折扣。  
2. 💳 **交易优惠**：`isTradeOffer`字段为`true`，可使用GolfNow积分预订。  
3. 🚶 **步行优惠**：可节省20-50美元的购物车费用。  
4. 🌅 **黄昏时段优惠**：下午2-3点后价格下降（查看`rateName: "Twilight"`）。  
5. 🏠 **本地居民优惠**：显示适用于本地居民的折扣信息。  
6. ⏰ **最后一刻优惠**：当天价格可能下降；优惠活动通常在开球时间附近出现。  
7. 📞 **致电专业球店**：有时电话预订价格更便宜。  
8. 🗓️ **工作日 > 周末**：周一至周四价格更优惠。  
9. 🌧️ **天气预报**：天气不佳时价格可能下降。  

## 季节性提示（根据所在地区）  
- **旺季**（12月-4月）：价格最高，建议提前3-7天预订；上午的球位通常很快售罄。  
- **夏季**（5月-9月）：价格便宜40-60%，但天气炎热潮湿。建议选择清晨或黄昏时段。  
- **飓风季节**（6月-11月）：因降雨可能提供折扣。  
- **性价比最高的月份**：9月（价格最低且人少）。  

## 预订流程  
### （通过浏览器使用GolfNow预订）  
### ⚠️ 重要提示：**在点击“确认预订”之前，务必将最终结算页面的截图发送给用户，并等待其明确批准。**  
1. 访问`https://www.golfnow.com/tee-times/facility/{facilityId}/tee-time/{teeTimeId}`  
2. 选择参赛人数，点击相应的单选按钮，确认果岭使用费是否更新。  
3. 点击“继续预订”（`.btnBook`）；未登录时会跳转到登录页面。  
4. 登录（使用GolfID：`my.golfid.io`），通过`frame=[src*=golfid]`访问邮箱/密码字段（使用`scripts/vault.sh get golfnow`获取GolfID）。  
5. 结算页面（URL：`.../checkout/players/{count}`）：  
   - **应用奖励**：点击`#applyRewardsBtn`，根据代码ID选择奖励（例如`#MEMBERSAVE`）；  
   - 注意：标有“Cannot Be Combined”的奖励无法与优惠活动同时使用。  
   - **应用GolfPass积分**：点击`#btn-apply-loyalty-points`（这些积分在优惠活动中可用）。  
   - **取消开球时间保护**：点击`input[name=rdlTeeTimeProtection][value=false]`。  
   - **拒绝慈善捐款**：如不需要可点击“No Thanks”。  
   - **支付**：使用保存的信用卡信息（默认为AMEX 1004）。  
6. **截图并发送给用户**：在继续下一步前，通过Telegram发送结算页面的截图。  
7. 等待用户批准。  
8. 确认预订条款（点击`#agree-terms-top`）。  
9. 确认预订（点击`#reservation-button-top`）。  
10. 去除Truist广告（`[class*=rokt], [class*=bold]`），并保存确认页面的截图。  

### 用户的预订偏好：  
- 始终应用积分/奖励以降低费用。  
- 取消开球时间保护（可节省3-4美元）。  
- 默认支付卡：AMEX（卡号以1004结尾）。  
- 预订完成后发送确认截图。