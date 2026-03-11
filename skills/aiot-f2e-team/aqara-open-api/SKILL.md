---
name: aqara-open-api
description: 通过 Aqara Open Platform API（HTTP JSON）查询和控制 Aqara/Lumi Studio 智能家居设备，并管理各个空间。当用户需要列出 Aqara 设备、获取设备状态、控制灯光/开关/传感器或管理房间/空间时，可以使用该功能。需要使用 `AQARA_OPEN_API_TOKEN` 和 `AQARA_ENDPOINT_URL`。
version: 1.0.1
author: aqara
homepage: https://opendoc.aqara.com
metadata: {"clawdbot":{"emoji":"🏠","requires":{"bins":["jq","curl"],"env":["AQARA_ENDPOINT_URL","AQARA_OPEN_API_TOKEN"]}}}
---
# Aqara Open API 技能

该技能使代理能够通过 HTTPS 请求访问 Aqara Open Platform API 来操作 Aqara/Lumi Studio 智能家居设备。**所有操作均通过 `curl` 命令执行**，`GetAllDevicesWithSpaceRequest` 除外，该请求必须通过 `bash scripts/fetch_all_devices.sh` 脚本来执行，以便刷新本地缓存文件 `data/devices.json`。

该技能仅支持以下功能：
- 设备发现和设备类型查询
- 从缓存中查询设备状态
- 设备控制
- 空间创建、更新以及设备分配

## 配置
需要以下环境变量：
- `AQARA_ENDPOINT_URL`：基础 URL
- `AQARA_OPEN_API_TOKEN`：您的长期有效访问令牌

## AI 快速导航（请先阅读此部分）

> 本部分仅用于导航和执行总结。它**不会添加新规则**或更改现有限制。

### 该技能的功能

- **设备发现**：加载所有设备、空间映射、端点、功能、特性以及当前值
- **设备类型目录**：查询项目中所有设备类型及其代码和显示名称
- **设备查询**：按类型、名称、房间/空间或在线状态进行过滤；读取当前特性值
- **设备控制**：使用从缓存中获取的 `deviceId`、`endpointId`、`functionCode` 和 `traitCode` 来发送控制请求
- **空间管理**：列出空间、创建空间、更新空间以及将设备分配到空间

### 最快路径的意图

- **列出所有设备 / 按类型列出设备 / 列出房间内的设备 / 获取设备状态**
  - 检查 `data/devices.json`
  - 如果缓存存在：读取文件
  - 如果缓存缺失：运行 `bash scripts/fetch_all_devices.sh`
- **控制设备**
  - 确保 `data/devices.json` 存在
  - 从缓存中读取 `deviceId + endpointId + functionCode + traitCode`
  - 然后使用 `bash + curl` 来执行 `ExecuteTraitRequest`
- **有哪些设备类型？**
  - 使用 `bash + curl` 来执行 `GetDeviceTypeInfosRequest`
- **刷新所有设备数据**
  - 仅运行 `bash scripts/fetch_all_devices.sh`
- **列出空间**
  - 使用 `bash + curl` 来执行 `GetSpacesRequest`
- **创建或更新空间**
  - 首先从 `GetSpacesRequest` 中获取 `spaceId`
  - 然后调用 `CreateSpaceRequest` 或 `UpdateSpaceRequest`
- **将设备分配到空间**
  - 首先从 `GetSpacesRequest` 中获取 `spaceId`
  - 从 `data/devices.json` 中读取 `deviceId` 值
  - 然后调用 `AssociateDevicesToSpaceRequest`

### 六条最高优先级的规则

1. **所有设备加载仅通过脚本进行**：`GetAllDevicesWithSpaceRequest` 只能通过 `bash scripts/fetch_all_devices.sh` 来执行。
2. **所有其他请求仅通过 curl 进行**：除了上述刷新脚本外，其他所有 API 调用都必须使用 `bash + curl`。
3. **请求体只能包含四个字段**：`type`、`version`、`msgId` 和 `data`；`version` 必须始终为 `"v1"`。
4. **`type` 仅限于白名单中的类型**：仅使用本文档中列出的请求类型；切勿尝试猜测其他类型，如 `GetAllSpacesRequest`、`GetSpaceListRequest` 或 `QuerySpaceListRequest`。
5. **所有 ID 和代码必须来自真实的 API 数据**：切勿猜测 `deviceId`、`endpointId`、`functionCode`、`traitCode` 或 `spaceId`。

### 必要的前提条件

- **在列出设备、读取状态或按房间/类型过滤之前**：检查 `data/devices.json` 是否存在
- **在控制设备之前**：从缓存文件中获取 `deviceId`、`endpointId`、`functionCode` 和 `traitCode`
- **在创建或更新空间之前**：如果需要 `spaceId`，请先调用 `GetSpacesRequest`
- **在将设备分配到空间之前**：从 `GetSpacesRequest` 中获取 `spaceId`，并从 `data/devices.json` 中获取 `deviceId` 值

### 术语和字段参考

- **缓存文件**：`data/devices.json`，其中存储了 `GetAllDevicesWithSpaceRequest` 返回的 `data` 数组
- **deviceId**：用于控制和空间分配的设备标识符
- **endpointId**：端点标识符，仅来自缓存的 `endpoints[].endpointId`
- **functionCode / traitCode**：来自缓存的特性标识符
- **spaceId**：来自 `GetSpacesRequest` 或缓存的 `space.spaceId`

### 部分索引

- **协议和四字段请求体**：请参阅 `## API 协议`
- **脚本与 curl 执行规则**：请参阅 `### 执行模型`
- **缓存文件规则**：请参阅 `### 文件缓存模型（缓存优先数据模型）`
- **设备 API**：请参阅 `### 设备管理` 下的 `## API 命令`
- **空间 API**：请参阅 `### 空间管理`
- **标准操作流程**：请参阅 `## 标准操作程序 (SOP)`
- **决策树**：请参阅 `## 缓存决策树` 和 `## API 调用决策树`
- **禁止的行为**：请参阅 `## 禁止的行为`
- **特性代码参考**：请参阅 `references/trait-codes.md`

## 1. 角色和核心理念

**角色**：您是一个严格的硬件接口控制器。切勿推断或猜测 ID 或特性字段。

## 2. 硬性安全规则

### 2.1 有效值规则

任何涉及设备实时状态的操作（如电源、亮度或温度）都必须遵循此规则：

| 电源状态 | 有效解释 | 响应方式 |
|-------------|----------------------|----------------|
| `Switch == "false"` | 亮度/色温/电源应视为 0 或 "关闭" | "设备当前处于关闭状态" |
| `Switch == "true"` | 使用实际返回的值 | "亮度为 X%" |

**切勿** 产生逻辑上不一致的输出，例如“灯是关闭的，但亮度为 100%”。

## 快速入门（操作员）

1. 设置环境变量：
- `AQARA_OPEN_API_TOKEN`：您的 Aqara Open API 令牌（JWT）
- `AQARA_ENDPOINT_URL`：API 基础 URL

**实际环境值规则**：`AQARA_ENDPOINT_URL` 和 `AQARA_OPEN_API_TOKEN` **必须从运行时环境读取**（通过 `$AQARA_ENDPOINT_URL` 和 `$AQARA_OPEN_API_TOKEN`）。**切勿猜测、伪造或使用示例占位符** 作为真实的请求值。如果任一变量缺失或为空，请告知用户先进行配置。

2. 测试连接：

```bash
curl -s -X POST "$AQARA_ENDPOINT_URL" \
  -H "Authorization: Bearer $AQARA_OPEN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"GetAllDevicesWithSpaceRequest","version":"v1","msgId":"test-1"}'
```

## API 协议

基础 URL：`$AQARA_ENDPOINT_URL`

所有请求都使用 **统一的 POST 端点**。路由由 JSON 正文中的 `type` 字段决定。

### 请求包

请求正文 JSON 可以包含 **恰好这 4 个字段**。请勿添加、删除或替换字段：

```json
{
  "type": "<RequestType>",
  "version": "v1",
  "msgId": "<unique-id>",
  "data": { ... }
}
```

| 字段 | 是否必需 | 含义 | 禁止的行为 |
|------|----------|---------|--------------------|
| `type` | 是 | API 方法名称，例如 `ExecuteTraitRequest` 或 `GetSpacesRequest` | 请勿修改、缩写或用文档中未列出的值替换 |
| `version` | 是 | **必须为字符串 `"v1"`** | 请勿省略；请勿使用 `"v2"`、`1.0` 或其他值 |
| `msgId` | 是 | 唯一的请求标识符，例如 `"msg-1234567890"` | 无 |
| `data` | 是 | 选定 `type` 的有效载荷（根据请求可能是 `null`、对象、数组或字符串） | 仅使用文档中定义的结构或 `references/` 中的内容 |

**严格的请求体约束**

1. **必须包含 `version`**：每个 curl 请求正文都必须包含 `"version":"v1"`。
2. **不得添加未定义的字段**：请求正文 **只能** 包含这 4 个键。请勿添加 `senderId`、`source`、`timestamp` 或文档中未定义的任何字段。
3. **不得发明字段名称或结构**：无论是顶级正文还是 `data`，都不得包含自创的字段或未记录的结构。
4. **不得发明或尝试使用替代的 `type` 值**：如果文档中指定的请求类型是 `GetSpacesRequest`，则 `type` 必须是 `GetSpacesRequest`。
5. **不得使用同义词或变体来代替 `type`**：除非文档中明确列出，否则禁止使用诸如 `GetAllSpacesRequest`、`GetSpaceListRequest`、`QuerySpaceListRequest`、`ListSpacesRequest` 等自创的名称。

### 必需的头部信息

```
Authorization: Bearer $AQARA_OPEN_API_TOKEN
Content-Type: application/json
```

### 响应包

```json
{
  "type": "<ResponseType>",
  "version": "v1",
  "msgId": "<matching-id>",
  "code": 0,
  "message": null,
  "data": { ... }
}
```

`code: 0` = 成功。非零 = 错误。常见错误代码：
- 400：参数无效
- 1001：令牌过期
- 2030：设备未找到

### curl 模板

每个 curl 请求的 `-d` 值必须是一个 JSON 对象，其中包含 **仅 4 个键**：`type`、`version`、`msgId` 和 `data`。将 `<TYPE>` 替换为 API 方法名称，将 `<DATA>` 替换为正确的有效载荷：

```bash
curl -s -X POST "$AQARA_ENDPOINT_URL" \
  -H "Authorization: Bearer $AQARA_OPEN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"<TYPE>","version":"v1","msgId":"msg-'$(date +%s)'","data":<DATA>}'
```

始终在 `-d` 中保持 `"version":"v1"`，并且切勿添加 `senderId` 或文档中未定义的任何其他字段。

## 代理应如何使用此技能

### 执行模型

**必须遵循的执行规则**：

- **仅 `GetAllDevicesWithSpaceRequest`**：通过 **`bash scripts/fetch_all_devices.sh`** 来执行。该脚本调用 API 并将响应写入 `data/devices.json`。请勿直接使用 curl 调用此请求。
- **所有其他支持的 API 请求**（如 `ExecuteTraitRequest`、`GetSpacesRequest`、`CreateSpaceRequest`、`UpdateSpaceRequest` 和 `AssociateDevicesToSpaceRequest`）：使用 `bash + curl` 来执行。JSON 正文必须包含 **恰好 4 个键**：`type`、`version`、`msgId` 和 `data`。
- **不要尝试重复相同的 `type` 请求**：当请求失败时，不要尝试类似类型的请求。请验证文档中规定的 `type`、有效载荷格式、令牌、ID、缓存和所需的前提条件，然后仅在适当的情况下重新尝试相同的请求。

### 文件缓存模型（缓存优先数据模型）

**本地缓存文件**

- `data/devices.json` — 来自 `GetAllDevicesWithSpaceRequest` 的 `data` 数组，包括完整的设备信息：`deviceId`、`name`、`deviceTypesList`、`state`、`space`、`endpoints` 以及所有 `functions/traits/current values`

**刷新缓存（创建/覆盖缓存文件）**

```bash
bash scripts/fetch_all_devices.sh
```

**必须遵循的使用规则**

1. **首先读取缓存**：当用户请求设备列表、设备类型、房间映射或基本设备信息时，检查 `data/devices.json` 是否存在且非空。
2. **缓存命中**：如果缓存文件存在，请**直接读取文件** 并继续操作。请勿再次调用 `GetAllDevicesWithSpaceRequest`。
3. **缓存未命中 / 文件缺失 / 解析失败**：运行 `bash scripts/fetch_all_devices.sh` 以刷新缓存。刷新后，请**重新读取缓存文件** 再继续操作。
4. **用户明确请求刷新**：运行 `bash scripts/fetch_all_devices.sh`，然后重新读取文件。
5. **控制命令**（`ExecuteTraitRequest`）仍然通过 curl 直接发送到 API，但所有 `deviceId` / `endpointId` / `functionCode` / `traitCode` 值 **必须来自缓存文件**。

### 关键数据规则

**切勿猜测、伪造或推断** `deviceId`、`endpointId`、`functionCode` 或 `traitCode`。控制调用中使用的每个值 **必须** 来自缓存的 `data/devices.json` 文件。
- `endpointId` 必须来自设备的 `endpoints[].endpointId`。
- `functionCode` 和 `traitCode` 必须来自 `endpoints[].functions[].traits[]`。
- `value` 类型必须与特性定义相匹配。

### 本地过滤（无需额外 API 调用）

当用户请求设备的子集（例如，所有灯、卧室中的设备或在线开关）时：
- **在本地通过 `deviceTypesList`、`name`、`state` 或 `space.name` / `space.spatialMarking` 对缓存的 `data/devices.json` 进行过滤**。
- **请勿** 发起新的 API 调用来进行过滤。

### 设备类型与设备名称

- **按类型（推荐）**：当用户请求灯或开关时，通过 `deviceTypesList` 在缓存文件中过滤。
- **按名称（备用）**：仅使用设备名称从缓存列表中选择特定设备。

### 错误处理

- 对于代码 1001（令牌过期）或 400（参数错误）的错误：重新检查令牌，验证所有 ID 是否来自缓存的设备数据。
- 对于 2030：设备未找到；运行 `bash scripts/fetch_all_devices.sh` 以刷新缓存并重试。
- 超时/网络错误：重试一次，然后报告。
- 缓存文件解析错误：删除 `data/devices.json` 并运行 `bash scripts/fetch_all_devices.sh` 以重新生成。

## API 命令（共 7 个）

### 设备管理

#### 获取包含空间信息的所有设备 — `GetAllDevicesWithSpaceRequest`

一次性检索所有智能家居设备，包括完整的设备信息、空间分配、端点、功能、特性以及当前值。无需 `data` 字段（或 `data: null`）。

代理 **必须** 将此响应写入本地缓存文件（`data/devices.json`），并使用缓存进行后续的设备查询、状态检查以及控制命令。使用提供的脚本来获取和缓存数据：

```bash
bash scripts/fetch_all_devices.sh
```

手动 curl（仅供参考 — 建议使用脚本）：

```bash
curl -s -X POST "$AQARA_ENDPOINT_URL" \
  -H "Authorization: Bearer $AQARA_OPEN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"GetAllDevicesWithSpaceRequest","version":"v1","msgId":"msg-'$(date +%s)'"}'
```

#### 获取所有设备类型 — `GetDeviceTypeInfosRequest`

检索当前项目中可用的所有设备类型。每个条目包含一个 `deviceType` 代码及其本地化的显示名称。

```bash
curl -s -X POST "$AQARA_ENDPOINT_URL" \
  -H "Authorization: Bearer $AQARA_OPEN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"GetDeviceTypeInfosRequest","version":"v1","msgId":"msg-'$(date +%s)'"}'
```

#### 控制设备 — `ExecuteTraitRequest`

控制一个或多个设备功能，例如打开/关闭或调节亮度。`endpointId`、`functionCode` 和 `traitCode` 必须从缓存中读取。

```bash
# Turn on
curl -s -X POST "$AQARA_ENDPOINT_URL" \
  -H "Authorization: Bearer $AQARA_OPEN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"ExecuteTraitRequest","version":"v1","msgId":"msg-'$(date +%s)'","data":[{"deviceId":"<deviceId>","endpointId":<endpointId>,"functionCode":"<functionCode>","traitCode":"OnOff","value":true}]}'

# Turn off
curl -s -X POST "$AQARA_ENDPOINT_URL" \
  -H "Authorization: Bearer $AQARA_OPEN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"ExecuteTraitRequest","version":"v1","msgId":"msg-'$(date +%s)'","data":[{"deviceId":"<deviceId>","endpointId":<endpointId>,"functionCode":"<functionCode>","traitCode":"OnOff","value":false}]}'
```

### 空间管理

#### 列出空间层次结构 — `GetSpacesRequest`

检索所有空间作为层次结构树。每个空间包括其 ID、名称、父空间 ID、空间标记标签以及嵌套的子空间。

**空间请求类型规则**：空间列表的请求类型 **仅** 为 `GetSpacesRequest`。请勿尝试 `GetAllSpacesRequest`、`GetSpaceListRequest`、`QuerySpaceListRequest` 或其他猜测的变体。

```bash
curl -s -X POST "$AQARA_ENDPOINT_URL" \
  -H "Authorization: Bearer $AQARA_OPEN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"GetSpacesRequest","version":"v1","msgId":"msg-'$(date +%s)'"}'
```

#### 创建新空间 — `CreateSpaceRequest`

创建房间、区域或建筑。如果不知道父空间 ID，请省略 `parentSpaceId`。如果需要父空间 ID，请先运行 `GetSpacesRequest`。

```bash
# Top-level space
curl -s -X POST "$AQARA_ENDPOINT_URL" \
  -H "Authorization: Bearer $AQARA_OPEN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"CreateSpaceRequest","version":"v1","msgId":"msg-'$(date +%s)'","data":{"name":"Living Room","spatialMarking":"living_room"}}'

# Sub-space
curl -s -X POST "$AQARA_ENDPOINT_URL" \
  -H "Authorization: Bearer $AQARA_OPEN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"CreateSpaceRequest","version":"v1","msgId":"msg-'$(date +%s)'","data":{"name":"Bedroom","parentSpaceId":"<parentSpaceId>","spatialMarking":"bedroom"}}'
```

#### 更新空间属性 — `UpdateSpaceRequest`

更新现有空间的名称或空间标记。仅更新提供的字段。`spaceId` 是必需的。

```bash
curl -s -X POST "$AQARA_ENDPOINT_URL" \
  -H "Authorization: Bearer $AQARA_OPEN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"UpdateSpaceRequest","version":"v1","msgId":"msg-'$(date +%s)'","data":{"spaceId":"<spaceId>","name":"New Room Name"}}'
```

#### 将设备分配到空间 — `AssociateDevicesToSpaceRequest`

将一个或多个设备分配到现有空间。响应 `data` 仅包含失败的项目；为空表示所有操作均成功。

```bash
curl -s -X POST "$AQARA_ENDPOINT_URL" \
  -H "Authorization: Bearer $AQARA_OPEN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"AssociateDevicesToSpaceRequest","version":"v1","msgId":"msg-'$(date +%s)'","data":{"spaceId":"<spaceId>","deviceIds":["<deviceId1>","<deviceId2>"]}}'
```

## 标准操作程序 (SOP)

### SOP A：列出或发现设备

1. 检查 `data/devices.json` 是否存在且非空。
2. 如果存在：直接从文件中读取设备数据。
3. 如果缺失或为空：运行 `bash scripts/fetch_all_devices.sh` 以生成缓存，然后读取文件。
4. 通过过滤缓存文件来回答用户的请求。

### SOP B：查询设备状态

1. 设备状态和特性值已包含在缓存文件中。
2. 如果 `data/devices.json` 缺失，请先运行 `bash scripts/fetch_all_devices.sh`。
3. 在缓存文件中找到设备并读取相应的特性值。
4. 无需单独的 API 调用来读取设备状态。

### SOP C：控制设备

1. 如果 `data/devices.json` 缺失，请先运行 `bash scripts/fetch_all_devices.sh`。
2. 从缓存文件中读取确切的 `deviceId`、`endpointId`、`functionCode` 和 `traitCode`。
3. 使用 `ExecuteTraitRequest` 和 curl 命令，并仅使用缓存中的值。
4. 响应 `data` 仅包含失败的项目；空数组表示所有操作均成功。

### SOP D：空间管理

1. 设备到空间的关联已包含在 `data/devices.json` 中。
2. 使用 `GetSpacesRequest` 和 curl 命令来检索完整的空间层次结构树。
3. 根据需要使用 `CreateSpaceRequest`、`UpdateSpaceRequest` 或 `AssociateDevicesToSpaceRequest`。

## 缓存决策树

```
Does the user request involve devices, spaces, or types?
├── Yes → Check the local cache file `data/devices.json`
│   ├── Cache hit (file exists and is non-empty)
│   │   └── Read from the file directly and filter/aggregate locally
│   └── Cache miss / missing file
│       ├── Run `bash scripts/fetch_all_devices.sh`
│       ├── Re-read the cache file
│       └── Continue with the refreshed data
└── No → Continue with the normal flow

Does the task require device control?
├── Yes → Ensure `data/devices.json` exists (refresh first if missing)
│   ├── Read `deviceId + endpointId + functionCode + traitCode` from cache
│   └── Call `ExecuteTraitRequest` via curl
└── No → Return the cached data result

Did the user explicitly ask to refresh device data?
└── Run `bash scripts/fetch_all_devices.sh` to overwrite the cache, then re-read it
```

## API 调用决策树

```
User wants devices by type?
  → data/devices.json exists? → Yes: filter file by deviceTypesList
                               → No:  bash scripts/fetch_all_devices.sh, then filter

User wants to list/discover all devices?
  → data/devices.json exists? → Yes: return full list from file
                               → No:  bash scripts/fetch_all_devices.sh, then read

User wants state of a device?
  → data/devices.json exists? → No: bash scripts/fetch_all_devices.sh
  → Read value from file: endpoints[].functions[].traits[].value

User wants to control a device?
  → data/devices.json exists? → No: bash scripts/fetch_all_devices.sh
  → Get deviceId + endpointId + functionCode + traitCode from file
  → curl ExecuteTraitRequest with correct value type

User wants devices by space/room?
  → data/devices.json exists? → Yes: filter file by space.name / spatialMarking
                               → No:  bash scripts/fetch_all_devices.sh, then filter

User wants to refresh device data?
  → bash scripts/fetch_all_devices.sh

User wants to see spaces?
  → curl GetSpacesRequest

User wants to create, update, or assign spaces?
  → curl GetSpacesRequest if a real spaceId is needed
  → then curl CreateSpaceRequest / UpdateSpaceRequest / AssociateDevicesToSpaceRequest
```

## 禁止的行为

| 禁止的行为 | 正确的行为 |
|-----------|------------------|
| 猜测或伪造 `deviceId` | 始终使用 `data/devices.json` 缓存文件中的 ID。 |
| 猜测或创建 `endpointId` | 始终从缓存文件中的 `endpoints[].endpointId` 获取。 |
| 猜测 `functionCode` 或 `traitCode` | 始终从缓存文件中的 `endpoints[].functions[].traits[]` 获取。 |
| 在未解析设备/端点信息的情况下运行 `ExecuteTraitRequest` | 确保 `data/devices.json` 存在并使用缓存的结构。 |
| 使用 curl 调用 `GetAllDevicesWithSpaceRequest` | 仅此请求通过脚本执行：使用 `bash scripts/fetch_all_devices.sh`。 |
| 在缓存文件已存在且用户未请求刷新的情况下调用脚本或 API | 请读取 `data/devices.json`。 |
| 发起单独的 API 调用来读取设备状态/值 | 设备状态和特性值已包含在 `data/devices.json` 中。 |
| 从设备名称推断设备类型 | 通过 `deviceTypesList` 在缓存中过滤设备。 |
| 猜测 `spaceId` | 始终使用 `GetSpacesRequest` 响应或缓存中的 `space.spaceId`。 |
| 猜测或尝试未记录的请求类型值 | 仅使用文档中列出的请求名称。 |
| 在失败后尝试替代的请求名称，如 `GetAllSpacesRequest`、`GetSpaceListRequest` 或 `QuerySpaceListRequest` | 仅使用 `GetSpacesRequest` 来列出空间。 |
| 猜测或伪造 `AQARA_ENDPOINT_URL` 或 `AQARA_OPEN_API_TOKEN` | 这些必须从运行时环境读取。 |

## 文件

- `scripts/fetch_all_devices.sh` — 缓存刷新脚本；调用 `GetAllDevicesWithSpaceRequest` 并写入 `data/devices.json`
- `data/devices.json` — 由脚本生成的缓存文件；包含完整的设备数据
- `references/examples.md` — curl 调用示例
- `references/trait-codes.md` — 完整的特性代码列表，包括类型、读写权限和订阅标志

请保持 `SKILL.md` 的简洁性；详情请参阅相关参考资料。