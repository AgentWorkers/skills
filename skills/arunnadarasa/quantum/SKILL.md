---
name: quantinuumclaw
description: 该功能支持使用 Quantinuum、Guppy、Selene 和 Fly.io 工具来构建和部署量子计算应用程序。适用于 OpenClaw 临床黑客马拉松、临床或医疗保健项目（如药物发现、治疗优化、患者分层、试验随机化）、基于量子技术的 Web 应用程序、将量子算法部署到云端，或将量子计算结果集成到用户界面中。
---
# QuantinuumClaw – Quantum Guppy/Selene 技术栈

该技术栈提供了使用 **Quantinuum**（量子硬件/模拟器）、**Guppy**（量子编程语言）、**Selene**（FastAPI 后端）和 **Fly.io**（部署平台）构建可生产级量子应用程序所需的一切功能，同时支持可选的 **Lovable** 前端框架。该技术栈专为 **OpenClaw 临床黑客马拉松** 和通用量子 Web 应用程序进行了优化。

## 适用场景

- 适用于 OpenClaw 临床黑客马拉松或任何与临床/医疗保健相关的量子项目
- 用于构建利用量子计算的应用程序（如优化、化学计算、机器学习、随机数生成、加密等）
- 部署量子算法作为 REST API，或创建用于展示量子计算结果的仪表板
- 相关术语包括：临床、医疗保健、药物发现、治疗优化、患者分层、分子模拟、临床试验、Guppy、Selene、Fly.io

## 示例请求：
- “构建一个带有 Web 界面的量子投资组合优化器”
- “将我的 Guppy 算法部署到云端”
- “创建一个临床分子模拟演示”
- “在 Fly.io 上设置一个量子机器学习服务”

## 技术栈概览

| 组件           | 功能                |
|-----------------|-------------------|
| **Quantinuum**     | 量子硬件（H 系列）或模拟器        |
| **Guppy**        | 量子编程语言（用于设计量子电路）     |
| **Selene**       | 运行 Guppy 并提供 REST API 的 FastAPI 后端 |
| **Fly.io**       | 在云端托管 Selene 后端        |
| **Lovable**      | React/TypeScript 前端框架；支持调用 Selene API |

## 快速入门（一个命令）

在项目根目录下执行以下命令：

```bash
python3 scripts/create_quantum_app.py \
  --app-name "clinical-demo" \
  --use-case "chemistry" \
  --description "Clinical molecular simulation" \
  --deploy
```

然后在前端代码中设置 `VITE_API_URL` 为你的 Fly.io 应用程序的 URL（例如：`https://clinical-demo.fly.dev`）。

## 临床用例与对应命令的映射：

| 临床场景                          | 对应命令                         | 备注                                      |
|----------------------------------|----------------------------------|-----------------------------------------|
| 药物发现/分子模拟                      | `chemistry`                        | 使用 Guppy 进行分子结构与能量属性的计算             |
| 治疗/资源优化                        | `optimization`                      | 应用量子优化算法（QAOA）                          |
| 患者分层/机器学习                      | `ml`                            | 利用量子机器学习模型进行患者分类                   |
| 试验随机化                        | `random`                          | 使用量子随机数生成器                          |
| 安全密钥/协议                        | `crypto`                          | 生成量子安全的加密密钥                        |

其他通用场景（如投资组合管理、金融等）也可以使用 `optimization`、`chemistry`、`ml`、`random`、`crypto` 或 `finance`。详细信息请参阅 `references/clinical-use-cases.md`。

## 完整开发流程：

### 第一步：定义应用场景
明确你要解决的问题（优化、模拟、机器学习、加密等）。

### 第二步：创建 Selene 后端
```bash
python3 scripts/setup_selene_service.py \
  --app-name "my-quantum-app" \
  --use-case "chemistry" \
  --description "Quantum chemistry simulator"
```
此步骤会创建一个包含 FastAPI、健康检查功能、Dockerfile 和 `fly.toml` 文件的后端目录。

### 第三步：实现 Guppy 量子电路
编辑 `my-quantum-app/main.py` 文件中的 `QuantumService._run_real_quantum()` 函数。参考 `references/guppy_guide.md` 了解语法规范。针对临床应用，需注意分子结构、测量次数和精度设置；对于优化场景，需设定目标函数和约束条件；对于机器学习场景，需定义特征参数和训练周期。

### 第四步：部署到 Fly.io
```bash
python3 scripts/flyio_deploy.py --app-name "my-quantum-app" --service-dir "my-quantum-app" --region "lhr"
```
使用 `fly secrets set` 命令配置应用程序的 secrets；如需演示，可以使用模拟器代替真实量子硬件。

### 第五步：开发前端
使用 `assets/lovable-template/` 模板，或根据需要自行开发前端代码。完成后执行 `npm install` 和 `npm run dev`。

### 第六步：连接并测试
将前端代码中的 `VITE_API_URL` 设置为 Fly.io 后端的地址，并访问 `/health` 确认服务是否正常运行。

## 临床用例快速参考：

- **药物发现/分子模拟**：使用 Guppy 的 VQE（Variational Quantum Encryption）算法计算分子能量和属性；通过 API 提供分子类型和参数信息。
- **治疗/资源优化**：设定优化目标（如成本、等待时间），在 Selene 中运行量子优化算法，并在用户界面展示结果。
- **患者分层/分类**：将患者特征数据输入模型，输出风险等级或分类结果。
- **随机化**：使用 Guppy 的量子随机数生成器生成随机样本；通过 API 提供随机数结果。
- **安全/密钥管理**：使用量子安全的加密算法生成密钥，并将密钥存储在后端。

## 数据与合规性注意事项（临床/黑客马拉松环境）：

- **演示用途**：仅使用合成数据或去标识化数据；切勿将真实患者信息发送到量子后端或存储在 Fly.io 中。
- **API 密钥**：将密钥存储在 Fly.io 的 secrets 配置中，切勿将其写入代码或前端代码。
- **生产环境**：添加身份验证机制、实施速率限制，并遵守 HIPAA/DPA 等法规；在 Selene 中配置 CORS（跨源资源共享）策略。

## 相关资源：

- **脚本**：
  - `create_quantum_app.py`：整合后端、部署和前端功能的脚本
  - `setup_selene_service.py`：用于搭建 Selene 后端的模板
  - `flyio_deploy.py`：用于将应用程序部署到 Fly.io
  - `lovable_integrate.py`：用于将前端与后端连接

- **参考文档**：
  - `guppy_guide.md`：Guppy 的编程语法、量子门操作和示例
  - `selene_api.md`：API 接口、请求与响应格式、错误处理方式
  - `flyio_config.md`：Fly.io 的扩展配置、区域设置和 secrets 管理
  - `lovable_patterns.md`：前端界面设计模板和 API 客户端代码示例
  - `clinical-use-cases.md`：详细的临床应用场景及合规性指南

- **资源文件**：
  - `selene-template/`：包含后端基础文件（main.py、Dockerfile、fly.toml、.env.example）
  - `lovable-template/`：基于 React/TypeScript 的前端框架，包含量子仪表板和 API 客户端代码

## 高级应用示例：

- **多量子算法集成**：
  - 结合 Selene 和 QAOA/VQE 算法；使用 Lovable 前端界面和滑块进行参数调整；Fly.io 提供扩展性支持。
  - **化学模拟工具**：利用 Guppy 进行分子模拟，并提供 3D 可视化功能；支持数据持久化存储。
- **量子机器学习 API**：Selene 提供量子神经网络（QNN）或支持向量机（QSVM）接口；Lovable 前端用于模型训练和预测；根据需要使用 Fly.io 的 GPU 资源。

## 性能、成本与安全考虑：

- **任务调度**：使用任务队列处理耗时较长的量子计算任务；前端可以使用 WebSockets 或轮询机制与后端通信。
- **缓存机制**：缓存重复的计算结果以降低硬件成本。
- **资源管理**：在空闲时关闭不必要的计算资源（`min_machines_running = 0`）；参考 `references/flyio_config.md` 了解虚拟机配置建议。
- **安全性**：前端代码中不存储 API 密钥；在 Selene 中实施速率限制；生产环境中使用 HTTPS 协议；详细安全配置请参阅 `references/selene_api.md`。

## 常见问题与解决方法：

- **Guppy 导入错误**：在后端环境中执行 `pip install guppy`；演示时可以使用模拟模式。
- **Selene 无法启动**：检查 `fly.toml` 配置文件、日志文件和环境变量。
- **前端无法连接**：确认 `VITE_API_URL` 设置正确；检查 Selene 的 CORS 配置；尝试使用 `curl .../health` 命令测试连接。
- **部署失败**：执行 `fly deploy --clean` 清理部署环境；查看 `fly logs --phase build` 日志；确保已正确配置身份验证。

## 下一步操作：
完成初始设置后，建议监控量子计算资源的使用情况和成本；如果应用程序面向公众，需为 Selene 添加身份验证机制；优化错误处理和日志记录功能；考虑为任务历史数据添加持久化存储方案。

---

如需了解详细的临床应用场景要求和合规性指南，请参阅 `references/clinical-use-cases.md`。