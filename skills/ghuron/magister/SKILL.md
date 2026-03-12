---
name: magister
description: 从 Magister 门户获取课程安排、成绩以及学生违规记录。
homepage: https://magister.net
metadata: {"clawdbot":{"emoji":"🇲","requires":{"bins":["python"],"env":["MAGISTER_HOST","MAGISTER_USER","MAGISTER_PASSWORD"]}}}
---
> **注意：** 该 API 未经过官方文档记录，可能会随时更改。

所有 API 请求均使用 `web_fetch`，并设置请求头 `Authorization: Bearer {token}`。时间戳采用 UTC 格式。

> **备用方案：** 如果 `web_fetch` 返回 401 错误，说明您的实现可能不支持自定义请求头；此时请改用 `curl`：
> ```bash
> curl -s -H "Authorization: Bearer {token}" {url}
> ```

## 获取令牌

将以下代码写入 `/tmp/magister_auth.py` 文件中：
```python
import http.cookiejar, json, os, re, secrets, urllib.parse, urllib.request

jar = http.cookiejar.CookieJar()

class Capture(urllib.request.HTTPRedirectHandler):
    token = ""
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        p = urllib.parse.urlparse(newurl)
        if p.path.endswith("redirect_callback.html"):
            Capture.token = urllib.parse.parse_qs(p.fragment).get("access_token", [""])[0]
            return None
        return super().redirect_request(req, fp, code, msg, hdrs, newurl)

cap    = Capture()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar), cap)

qs = urllib.parse.urlencode({
    "client_id": f"M6-{os.environ['MAGISTER_HOST']}", "state": secrets.token_urlsafe(16),
    "redirect_uri": f"https://{os.environ['MAGISTER_HOST']}/oidc/redirect_callback.html",
    "response_type": "id_token token", "acr_values": f"tenant:{os.environ['MAGISTER_HOST']}",
    "nonce": secrets.token_urlsafe(16),
    "scope": "openid profile attendance.overview calendar.user grades.read",
})
resp      = opener.open(f"https://accounts.magister.net/connect/authorize?{qs}")
login_url = resp.geturl()
session_id = re.search(r"sessionId=([a-f0-9A-F-]+)", login_url).group(1)
return_url = urllib.parse.unquote(re.search(r"returnUrl=([^&]+)", login_url).group(1))

def challenge(path, extra):
    body = json.dumps({"sessionId": session_id, "returnUrl": return_url,
                       **extra}).encode()
    req  = urllib.request.Request(f"https://accounts.magister.net/challenges/{path}", data=body,
           headers={"Content-Type": "application/json",
                    "X-XSRF-TOKEN": urllib.parse.unquote(next((c.value for c in jar if c.name == "XSRF-TOKEN"), ""))})
    return json.loads(opener.open(req).read())

r = challenge("username", {"username": os.environ["MAGISTER_USER"]})
r = challenge("password", {"password": os.environ["MAGISTER_PASSWORD"]})

try: opener.open(f"https://accounts.magister.net{r['redirectURL']}")
except: pass

print(cap.token)
```

然后运行该文件：
```bash
python /tmp/magister_auth.py; rm /tmp/magister_auth.py
```

## 获取父节点 ID

使用 `Persoon.Id`（数值整数）作为 `{parent_id}`，执行以下请求：
`web_fetch GET https://{MAGISTER_HOST}/api/account`

## 列出子节点信息

执行以下请求以获取子节点信息（返回的 JSON 数据为小写格式）：
`web_fetch GET https://{MAGISTER_HOST}/api/ouders/{parent_id}/kinderen`
- `roepnaam`（姓名）
- `achternaam`（姓氏）
- `id`（子节点 ID，用于查询日程或违规记录）
- `actieveAanmeldingen[0].links.self.href`（关联的 `aanmelding_id`，用于查询成绩）

## 日程安排

执行以下请求以获取子节点的日程安排信息（返回的 JSON 数据为 PascalCase 格式）：
`web_fetch GET https://{MAGISTER_HOST}/api/personen/{child_id}/afspraken?van=YYYY-MM-DD&tot=YYYY-MM-DD`
- `Start`（开始时间）
- `Einde`（结束时间）
- `Omschrijving`（安排描述）
- `Lokatie`（地点）
- `Vakken[0].Naam`（课程名称）
- `Docenten[0].Naam`（授课教师姓名）

## 违规记录

执行以下请求以获取子节点的违规记录信息（返回的 JSON 数据为 PascalCase 格式）：
`web_fetch GET https://{MAGISTER_HOST}/api/personen/{child_id}/absenties?van=YYYY-MM-DD&tot=YYYY-MM-DD`
- `Omschrijving`（违规类型）
- `Code`（违规代码，如 “TR”/“HV”/“AT”）
- `Geoorloofd`（是否被允许）
- `Afspraak.Omschrijving`（违规详情）

## 成绩记录

执行以下请求以获取子节点的成绩记录（返回的 JSON 数据为小写格式）：
`web_fetch GET https://{MAGISTER_HOST}/api/aanmeldingen/{aanmelding_id}/cijfers?top=50`
- `waarde`（成绩值）
- `isVoldoende`（是否及格）
- `teltMee`（是否计入总分）
- `kolom.omschrijving`（成绩栏描述）
- `kolom.weegfactor`（成绩权重）
- `kolom.type`（成绩类型，如 “cijfer”/“gemiddelde”/“tekortpunten”/“som”）