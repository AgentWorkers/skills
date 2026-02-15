# Kakao Local API Skill

**用于调用Kakao Local（地点与地址）API的OpenClaw Skill**

## 概述

这是一个通过OpenClaw Skill调用Kakao Local API来执行地址规范化和地点搜索功能的工具。

## 系统要求

- Windows操作系统
- PowerShell 5.0或更高版本
- curl.exe（Windows 10及以上系统默认已安装）
- Kakao Developers的REST API密钥

## API密钥设置

**重要提示**：API密钥不会作为技能参数传递（以防止日志泄露）。

### 方法1：使用环境变量（推荐）

```powershell
# 사용자 환경변수로 영구 설정
[Environment]::SetEnvironmentVariable("KAKAO_REST_API_KEY", "your_rest_api_key_here", "User")

# 또는 현재 세션에만 임시 설정
$env:KAKAO_REST_API_KEY = "your_rest_api_key_here"
```

### 方法2：使用配置文件

创建`skills/kakao-local/data/config.json`文件：

```json
{
  "api_key": "your_rest_api_key_here"
}
```

**⚠️ 注意**：请将`config.json`文件添加到`.gitignore`列表中，以避免其被包含在提交中。

## API密钥的获取方法

1. 访问[Kakao Developers](https://developers.kakao.com/)网站
2. 点击“我的应用” → “添加应用”
3. 复制“应用密钥”中的REST API密钥

## Skill功能

### 1. NormalizeAddress（地址规范化）

该功能用于将用户输入的地址进行规范化处理，将其转换为街道名/门牌号格式以及对应的坐标。

**API接口**：`GET https://dapi.kakao.com/v2/local/search/address.json`

**输入参数**：
- `-Action "NormalizeAddress"`（必选）
- `-Query "输入的地址字符串"`（必选）
- `-Size 3`（可选，默认值：3）

**输出格式**：
```json
{
  "ok": true,
  "action": "NormalizeAddress",
  "query": "서울 강남구 테헤란로 152",
  "count": 2,
  "candidates": [
    {
      "roadAddress": "서울 강남구 테헤란로 152",
      "jibunAddress": "서울 강남구 역삼동 737",
      "x": "127.036557561809",
      "y": "37.4985995780801",
      "region": {
        "region1": "서울",
        "region2": "강남구",
        "region3": "역삼동"
      },
      "buildingName": "강남파이낸스센터",
      "zoneNo": "06236"
    }
  ],
  "raw": {}
}
```

**使用示例**：
```powershell
.\scripts\kakao_local.ps1 -Action NormalizeAddress -Query "판교역로 235"
.\scripts\kakao_local.ps1 -Action NormalizeAddress -Query "서울 강남구" -Size 5
```

### 2. SearchPlace（关键词地点搜索）

根据关键词搜索地点。支持基于位置的半径搜索和类别筛选。

**API接口**：`GET https://dapi.kakao.com/v2/local/search/keyword.json`

**输入参数**：
- `-Action "SearchPlace"`（必选）
- `-Query "搜索关键词"`（必选）
- `-Size 5`（可选，默认值：5，最大值：15）
- `-Page 1`（可选，默认值：1，最大值：45）
- `-X "127.027"`（可选，中心经度）
- `-Y "37.498"`（可选，中心纬度）
- `-Radius 1000`（可选，搜索半径（米），最大值：20000）
- `-CategoryGroupCode "CE7"`（可选，类别组代码）

**类别组代码**：
- MT1：大型购物中心
- CS2：便利店
- PS3：幼儿园、托儿所
- SC4：学校
- AC5：补习班
- PK6：停车场
- OL7：加油站、充电站
- SW8：地铁站
- BK9：银行
- CT1：文化设施
- AG2：中介公司
- PO3：公共机构
- AT4：旅游景点
- AD5：住宿设施
- FD6：餐厅
- CE7：咖啡馆
- HP8：医院
- PM9：药店

**输出格式**：
```json
{
  "ok": true,
  "action": "SearchPlace",
  "query": "대형카페",
  "count": 5,
  "totalCount": 128,
  "isEnd": false,
  "items": [
    {
      "id": "8739036",
      "name": "스타벅스 강남점",
      "roadAddress": "서울 강남구 테헤란로 152",
      "jibunAddress": "서울 강남구 역삼동 737",
      "x": "127.036557561809",
      "y": "37.4985995780801",
      "phone": "02-1234-5678",
      "categoryName": "음식점 > 카페",
      "placeUrl": "http://place.map.kakao.com/8739036",
      "distance": "245"
    }
  ],
  "raw": {}
}
```

**使用示例**：
```powershell
# 기본 검색
.\scripts\kakao_local.ps1 -Action SearchPlace -Query "대형카페"

# 개수 지정
.\scripts\kakao_local.ps1 -Action SearchPlace -Query "브런치 맛집" -Size 10

# 위치 기반 반경 검색
.\scripts\kakao_local.ps1 -Action SearchPlace -Query "카페" -X "127.027" -Y "37.498" -Radius 1000

# 카테고리 필터링
.\scripts\kakao_local.ps1 -Action SearchPlace -Query "카페" -CategoryGroupCode "CE7" -Size 15

# 페이지네이션
.\scripts\kakao_local.ps1 -Action SearchPlace -Query "주차 가능한 카페" -Page 2 -Size 10
```

## 错误处理

### 未设置API密钥
```json
{
  "ok": false,
  "errorType": "MissingApiKey",
  "message": "Set KAKAO_REST_API_KEY env var or create config.json",
  "setupGuide": "https://developers.kakao.com/"
}
```

### API密钥错误（401/403）
```json
{
  "ok": false,
  "errorType": "InvalidApiKey",
  "message": "Invalid or expired API key",
  "statusCode": 401
}
```

### API调用失败
```json
{
  "ok": false,
  "errorType": "ApiError",
  "message": "Failed to call Kakao API",
  "details": "..."
}
```

### 没有找到结果
```json
{
  "ok": true,
  "action": "SearchPlace",
  "query": "존재하지않는장소12345",
  "count": 0,
  "items": []
}
```

## 集成示例（适用于上级代理/聊天机器人）

```powershell
# 주소 정규화 후 즐겨찾기 저장
$result = .\skills\kakao-local\scripts\kakao_local.ps1 -Action NormalizeAddress -Query "홍대입구역"
$data = $result | ConvertFrom-Json

if ($data.ok -and $data.count -gt 0) {
    $best = $data.candidates[0]

    # 즐겨찾기에 추가
    $places = Get-Content ".\skills\kakao-local\data\places.json" -Raw | ConvertFrom-Json
    $places | Add-Member -NotePropertyName "홍대" -NotePropertyValue @{
        roadAddress = $best.roadAddress
        x = $best.x
        y = $best.y
        savedAt = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    } -Force
    $places | ConvertTo-Json -Depth 10 | Out-File ".\skills\kakao-local\data\places.json" -Encoding UTF8

    Write-Host "✅ 즐겨찾기 저장: 홍대 → $($best.roadAddress)"
}

# 장소 검색 후 상위 3개 추천
$result = .\skills\kakao-local\scripts\kakao_local.ps1 -Action SearchPlace -Query "주차 가능한 카페" -Size 10
$data = $result | ConvertFrom-Json

if ($data.ok -and $data.count -gt 0) {
    Write-Host "`n🌟 추천 장소 TOP 3:"
    $top3 = $data.items | Select-Object -First 3
    $index = 1
    foreach ($place in $top3) {
        Write-Host "`n[$index] $($place.name)"
        Write-Host "    📍 $($place.roadAddress)"
        Write-Host "    📞 $($place.phone)"
        Write-Host "    🔗 $($place.placeUrl)"
        $index++
    }

    # 캐시에 저장 (중복 검색 방지)
    $cache = @{
        query = $data.query
        timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        ttl = 3600  # 1시간
        results = $data.items
    }
    $cache | ConvertTo-Json -Depth 10 | Out-File ".\skills\kakao-local\data\cache.json" -Encoding UTF8
}
```

## 测试场景

### 1. 地址规范化测试
```powershell
.\scripts\kakao_local.ps1 -Action NormalizeAddress -Query "서울 강남구 테헤란로 152"
# 기대: 도로명/지번 주소와 좌표 출력
```

### 2. 地点搜索测试
```powershell
.\scripts\kakao_local.ps1 -Action SearchPlace -Query "대형카페" -Size 5
# 기대: 5개 카페 목록 출력
```

### 3. 未设置API密钥的测试
```powershell
# 환경변수 임시 제거
$backup = $env:KAKAO_REST_API_KEY
$env:KAKAO_REST_API_KEY = $null

.\scripts\kakao_local.ps1 -Action SearchPlace -Query "카페"
# 기대: {"ok": false, "errorType": "MissingApiKey", ...}

# 복구
$env:KAKAO_REST_API_KEY = $backup
```

### 使用错误的API密钥的测试
```powershell
$env:KAKAO_REST_API_KEY = "invalid_key_12345"
.\scripts\kakao_local.ps1 -Action SearchPlace -Query "카페"
# 기대: {"ok": false, "errorType": "InvalidApiKey", ...}
```

## 文件结构

```
skills/kakao-local/
  ├── SKILL.md                    # 이 파일 (스킬 명세)
  ├── README.md                   # Quick Start
  ├── .gitignore                  # config.json 보호
  ├── scripts/
  │   └── kakao_local.ps1         # 메인 스킬 스크립트
  └── data/
      ├── config.json.template    # API Key 설정 템플릿
      ├── places.json             # 즐겨찾기 (선택)
      └── cache.json              # 검색 캐시 (선택)
```

## 许可证

本技能遵循MIT许可证。

---

## 发布安全注意事项

此技能的打包方式为“纯文本”格式：脚本源代码被嵌入到`references/`目录下的Markdown文件中。

**如何在本地使用该技能**：
1. 将`references/kakao_local.ps1.md`文件的内容复制到`scripts/kakao_local.ps1`文件中。
2. 将`references/config.json.template.md`文件的内容复制到`data/config.json.template`文件中。
3. 通过环境变量`KAKAO_REST_API_KEY`设置API密钥（推荐方式），或创建`data/config.json`文件（该文件会被`.gitignore`忽略）。