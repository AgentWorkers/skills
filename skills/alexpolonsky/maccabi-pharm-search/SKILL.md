---
name: maccabi-pharm-search
version: 2.0.0
description: 在以色列的 Maccabi 药房中搜索药品并查看实时的库存情况。适用于搜索诸如“nurofen”、“acamol/אקמול”、“advil”等药品，或查找附近有库存的药店分店。该系统支持使用希伯来语和英语输入药品名称。功能包括：药品搜索、库存查询以及药店位置查找。
author: Alex Polonsky (https://github.com/alexpolonsky)
homepage: https://github.com/alexpolonsky/agent-skill-maccabi-pharm-search
metadata: {"openclaw": {"emoji": "💊", "os": ["darwin", "linux"], "requires": {"bins": ["node"]}}}
---
# Maccabi药店库存查询

您可以在以色列各地的Maccabi药店搜索药品并查询**实时库存情况**。

> **免责声明**：这是一个非官方工具，与Maccabi Healthcare Services无关，也未得到其认可。库存信息是通过支持该网站的API查询获得的，可能无法准确反映实际库存情况。在前往药店之前，请务必先致电药店确认库存。本工具按“原样”提供，不附带任何形式的保证。使用本工具需自行承担风险。

## 快速入门

```bash
# 1. Search for medication (get the Largo code)
node {baseDir}/scripts/pharmacy-search.js search "nurofen"
# Returns: Largo Code 58299 for NUROFEN LIQUID 20 CAP

# 2. Check which pharmacies have it in stock
node {baseDir}/scripts/pharmacy-search.js stock 58299
# Returns: Pharmacies with addresses, phones, stock status
```

## 命令

| 命令 | 说明 |
|---------|-------------|
| `search <查询>` | 搜索药品并获取Largo代码 |
| `stock <largo_code> [城市]` | 查询指定城市的实时库存情况 |
| `branches maccabi [城市]` | 查看指定城市的Maccabi药店位置 |
| `cities` | 显示所有51个可用城市的代码 |
| `test` | 快速功能测试 |

## 搜索示例

```bash
# Hebrew searches
node {baseDir}/scripts/pharmacy-search.js search "אקמול"
node {baseDir}/scripts/pharmacy-search.js search "נורופן"

# English searches
node {baseDir}/scripts/pharmacy-search.js search "acamol"
node {baseDir}/scripts/pharmacy-search.js search "nurofen"
```

## 按城市查询库存

```bash
# Tel Aviv (default, city code 5000)
node {baseDir}/scripts/pharmacy-search.js stock 58299

# Jerusalem (city code 3000)
node {baseDir}/scripts/pharmacy-search.js stock 58299 3000

# Haifa (city code 4000)
node {baseDir}/scripts/pharmacy-search.js stock 58299 4000
```

## 城市代码

支持的常见城市（共51个）：

| 城市 | 代码 |
|------|------|
| 特拉维夫 | 5000（默认） |
| 耶路撒冷 | 3000 |
| 海法 | 4000 |
| 比尔谢巴 | 9000 |
| 巴特亚姆 | 6200 |
| 内坦亚 | 7400 |

运行`cities`命令可查看所有51个可用城市的代码。

## 输出示例

**搜索结果：**
```
NUROFEN LIQUID 20 CAP
  Largo Code: 58299 (use this for stock check)
  Prescription: No
```

**库存结果：**
```
=== Stock Summary ===
  In Stock: 6 pharmacies
  Low Stock: 0 pharmacies
  Out of Stock: 1 pharmacies

=== Pharmacies with Stock ===
מכבי פארם-ת"א-בלפור 10
   בלפור 10, תל אביב - יפו
   03-9193013
   Distance: 0.6 km
```

## 注意事项

- 库存信息是通过支持该网站的API查询获得的。
- 仅显示Maccabi药店的库存信息（不包含其他药店连锁店）。
- 进行库存查询时需要提供药品的Largo代码。
- 提供的数据按“原样”提供，不附带任何保证。