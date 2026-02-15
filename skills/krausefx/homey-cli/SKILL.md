---
name: homey-cli
description: 通过命令行界面（CLI）控制 Homey 家庭自动化中心。当您需要控制智能家居设备（如灯光、恒温器、插座等）、查看设备状态、列出区域、触发自动化流程或执行任何 Homey 自动化任务时，可以使用该方式。支持开关设备、调节亮度、更改颜色、控制温度以及检查设备状态等操作。仅允许执行安全且被系统允许的操作。
---

# Homey CLI

这是一个安全、易于使用的命令行工具（CLI），用于控制 Homey 家庭自动化系统。

## 该工具的功能

- **设备控制**：开关设备、调节灯光亮度、更改颜色、设置温度
- **设备信息查询**：列出设备、检查设备状态、读取设备功能
- **区域管理**：列出各个区域及其所属设备
- **流程管理**：列出并触发自动化流程
- **设备清单**：获取整个系统的设备概览

## 设置

### 1. 安装依赖项

```bash
cd skills/homey-cli
npm install
```

### 2. 创建 Homey 应用程序凭据

1. 访问 https://tools.developer.homey.app/tools/app
2. 创建一个新的应用程序，设置以下参数：
   - **回调 URL**：`http://localhost:8787/callback`
   - 记下您的 **客户端 ID** 和 **客户端密钥**

### 3. 配置环境变量

创建 `.env` 文件：

```bash
export HOMEY_CLIENT_ID="your-client-id"
export HOMEY_CLIENT_SECRET="your-client-secret"
export HOMEY_REDIRECT_URL="http://localhost:8787/callback"
```

### 4. 登录

```bash
bash run.sh auth login
```

在浏览器中按照 OAuth 流程进行登录。登录生成的令牌会存储在 `~/.config/homey-cli/` 目录下。

## 使用方法

### 列出所有 Homey 设备

```bash
bash run.sh homey list
```

### 选择当前激活的 Homey 系统

```bash
bash run.sh homey use <homeyId>
```

### 设备操作

```bash
# List all devices
bash run.sh devices list

# List devices as JSON
bash run.sh devices list --json

# Get specific device
bash run.sh devices get <deviceId>

# Read capability value
bash run.sh devices read <deviceId> onoff

# Control devices
bash run.sh devices on <deviceId>
bash run.sh devices off <deviceId>
bash run.sh devices dim <deviceId> 0.4
bash run.sh devices color <deviceId> #FF8800
bash run.sh devices temperature <deviceId> 21.5
```

### 自动化流程操作

```bash
# List flows
bash run.sh flows list

# Trigger flow
bash run.sh flows trigger <flowId>
```

### 获取完整设备清单

```bash
bash run.sh inventory --json
```

## 安全机制

为确保系统安全，某些操作仅允许在设备具备相应功能的情况下执行：

- **默认允许的操作**：`onoff`（开关设备）、`dim`（调节亮度）、`light_hue`（调整色温）、`light_saturation`（调整饱和度）、`light_temperature`（设置温度）、`target_temperature`（设置目标温度）
- **可通过以下命令覆盖默认设置**：`export HOMEYCLI_ALLOWED_CAPABILITIES=onoff,dim,target_temperature`

**禁止的操作**：
- 删除设备
- 修改自动化流程
- 更改应用程序设置

## 常见问题解答

- **问题**：“打开厨房的灯” → 先列出所有设备，找到对应的设备，然后使用 `devices on <deviceId>` 命令
- **问题**：“将客厅的灯光调暗 50%” → 找到相应的设备，然后使用 `devices dim <deviceId> 0.5` 命令
- **问题**：“卧室的温度是多少？” → 找到对应的设备，然后使用 `devices read <deviceId> measure_temperature` 命令
- **问题**：“列出我所有的灯” → 使用 `devices list --json` 命令，并根据设备类别或功能进行筛选

## 配置数据存储位置

- **登录凭据**：`~/.config/homey-cli/credentials.json`
- **Homey 系统配置**：`~/.config/homey-cli/config.json`

## 故障排除

- **认证错误**：重新运行 `bash run.sh auth login`
- **设备未找到**：使用 `bash run.sh devices list` 命令检查设备名称/ID
- **某些操作被禁止**：将其添加到 `HOMEYCLI_ALLOWED_CAPABILITIES` 文件中，或确认该操作是否为只读功能