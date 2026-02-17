---
name: peaq-robotics
description: 通过启动 ROS 2 节点并调用相关服务来控制 peaq-robotics-ros2（例如：创建/读取数据、添加/读取存储内容、访问控制、连接 USDT 等）。当请求中提到 peaq ROS2、机器人 DID、区块链存储、访问权限、连接 USDT 或 ROS 2 服务调用时，请使用此方法。
---
# Peaq ROS 2 集成

## 概述

使用此技能，可以通过启动 ROS 2 节点并调用其服务来操作 peaq-robotics-ros2 工作空间，以实现身份验证、存储、访问控制以及 USDT 转换等功能。

## 安装和共享（第一步）

1. **决定其他代理如何安装此技能：**
   - **同一主机上共享：** 将此文件夹放置在 `~/.openclaw/skills/peaq-robotics`，以便主机上的所有代理都能看到它。
   - **按工作空间划分：** 将其放置在 `<workspace>/skills/peaq-robotics`。
   - **远程代理：** 将其发布到 ClawHub/ClawdHub，或传输打包好的 `peaq-robotics.skill` 文件。

2. **安装 peaq-robotics-ros2 仓库**（默认从 `https://github.com/peaqnetwork/peaq-robotics-ros2` 安装到 `~/peaq-robotics-ros2`）。此操作会自动将 `peaq_robot.example.yaml` 复制到 `peaq_robot.yaml`，并固定主网 WSS，同时自动运行 `colcon build --symlink-install`：
   - `{baseDir}/scripts/peaq_ros2.sh install`
   - **可选的固定版本：** `{baseDir}/scripts/peaq_ros2.sh install --ref <tag|commit>`
   - **更新现有克隆：** `{baseDir}/scripts/peaq_ros2.sh install --update`
   - **如果希望稍后构建，则跳过构建：** `{baseDir}/scripts/peaq_ros2.sh install --skip-build`

**要求：** 主机上需要安装 ROS 2 和 `colcon`（安装器使用默认的 `ROS_SETUP`，位于 `/opt/ros/humble/setup.bash`）。

**安装器安全注意事项：**
   - 仅接受 `origin` 指向官方 `peaqnetwork/peaq-robotics-ros2` 仓库的现有克隆。
   - 安装器不会修改上游源代码。
   - 为了可重复的安装，请使用 `--ref` 参数固定一个已知的标签/提交。
   - 默认情况下，设置脚本仅从受信任的来源（`/opt/ros`、`<PEAQ_ROS2_ROOT>/install`）获取配置。如需允许自定义配置来源，请设置 `PEAQ_ROS2_TRUSTED_SETUP_ROOTS`（CSV 格式）或 `PEAQ_ROS2_TRUST_SETUP_OVERRIDES=1`。

**网络配置：**
   - `PEAQ_ROS2_NETWORK_PRIMARY`（默认为 `wss://quicknode3.peaq.xyz`）
   - `PEAQ_ROS2_NETWORK_FALLBACKS`（CSV 格式，默认为 `wss://quicknode1.peaq.xyz,wss://quicknode2.peaq.xyz,wss://peaq.api.onfinality.io/public-ws,wss://peaq-rpc.publicnode.com`）
   - 如果主网络失败，`core-configure` 会自动重试并切换网络。
   - 设置 `PEAQ_ROS2_PIN_NETWORK=0` 可以保持配置网络不变。

**钱包路径：**
   - `PEAQ_ROS2_WALLET_PATH`（可选）用于在安装过程中设置钱包路径。默认值为 `~/.peaq_robot/wallet.json`。

3. **通过 OpenClaw 技能配置环境变量**，以确保所有代理使用相同的 ROS 2 工作空间：
   - `PEAQ_ROS2_ROOT`：peaq-robotics-ros2 仓库的根目录。
   - `PEAQ_ROS2_CONFIG_YAML`：配置文件的路径。
   - `ROS_DOMAIN_ID`（可选）：用于 ROS 2 域名隔离。
   - `PEAQ_ROS2_LOG_DIR` 和 `PEAQ_ROS2_PID_DIR`（可选）：用于覆盖默认值（后缀为 `-<ROS_DOMAIN_ID>`）。

**注意：** 如果从包含 `AGENTS.md`/`TOOLS.md` 的 OpenClaw 工作空间调用此技能，并且未设置 `PEAQ_ROS2_CONFIG_YAML`，辅助工具会自动在工作空间 `<workspace>/.peaq_robot/` 下创建一个配置文件 `peaq_robot.yaml`，并使用工作空间特有的钱包（`<workspace>/.peaq_robot/wallet.json`）。同时，会为每个工作空间自动分配一个稳定的 `ROS_DOMAIN_ID`（范围在 100–199 之间），以避免冲突。

4. **确保代理可以运行 `ros2` 命令并访问已构建的工作空间。** 如果使用沙箱环境，请在已经包含 ROS 2 和 peaq-robotics-ros2 工作空间的专用容器中运行。

### 邀请消息模板（复制/粘贴）

**ClawHub/ClawdHub 安装（适用于远程代理）：**
```
clawhub install peaq-robotics && ~/.openclaw/skills/peaq-robotics/scripts/peaq_ros2.sh install
```

**同一主机上的共享安装：**
```
cp -R /path/to/peaq-robotics ~/.openclaw/skills/peaq-robotics && ~/.openclaw/skills/peaq-robotics/scripts/peaq_ros2.sh install
```

安装技能后，请重启 OpenClaw 会话。

## 引导代理（资金来源）

1. **确保 ROS 2 工作空间已构建，并且您有一个配置文件（通常是 `peaq_ros2_examples/config/peaq_robot.yaml`）。**
2. **启动核心节点并激活它：**
   - `{baseDir}/scripts/peaq_ros2.sh core-start`
   - `{baseDir}/scripts/peaq_ros2.sh core-configure`
   - `{baseDir}/scripts/peaq_ros2.sh core-activate`

3. **获取钱包地址和 DID（将地址发送给自己以进行资金注入）：**
   - `{baseDir}/scripts/peaq_ros2.sh core-address`
   - `{baseDir}/scripts/peaq_ros2.sh core-did`

4. **使用 PEAQ 代币为该地址提供资金。** 这将成为新代理的资金来源。

## 新代理的入职流程

1. **安装此技能（使用共享主机路径、工作空间路径或 ClawHub/ClawdHub）。**
2. **通过技能配置设置 `PEAQ_ROS2_ROOT` 和 `PEAQ_ROS2_CONFIG_YAML`。**
3. **启动核心节点并完成配置和激活。**
4. **运行 `{baseDir}/scripts/peaq_ros2.sh core-address`，请求引导代理为其提供资金。**
5. **资金注入完成后，运行 `{baseDir}/scripts/peaq_ros2.sh did-create '{"type":"robot"}'`。

### 核心引导（用户友好型）**
```
~/.openclaw/skills/peaq-robotics/scripts/peaq_ros2.sh core-start && \
~/.openclaw/skills/peaq-robotics/scripts/peaq_ros2.sh core-configure && \
~/.openclaw/skills/peaq-robotics/scripts/peaq_ros2.sh core-activate
```

**单独使用 `fund-request` 命令请求资金。**

### 资金请求模板（复制/粘贴）
```
peaq-robotics funding request:
address: <PASTE_CORE_ADDRESS>
reason: initial DID creation + storage/access ops
amount: <AMOUNT> PEAQ
```

### 资金转移（代理之间）**

**使用已提供资金的代理向新代理转移 PEAQ：**
- **检查余额：** `{baseDir}/scripts/peaq_ros2.sh balance [address]`
- **向另一个代理转账：** `{baseDir}/scripts/peaq_ros2.sh fund <to_address> <amount>`
- **生成请求：** `{baseDir}/scripts/peaq_ros2.sh fund-request [amount] [reason]`

**注意事项：**
- `fund` 命令使用配置文件中的 `wallet.path` 指定的本地代理钱包。
- `fund` 和 `tether-usdt-transfer` 命令默认是禁用的；在运行资金转移之前，请设置 `PEAQ_ROS2_ENABLE_TRANSFERS=1`。
- 默认金额单位为 PEAQ；可以使用 `--planck` 传递原始的 Planck 单位。
- 如果资金转移返回临时 WebSocket 错误，脚本会在失败前检查余额变化。
- 当未配置 Pinata 时（`storage.mode` 缺失或 `pinata jwt` 为空），存储桥接默认使用本地 IPFS。

### 一键式资金请求（复制/粘贴）
```
peaq-robotics fund-request: address=<ADDRESS> amount=<AMOUNT> PEAQ reason="DID + storage init"
```

### 自动通知资金提供者（代理之间）

**如果您知道资金提供者的代理 ID，可以使用 OpenClaw 的代理间通信工具发送请求：**
1. **生成请求行：** `{baseDir}/scripts/peaq_ros2.sh fund-request [amount] [reason]`
2. **通过 `sessions_send` 将请求发送给资金提供者代理。**

### 代理间的通信（使用 OpenClaw）**

代理可以通过 OpenClaw 会话进行通信：
1. **创建另一个代理：** `openclaw agents add <agent-id> --workspace <dir> --non-interactive`
2. **发送消息：** `openclaw agent --agent <agent-id> --message "<your message>"`

**使用此方法将 `fund-request` 请求发送给资金提供者代理。**

## 身份卡（与 DID 关联的联系记录）**

使用身份卡将 DID 变为可操作的代理联系记录（包括名称、角色和端点）。这些信息在创建 DID 时会被嵌入其中。

- **生成 JSON 文件：** `{baseDir}/scripts/peaq_ros2.sh identity-card-json [name] [roles_csv] [endpoints_json] [metadata_json]`
- **使用身份卡元数据创建 DID：** `{baseDir}/scripts/peaq_ros2.sh identity-card-did-create [name] [roles_csv] [endpoints_json] [metadata_json]`
- **从 DID 读取身份卡信息：** `{baseDir}/scripts/peaq_ros2.sh identity-card-did-read`

**身份卡 JSON 的格式：**
```
{
  "schema": "peaq.identityCard.v1",
  "name": "Agent Name",
  "roles": ["funder", "operator"],
  "endpoints": {"openclaw": {"agentId": "funder"}},
  "metadata": { "any": "extra fields" }
}
```

**注意事项：**
- `name` 默认为 OpenClaw 代理 ID（如果可用），否则使用主机名。
- 对于现有的 DID，ROS2 核心服务不支持更新（仅支持创建）。

## 核心工作流程

### 启动节点（常见操作）

1. **启动并激活核心节点：**
   - `{baseDir}/scripts/peaq_ros2.sh core-start`
   - `{baseDir}/scripts/peaq_ros2.sh core-configure`
   - `{baseDir}/scripts/peaq_ros2.sh core-activate`

**核心节点激活后，单独运行 `fund-request` 命令。**

2. **可选节点：**
   - **存储桥接：** `{baseDir}/scripts/peaq_ros2.sh storage-start`
   - **事件节点：** `{baseDir}/scripts/peaq_ros2.sh events-start`
   - **Tether 节点：** `{baseDir}/scripts/peaq_ros2.sh tether-start`（需要 tether 配置以及 `peaq_ros2_tether/js` 中的 npm 安装）
   - **人形机器人桥接：** `{baseDir}/scripts/peaq_ros2.sh humanoid-start`

### 调用服务**

使用辅助脚本的子命令来调用常见服务：
- **创建 DID（如果省略，则默认类型为 "robot"）：** `{baseDir}/scripts/peaq_ros2.sh did-create`
- **使用元数据 JSON 或完整的 DID 文档创建 DID：** `{baseDir}/scripts/peaq_ros2.sh did-create '{"type":"robot"}`
- **从文件创建 DID：** `{baseDir}/scripts/peaq_ros2.sh did-create @/path/to/did_doc.json`
- **读取 DID：** `{baseDir}/scripts/peaq_ros2.sh did-read`
- **存储数据：** `{baseDir}/scripts/peaq_ros2.sh store-add sensor_data '{"temp":25.5}' FAST`
- **读取数据：** `{baseDir}/scripts/peaq_ros2.sh store-read sensor_data`
- **访问控制：** `{baseDir}/scripts/peaq_ros2.sh access-create-role operator 'Robot operator'`

**注意事项：**
- `did-create` 命令将包含 DID 字段（`id`、`controller`、`services`、`verificationMethods` 等）的 JSON 视为完整的 DID 文档。
- 纯元数据 JSON 会被封装到 DID 的 `services` 字段中（类型为 `peaqMetadata`），以便在链上保存。
- 在每次服务调用之前（`did-create`、`store-add`、身份卡元数据），都会对 JSON 输入进行验证。
- 服务负载会被序列化为 JSON 对象（而不是 shell 构建的 YAML 字符串），从而降低用户提供内容带来的注入风险。
- 输入路径 `@/path/file.json` 仅限于允许的根目录（`skill folder`、`PEAQ_ROS2_ROOT` 和工作空间 `.peaq_robot`）；可以通过 `PEAQ_ROS2_JSON_ALLOWED_ROOTS` 设置额外的根目录。

**有关完整的服务/参数映射和原始 ROS 2 主题/服务名称，请参阅 `references/peaq_ros2_services.md`。**

## 安全性和防护措施**

- 在执行任何可能产生链上费用或实际资金操作的步骤之前，请务必确认。
- **切勿通过 ROS 2 服务传递私钥或助记词**；Tether 操作仅使用地址进行调用。
- 钱包密钥应保持本地存储。辅助脚本避免在命令行中打印或传递助记词。
- 如果在同一主机上运行多个 ROS 2 图谱，请为每个环境设置不同的 `ROS_DOMAIN_ID` 以避免冲突。

## 参考资料**

- **服务映射：** `references/peaq_ros2_services.md`