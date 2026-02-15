---
name: dsiprouter
description: 使用 Postman 工具集（curl + jq）调用 dSIPRouter 的 REST API。
metadata: {"openclaw":{"emoji":"📡","requires":{"bins":["curl","jq"],"env":["DSIP_ADDR","DSIP_TOKEN"]}}}
---

# dSIPRouter API 技能

该技能基于 Postman 收集自动生成，提供以下功能：
- 安全的 `curl` 调用规范
- 一个名为 `bin/dsiprouter.sh` 的辅助命令行工具（CLI），其中包含用于执行收集中各项请求的子命令
- 示例请求数据（如果 Postman 中提供了相关数据）

## 所需环境变量

- `DSIP_ADDR` — 你的 dSIPRouter 节点的主机名或 IP 地址（不包含协议）
- `DSIP_TOKEN` — API 访问令牌
- 可选参数：`DSIP_INSECURE=1`（用于启用自签名 TLS 协议，此时需要在命令行中添加 `-k` 参数）

**基础 URL：**
- `https://$DSIP_ADDR:5000/api/v1`

**认证头：**
- `Authorization: Bearer $DSIP_TOKEN`

## 安全调用规范
（请参考代码块 ```bash
dsip_api() {
  local method="$1"; shift
  local path="$1"; shift

  local insecure=()
  if [ "${DSIP_INSECURE:-}" = "1" ]; then insecure=(-k); fi

  curl "${insecure[@]}" --silent --show-error --fail-with-body \
    --connect-timeout 5 --max-time 30 \
    -H "Authorization: Bearer ${DSIP_TOKEN}" \
    -H "Content-Type: application/json" \
    -X "${method}" "https://${DSIP_ADDR}:5000${path}" \
    "$@"
}
``` 以获取具体的安全调用规范）

## 建议使用方式：使用捆绑的辅助 CLI 工具
（请参考代码块 ```bash
# list subcommands
dsiprouter.sh help

# list endpoint groups
dsiprouter.sh endpointgroups:list | jq .

# create inbound mapping with your own JSON payload
dsiprouter.sh inboundmapping:create '{"did":"13132222223","servers":["#22"],"name":"Taste Pizzabar"}' | jq .

# or send the Postman sample body
dsiprouter.sh inboundmapping:create --sample | jq .
``` 以了解如何使用辅助 CLI）

## Kamailio 相关操作
（请参考代码块 ```bash
dsiprouter.sh kamailio:stats | jq .
dsiprouter.sh kamailio:reload | jq .
``` 以获取与 Kamailio 相关的 API 操作）

## 端点管理（来自 Postman 的 API 列表）

### 端点组（Endpoint Groups）
- `endpointgroups:list` → **GET** `/api/v1/endpointgroups`  
- `endpointgroups:get` → **GET** `/api/v1/endpointgroups/9` — 获取单个端点组  
- `endpointgroups:create` → **POST** `/api/v1/endpointgroups` — 创建端点组  
- `endpointgroups:create_1` → **POST** `/api/v1/endpointgroups` — 创建端点组  
- `endpointgroups:create_2` → **POST** `/api/v1/endpointgroups` — 创建端点组  
- `endpointgroups:create_3` → **POST** `/api/v1/endpointgroups` — 创建端点组  
- `endpointgroups:delete` → **DELETE** `/api/v1/endpointgroups/53` — 删除端点组  
- `endpointgroups:update` → **PUT** `/api/v1/endpointgroups/34` — 更新端点组  

### Kamailio 相关操作
- `kamailio:reload` → **POST** `/api/v1/reload/kamailio` — 在进行更改后触发 Kamailio 重新加载  
- `kamailio:list` → **GET** `/api/v1/kamailio/stats` — 获取呼叫统计信息  

### 入站映射（Inbound Mapping）
- `inboundmapping:list` → **GET** `/api/v1/inboundmapping` — 获取所有入站映射的列表  
- `inboundmapping:create` → **POST** `/api/v1/inboundmapping` — 创建新的入站映射  
- `inboundmapping:update` → **PUT** `/api/v1/inboundmapping?did=13132222223` — 更新入站映射  
- `inboundmapping:delete` → **DELETE** `/api/v1/inboundmapping?did=13132222223` — 删除入站映射  

### 租约管理（Leases）
- `leases:list` → **GET** `/api/v1/lease/endpoint?email=mack@goflyball.com&ttl=5m` — 获取单个端点组的租约信息  
- `leases:list_1` → **GET** `/api/v1/lease/endpoint?email=mack@goflyball.com&ttl=1m&type=ip&auth_ip=172.145.24.2` — 获取单个端点组的租约信息  
- `leases:revoke` → **DELETE** `/api/v1/lease/endpoint/34/revoke` — 取消某个端点组的租约  

### 运营商组（Carriergroups）
- `carriergroups:list` → **GET** `/api/v1/carriergroups`  
- `carriergroups:create` → **POST** `/api/v1/carriergroups` — 创建运营商组  

### 用户认证（Auth）
- `auth:create` → **POST** `/api/v1/auth/user`  
- `auth:update` → **PUT** `/api/v1/auth/user/2`  
- `auth:delete` → **DELETE** `/api/v1/auth/user/2`  
- `auth:list` → **GET** `/api/v1/auth/user`  
- `auth:login` → **POST** `/api/v1/auth/login`  

### CDR（Call Detail Record）管理
- `cdr:get` → **GET** `/api/v1/cdrs/endpointgroups/17?type=csv&dtfilter=2022-09-14&email=True`  
- `cdr:get_1` → **GET** `/api/v1/cdrs/endpoint/54`  

## 包含的文件
- `bin/dsiprouter.sh`