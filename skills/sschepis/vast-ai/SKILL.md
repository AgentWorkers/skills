# 技能：VAST.ai GPU租赁服务

## 概述
该技能允许您按需配置GPU基础设施。在执行写入操作之前，您必须拥有用户提供的API密钥。

## 功能
1. **搜索**：根据GPU型号（例如：“RTX 4090”）查找相应的机器，并显示其最高每小时租金。
2. **租赁**：在指定的资源ID上创建一个容器（默认使用PyTorch环境）。
3. **连接**：获取当前正在运行的容器的SSH连接字符串。
4. **余额查询**：查看所有正在运行的机器的可用信用额度以及当前的每小时使用情况。

## 使用流程
- **步骤1**：如果尚未获取用户提供的API密钥，请先向用户索取。
- **预租检查**：在租赁之前，调用`balance`函数以确保用户有足够的资金。
- **步骤2**：搜索可用的资源，并向用户展示前三种价格最低的选项。
- **步骤3**：用户确认后，调用`rent`函数进行租赁。
- **提醒机制**：如果用户的信用额度低于5.00美元，在每次成功租赁后向用户发出警告。
- **步骤4**：等待30-60秒后，调用`connect`函数以获取SSH连接字符串。

## 工具定义
- `search(gpu: string, price: number)`：根据GPU型号和价格搜索资源。
- `rent(id: number, image: string)`：根据资源ID和指定的容器镜像进行租赁。
- `connect(id: number)`：连接指定的资源以获取SSH连接信息。
- `balance()`：查询当前的所有可用资源及其使用情况。

## 执行方式
通过运行以下命令来使用这些工具：
```
node /Users/sschepis/Development/vast-ai/dist/cli.js <action> [params]
```
注意：必须设置环境变量`VAST_API_KEY`。

### 示例
- 搜索：`node dist/cli.js search --gpu "RTX 4090" --price 0.5`
- 租赁：`node dist/cli.js rent --id 12345 --image "pytorch/pytorch"`
- 连接：`node dist/cli.js connect --id 12345`
- 查询余额：`node dist/cli.js balance`