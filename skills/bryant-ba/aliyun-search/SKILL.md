---
name: aliyun-search
description: 使用 Alibaba Cloud UnifiedSearch API 进行网络搜索。该 API 提供了高级搜索功能，并支持配置各种参数。
---

# 阿里云 UnifiedSearch 技能

该技能提供了使用阿里云 UnifiedSearch API 进行网络搜索的功能。

## 特点

- 支持多种搜索引擎类型（Generic、GenericAdvanced、LiteAdvanced）
- 可配置时间范围过滤
- 针对特定类别的搜索（金融、法律、医疗等）
- 基于位置的搜索（城市/IP）
- 丰富的结果格式化

## 使用方法

### 基本使用方法
```bash
python search.py "云栖大会"
```

### 高级使用方法
```bash
python search.py "北京天气" --engine-type "Generic" --city "北京市"
```

```bash
python search.py "金融新闻" --category "finance" --time-range "OneWeek" --engine-type "GenericAdvanced"
```

## 脚本

- `search.py`：阿里云 UnifiedSearch API 的 Python 实现

## 配置

在使用之前，您需要完成以下步骤：
1. 获取阿里云 AccessKey 和 Secret
2. 设置环境变量：
   ```bash
   export ALIBABA_CLOUD_ACCESS_KEY_ID="your_access_key_id"
   export ALIBABA_CLOUD_ACCESS_KEY_SECRET="your_access_key_secret"
   ```
3. 确保已获得所需的权限
4. 安装依赖项：`pip install aliyun-python-sdk-core requests`