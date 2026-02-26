---
name: molit-real-estate
description: MOLIT公寓实际交易价格API
version: 2.2.0
author: chumjibot
created: 2026-02-10
updated: 2026-02-19
tags: [real-estate, korea, openapi, data.go.kr]
connectors: [~~realestate, ~~law, ~~search, ~~notify]
---
# 房地产交易技能

整合了MOLIT公寓销售交易数据与相关法律信息。

## 概述

| 关键信息 | 值 |
|-------|-------|
| 提供方 | MOLIT（国土交通部） |
| 服务ID | 15126469 |
| 认证信息 | `~/.config/data-go-kr/api_key` |
| 端点地址 | `https://apis.data.go.kr/1613000/RTMSDataSvcAptTrade` |
| 法律依据 | 《房地产交易报告法》 |
| 操作手册 | `playbook.md` |

## 脚本

```
scripts/
└── real_estate.sh [district_code] [YYYYMM] [rows]
```

## 工作流程

### 第1步：确定区域和时间段
- 例如：“강남 아파트” → 选择Gangnam-gu（区域代码11680），当前月份
- 可参考`playbook.md`中的关注区域列表
- 默认为当前月份；若列表为空，则查询最近3个月的交易数据

### 第2步：获取交易数据
- 使用`real_estate.sh [代码] [YYYYMM]`命令获取数据

### 第3步：数据分析
- 计算每坪的价格（面积除以3.3058）
- 可根据需求进行同比价格比较

### 第4步：法律信息整合（可选）
- 租赁纠纷相关内容参考《住房租赁保护法》
- 销售相关内容参考《房地产交易报告法》

### 第5步：生成结构化响应

## 输出模板

```markdown
## 🏠 [District] Apartment Transactions

### Recent Transactions
| Apt | Area | Floor | Price | Per Pyeong | Date |
|-----|------|-------|-------|-----------|------|

### 📊 Summary
- Avg price: X억
- Avg per pyeong: X만/평
- Total transactions: X

### 💡 Notes
[Trend / related law info]
```

## 首尔各区代码

| 区域 | 代码 | 区域 | 代码 |
|----------|------|----------|------|
| Jongno | 11110 | Mapo | 11440 |
| Yongsan | 11170 | Gangnam | 11680 |
| Seocho | 11650 | Songpa | 11710 |
| Gangdong | 11740 | Yeongdeungpo | 11560 |
| Seongdong | 11200 | Gwanak | 11620 |

## 其他城市代码
| 区域 | 代码 |
|----------|------|
| Busan Haeundae | 26350 |
| Daegu Suseong | 27200 |
| Incheon Yeonsu | 28185 |
| Daejeon Yuseong | 30200 |

## 响应字段（XML格式，自2026年起使用英文字段名）

| 关键字段 | 说明 |
|-----|-------------|
| aptNm | 公寓名称 |
| umdNm | 区域名称 |
| excluUseAr | 独有面积（平方米） |
| floor | 楼层 |
| dealAmount | 交易价格（万韩元，以逗号分隔） |
| dealYear/Month/Day | 交易日期 |
| dealingGbn | 交易类型 |
| buildYear | 建筑年份 |

## 连接器

| 占位符 | 用途 | 当前使用的工具 |
|-------------|---------|-------------|
| `~~realestate` | 交易数据 API | MOLIT数据接口（data.go.kr） |
| `~~law` | 法律参考资料 | law.go.kr |
| `~~search` | 市场趋势查询 | Brave Search搜索引擎 |
| `~~notify` | 通知功能 | Telegram消息服务 |

## 意图路由规则

| 意图 | 触发条件 | 输出内容 |
|---|--------|--------------------|--------|
| 1 | 价格查询 | 输入“강남 아파트 실거래가”或“최근 거래 보여줘” | 显示交易列表及价格汇总 |
| 2 | 趋势分析 | 输入“송파 시세 추이”或“6개월간 가격 변화” | 显示多个月份的价格变化 |
| 3 | 区域对比 | 输入“강남 vs 서초 비교”或“강남3구 어디가 비싸?” | 显示两个区域的房价对比表 |

详情请参见上述工作流程。

## 跨技能整合

| 触发条件 | 相关技能 | 实现方式 |
|---------|---------------|-----|
| “需要相关法律信息” | `law-search`（用于查询《住房租赁保护法》或《房地产交易报告法》 | 提供相关法律条文 |
| “需要周边环境信息” | `kma-weather`（用于查询天气数据） | 提供区域的气候和环境信息 |
| “从投资角度分析” | `finance-sector-analysis` | 提供房地产行业分析 |

### 跨技能整合示例：
- 使用`real_estate.sh`获取交易数据
- 通过`law-search`查询相关法律法规
- 将法律参考内容添加到报告报告中

### 跨技能：房地产与地理位置的结合
- 使用`real_estate.sh`获取交易数据
- 通过`kma-weather`获取区域天气和空气质量数据
- 将这些信息整合到区域对比报告中

## 注意事项：
1. 区域代码为5位数字（表示市/郡/区级别）
2. 合同签订月份采用YYYYMM格式
3. `dealAmount`字段包含逗号，需将其解析为字符串处理
4. 数据更新延迟约为实际交易后的1-2个月
5. 对于大量数据，可使用`pageNo`参数进行分页查询

---
*Cowork架构 v2.2 — 🦞 chumjibot (2026-02-19)*

## 🔧 设置（公共数据门户API）

1. 访问[data.go.kr](https://www.data.go.kr)注册账号
2. 登录后进入个人页面，复制**通用认证密钥**
3. 将API密钥保存到指定位置（见```bash
   mkdir -p ~/.config/data-go-kr
   echo "YOUR_API_KEY" > ~/.config/data-go-kr/api_key
   ```）
4. 向相关服务提交**使用申请**（系统将自动批准）
   - 可查询[韩国国土交通部的公寓交易数据](https://www.data.go.kr/data/15057511/openapi.do)（API编号：15057511）