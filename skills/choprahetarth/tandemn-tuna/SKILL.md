---
name: tandemn-tuna
description: 在 GPU 上部署并运行大型语言模型（LLM）模型。比较不同 GPU 的价格。可以在 Modal、RunPod、Cerebrium、Cloud Run、Baseten 或 Azure 上启动 vLLM 服务，并支持使用临时实例（spot instance）作为备用方案。提供与 OpenAI 兼容的推理端点（inference endpoint）。
version: 0.0.1
metadata:
  openclaw:
    requires:
      bins:
        - uv
      anyBins:
        - aws
        - az
      env: []
    emoji: "\U0001F41F"
    homepage: https://github.com/Tandemn-Labs/tandemn-tuna
    install:
      - kind: uv
        package: tandemn-tuna
        bins: [tuna]
---
# Tuna — 在GPU基础设施上部署和运行大语言模型（LLM）  

Tuna是一个混合型的GPU推理编排工具，它允许你在无服务器（serverless）环境中的GPU上部署、运行和管理大语言模型（如Llama、Qwen、Mistral、DeepSeek、Gemma以及HuggingFace提供的任何模型）。这些GPU可以来自Modal、RunPod、Cerebrium、Google Cloud Run、Baseten或Azure Container Apps等平台。此外，通过SkyPilot，你还可以选择在AWS上使用按需（spot）实例作为备用方案。每个部署都会生成一个兼容OpenAI的 `/v1/chat/completions` 端点。  

**核心原理：** 无服务器GPU能够即时处理请求（快速启动，按秒计费），同时系统会在后台启动成本更低的按需GPU。一旦按需GPU准备好，流量就会自动切换到该GPU；如果按需GPU被中断，流量会自动回退到无服务器环境。这种方式相比纯无服务器方案可节省3-5倍的成本，并且完全没有停机时间。  

## 快速入门 — 通过3个命令部署模型  

```bash
# 1. Install tuna
uv pip install tandemn-tuna

# 2. Deploy a model (auto-picks cheapest serverless provider for the GPU)
tuna deploy --model Qwen/Qwen3-0.6B --gpu L4 --service-name my-llm

# 3. Query your endpoint (shown in deploy output)
curl http://<router-ip>:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen/Qwen3-0.6B", "messages": [{"role": "user", "content": "Hello!"}]}'
```  

**仅使用无服务器环境（无需按需实例，也不需要AWS）：**  
```bash
tuna deploy --model Qwen/Qwen3-0.6B --gpu L4 --serverless-only
```  

## 所有命令  

### `tuna deploy` — 在GPU上部署模型  
此命令用于在无服务器环境和按需GPU环境中部署模型。  

**必选参数：**  
- `--model` — HuggingFace模型的ID（例如：`Qwen/Qwen3-0.6B`、`meta-llama/Llama-3-70b`）  
- `--gpu` — GPU类型（例如：`T4`、`L4`、`L40S`、`A100`、`H100`、`B200`）  

**常用选项：**  
- `--service-name` — 部署的名称（如果省略则自动生成）  
- `--serverless-provider` — 强制指定服务提供商：`modal`、`runpod`、`cloudrun`、`baseten`、`azure`（默认为最便宜的提供商）  
- `--serverless-only` — 仅使用无服务器环境，不使用按需GPU（无需AWS）  
- `--gpu-count` — GPU的数量（默认：1）  
- `--tp-size` — 张量并行度（默认：1）  
- `--max-model-len` — 模型的最大序列长度（默认：4096）  
- `--spots-cloud` — 按需GPU的云服务：`aws` 或 `azure`（默认：`aws`）  
- `--region` — 按需实例的云区域  
- `--concurrency` — 修改无服务器环境的并发限制  
- `--no-scale-to-zero` — 确保至少有一个按需GPU实例在运行  
- `--public` — 使端点公开可访问（无需身份验证）  
- `--scaling-policy` — 包含扩展参数的YAML文件路径  

**特定提供商的选项：**  
- `--gcp-project`、`--gcp-region` — 用于Google Cloud Run  
- `--azure-subscription`、`--azure-resource-group`、`--azure-region`、`--azure-environment` — 用于Azure  

**示例：**  
```bash
# Deploy Llama 3 on Modal with hybrid spot
tuna deploy --model meta-llama/Llama-3-8b --gpu A100 --serverless-provider modal

# Deploy on RunPod, serverless-only
tuna deploy --model mistralai/Mistral-7B-Instruct-v0.3 --gpu L40S --serverless-provider runpod --serverless-only

# Deploy on Azure with an existing environment
tuna deploy --model Qwen/Qwen3-0.6B --gpu T4 --serverless-provider azure --azure-environment my-env

# Deploy a large model with tensor parallelism
tuna deploy --model meta-llama/Llama-3-70b --gpu H100 --gpu-count 4 --tp-size 4
```  

### `tuna show-gpus` — 查看各提供商的GPU价格**  
此命令可显示所有无服务器提供商的GPU价格，包括按需GPU的价格。  

**示例：**  
```bash
tuna show-gpus [--gpu <GPU>] [--provider <provider>] [--spot]
```  

### `tuna check` — 预检部署环境**  
在部署前运行此命令，验证凭证、命令行工具（CLI）和提供商的配额是否正确。  

**示例：**  
```bash
tuna check --provider <provider> [--gpu <GPU>]
```  

### `tuna status` — 查看部署状态**  
```bash
tuna status --service-name <name>
```  

### `tuna cost` — 查看成本节省情况**  
```bash
tuna cost --service-name <name>
```  

### `tuna list` — 列出所有已部署的模型**  
```bash
tuna list [--status active|destroyed|failed]
```  

### `tuna destroy` — 卸载部署**  
```bash
# Destroy a specific deployment
tuna destroy --service-name <name>

# Destroy all deployments
tuna destroy --all
```  

## 提供商设置指南  
每个无服务器提供商都需要单独的凭证。运行 `tuna check --provider <provider>` 来验证配置是否正确。  

### Modal  
```bash
pip install modal  # or: uv pip install tandemn-tuna[modal]
modal token new    # opens browser to authenticate
```  
无需设置环境变量——凭证存储在Modal的配置文件中。  

### RunPod  
```bash
export RUNPOD_API_KEY="your-api-key"
```  
从[RunPod控制台](https://www.runpod.io/console/user/settings)获取你的API密钥。  

### Google Cloud Run  
```bash
pip install google-cloud-run  # or: uv pip install tandemn-tuna[cloudrun]
gcloud auth login
gcloud auth application-default login
```  
可选地设置 `GOOGLE_CLOUD_PROJECT` 和 `GOOGLE_CLOUD_REGION`，或直接使用 `--gcp-project` 和 `--gcp-region`。  

### Baseten  
```bash
pip install truss  # or: uv pip install tandemn-tuna[baseten]
export BASETEN_API_KEY="your-api-key"
truss login --api-key $BASETEN_API_KEY
```  

### Azure Container Apps  
```bash
pip install azure-mgmt-appcontainers azure-identity  # or: uv pip install tandemn-tuna[azure]
az login
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights
```  
在部署时传递 `--azure-subscription`、`--azure-resource-group` 和 `--azure-region`；或者设置环境变量 `AZURE_SUBSCRIPTION_ID`、`AZURE_RESOURCE_GROUP`、`AZURE_REGION`。首次部署会创建一个GPU环境（约30分钟），后续部署将重用该环境（约2分钟）。可以使用 `--azure-environment` 来指定现有的环境。  

### Cerebrium  
**注意：** Hobby计划仅支持T4、A10、L4、L40S类型的GPU；A100和H100需要Enterprise计划。  

### 使用SkyPilot在AWS上使用按需GPU  
混合部署会自动包含按需GPU。只需配置AWS即可。  
```bash
aws configure  # set access key, secret key, region
```  
如果尚未配置AWS，可以使用 `--serverless-only` 选项跳过按需GPU的配置。  

## 常见场景  

**用户希望快速测试模型时：**  
使用 `--serverless-only` 选项跳过按需GPU的配置，选择较小的GPU（如L4或T4）。示例：  
```bash
tuna deploy --model Qwen/Qwen3-0.6B --gpu L4 --serverless-only
```  

**用户希望以最低成本部署模型时：**  
首先运行 `tuna show-gpus --spot` 查看无服务器环境和按需GPU的价格，然后使用混合模式（默认设置）进行部署以节省成本。系统会自动选择最适合所选GPU的最便宜的无服务器提供商。  

**用户想比较GPU价格时：**  
```bash
tuna show-gpus
tuna show-gpus --gpu A100
tuna show-gpus --spot  # includes AWS spot prices
```  

**用户询问“哪些提供商支持H100 GPU？”或特定GPU时：**  
```bash
tuna show-gpus --gpu H100
```  

**用户希望在特定提供商上部署模型时：**  
使用 `--serverless-provider <provider>`。部署前先运行 `tuna check --provider <provider>` 验证凭证。  

**用户希望部署大型模型（超过70B参数）时：**  
需要使用多个GPU并设置适当的张量并行度。  
```bash
tuna deploy --model meta-llama/Llama-3-70b --gpu H100 --gpu-count 4 --tp-size 4
```  

**用户想检查配置是否正确时：**  
```bash
tuna check --provider modal
tuna check --provider runpod
```  

**用户想查看当前已部署的模型时：**  
```bash
tuna list
tuna list --status active
```  

**用户想卸载所有部署时：**  
```bash
tuna destroy --all
```  

## 支持的GPU类型  
Tuna支持的GPU类型及其对应的平台如下：  

| GPU | VRAM | 架构 | 可用平台 |  
|-----|------|-------------|-------------|  
| T4 | 16 GB | Turing | Modal、RunPod、Baseten、Azure、Cerebrium、Spot |  
| A10 | 24 GB | Ampere | Cerebrium |  
| A10G | 24 GB | Ampere | Modal、Baseten、Spot |  
| A4000 | 16 GB | Ampere | RunPod |  
| A5000 | 24 GB | Ampere | RunPod |  
| RTX 4090 | 24 GB | Ada | RunPod |  
| L4 | 24 GB | Ada | Modal、RunPod、Cloud Run、Baseten、Cerebrium、Spot |  
| A40 | 48 GB | Ampere | RunPod |  
| A6000 | 48 GB | Ampere | RunPod |  
| L40 | 48 GB | Ada | RunPod |  
| L40S | 48 GB | Ada | Modal、RunPod、Cerebrium、Spot |  
| A100 (40 GB) | 40 GB | Ampere | Modal、Cerebrium、Spot |  
| A100 (80 GB) | 80 GB | Ampere | Modal、RunPod、Azure、Baseten、Cerebrium、Spot |  
| H100 | 80 GB | Hopper | Modal、RunPod、Baseten、Cerebrium、Spot |  
| H200 | 141 GB | Hopper | Spot |  
| B200 | 192 GB | Blackwell | Modal、Baseten |  
| RTX PRO 6000 | 32 GB | Blackwell | Cloud Run |  

可以使用 `tuna show-gpus` 查看所有提供商当前的GPU价格。  

## 错误处理  

- **预检失败 (`tuna check`)：**  
输出会明确指出问题所在：缺少命令行工具、凭证过期、提供商未注册或配额不足。修复问题后重新运行 `tuna check`。  
- **部署失败：**  
  1. 运行 `tuna check --provider <provider> --gpu <gpu>` 验证环境配置。  
  2. 使用 `-v` 选项查看详细日志：`tuna deploy -v ...`  
  3. 使用 `tuna status --service-name <name>` 查看部署状态。  
- **按需GPU无法使用：**  
  按需GPU的可用性受云服务影响。如果按需GPU无法启动，无服务器环境仍会继续提供服务（无停机时间）。可以尝试更换云区域（使用 `--region`），或使用 `--serverless-only` 选项。  
- **“没有提供商支持某种GPU”：**  
  使用 `tuna show-gpus --gpu <GPU>` 查看哪些提供商提供该GPU。并非所有GPU在所有平台上都可用。  
- **Azure环境配置耗时过长：**  
  首次部署时会创建一个GPU环境（约30分钟），后续部署会重用该环境（约2分钟）。可以使用 `--azure-environment` 指定现有的环境。