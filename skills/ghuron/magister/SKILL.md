---
name: magister
description: 从 Magister 门户获取课程安排、成绩以及违规记录。
homepage: https://magister.net
metadata: {"clawdbot":{"emoji":"🇲","requires":{"bins":["node"],"env":["MAGISTER_HOST","MAGISTER_USER","MAGISTER_PASSWORD"]}}}
---
# 获取令牌

```bash
node "$(dirname "$0")/obtain_token.mjs"
```

将 `{token}` 打印到标准输出（stdout）。后续的所有 API 请求都需要使用 `web_fetch`，并设置请求头 `Authorization: Bearer {token}`。

> **备用方案：** 如果 `web_fetch` 返回 401 错误，说明您的实现可能不支持自定义请求头。  
> 可以改用 `curl` 来发送请求：  
> ```bash
> curl -s -H "Authorization: Bearer {token}" {url}
> ```

所有时间均以 UTC 为基准。

# 获取父级 ID

```
web_fetch GET https://{MAGISTER_HOST}/api/account
```

使用 `Persoon.Id`（一个数字整数）作为 `{parent_id}`。

# 列出子级信息

```
web_fetch GET https://{MAGISTER_HOST}/api/ouders/{parent_id}/kinderen
```

数据以小写 JSON 格式返回，每个子级信息包含以下字段：  
- `roepnaam`（名字）  
- `achternaam`（姓氏）  
- `id`（子级 ID，用于关联日程或违规记录）  
- `actieveAanmeldingen[0].links.self.href`（关联的报名记录 ID，用于获取成绩信息）

# 日程安排

```
web_fetch GET https://{MAGISTER_HOST}/api/personen/{child_id}/afspraken?van=YYYY-MM-DD&tot=YYYY-MM-DD
```

数据以大写 JSON 格式返回，每个日程安排包含以下字段（忽略 `Status=5` 的记录，表示已取消）：  
- `Start`（开始时间）  
- `Einde`（结束时间）  
- `Omschrijving`（描述）  
- `Lokatie`（地点）  
- `Vakken[0].Naam`（课程名称）  
- `Docenten[0].Naam`（教师姓名）

# 违规记录

```
web_fetch GET https://{MAGISTER_HOST}/api/personen/{child_id}/absenties?van=YYYY-MM-DD&tot=YYYY-MM-DD
```

数据以大写 JSON 格式返回，每个违规记录包含以下字段：  
- `Omschrijving`（违规类型）  
- `Code`（违规代码，例如 “TR”/“HV”/“AT”）  
- `Geoorloofd`（是否被原谅）  
- `Afspraak.Omschrijving`（违规详情）

# 成绩记录

```
web_fetch GET https://{MAGISTER_HOST}/api/aanmeldingen/{aanmelding_id}/cijfers?top=50
```

数据以小写 JSON 格式返回，每个成绩记录包含以下字段：  
- `waarde`（成绩值）  
- `isVoldoende`（是否及格）  
- `teltMee`（是否计入总成绩）  
- `kolom.omschrijving`（成绩说明）  
- `kolom.weegfactor`（成绩权重）  
- `kolom.type`（成绩类型，例如 “cijfer”/“gemiddelde”/“tekortpunten”/“som”）