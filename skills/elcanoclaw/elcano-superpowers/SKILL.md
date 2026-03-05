# 超级功能——使用子代理进行结构化开发

改编自 [obra/superpowers](https://github.com/obra/superpowers)，适用于 OpenClaw。

## 何时启用

当 Chema 或 Luis 在任何项目中请求一个新的功能、进行大规模重构或修改多个文件时（例如 Elicita、FlightCBT 等），请启用此流程。**不适用于单行代码的修复或外观上的修改**。

## 流程

```
1. BRAINSTORM → 2. PLAN → 3. EXECUTE → 4. REVIEW → 5. SHIP
```

---

## 1. 集思广益（必选）

**严格规定：** 在设计获得批准之前，严禁编写代码。  
即使看起来很简单，但简单的场景往往隐藏着潜在的问题。  

### 步骤：  
1. **了解背景** — 阅读相关文件、最近的提交记录以及当前的项目状态。  
2. **提出问题** — 每次只提出一个问题，最好提供多个选项。  
3. **提出 2-3 个解决方案** — 包括各自的优缺点以及你的推荐方案。  
4. **展示设计方案** — 将设计方案分成易于理解的段落展示，并在继续之前等待批准。  
5. **保存设计方案** — 将设计方案保存为 `docs/plans/YYYY-MM-DD-<feature>-design.md` 文件。  

### 需要涵盖的内容：  
- 受影响的架构/组件  
- 数据流  
- 错误处理机制  
- 测试方法  
- 对现有代码的影响  

---

## 2. 制定计划  

在设计获得批准后，编写实施计划。  

### 计划制定规则：  
- 将计划保存为 `docs/plans/YYYY-MM-DD-<feature>-plan.md` 文件。  
- 每个任务应耗时 **2-5 分钟**。  
- 明确指出需要创建或修改的文件路径。  
- 在计划中包含完整的代码实现（而非仅描述验证步骤）。  
- 使用具体的命令，并说明预期的执行结果。  
- 遵循 DRY（Don’t Repeat Yourself）和 YAGNI（You Ain’t Gonna Need It）原则，频繁提交代码更改。  

### 任务结构：  

```markdown
### Tarea N: [Nombre]

**Archivos:**
- Crear: `ruta/exacta/archivo.ts`
- Modificar: `ruta/exacta/existente.ts`
- Test: `tests/ruta/test.ts`

**Paso 1:** Escribir test que falle
[código completo del test]

**Paso 2:** Verificar que falla
Ejecutar: `npm test -- --grep "nombre"`
Esperado: FAIL

**Paso 3:** Implementación mínima
[código completo]

**Paso 4:** Verificar que pasa
Ejecutar: `npm test -- --grep "nombre"`
Esperado: PASS

**Paso 5:** Commit
`git add ... && git commit -m "feat: descripción"`
```

### 完成计划后，询问：  
> “计划已保存在 `docs/plans/...` 文件中。是直接使用子代理执行，还是希望先进行审查？”  

---

## 3. 执行——按任务分配子代理  

为计划中的每个任务创建一个单独的子代理（使用 `sessions_spawn`）。使用新的子代理可以避免上下文混淆。  

### 子代理的提示语：  

```
Eres un implementador. Tu ÚNICA tarea es ejecutar exactamente lo que dice el plan.

REGLAS:
- Sigue el plan al pie de la letra
- Si algo no está claro, PARA y pregunta (no improvises)
- Test primero, implementación después
- Commit al terminar
- NO hagas nada que no esté en el plan

TAREA:
[texto completo de la tarea del plan]

CONTEXTO DEL PROYECTO:
[archivos relevantes, stack, convenciones]
```

### 每个任务完成后，进行双重审查：  

**第一次审查：**  
- **是否符合计划要求？**  
  - 是否创建或修改了正确的文件？  
  - 测试是否通过？  
  - 是否添加了计划中未包含的内容？ → 如果有，需要回滚更改。  
  - 是否遗漏了计划中的内容？ → 需要补充完成。  

**第二次审查：**  
- **代码质量**：  
  - 代码是否整洁？  
  - 测试是否覆盖了边缘情况？  
  - 代码是否存在问题（如“代码异味”）？  

### 如果审查未通过：  
- 根据具体反馈重新启动子代理进行审查，直到两次审查都通过为止。  

---

## 4. 最终审查  

所有任务完成后：  
- 确保构建过程能够成功执行。  
- 如果有用户界面（UI），请截取屏幕截图。  
- 完整审查所有的代码差异（diff）。  
- 将审查结果记录在每日笔记中。  

---

## 5. 发布代码  

- 使用 `git push` 将代码推送到远程仓库。  
- 如果需要，重启 PM2 服务器。  
- 向 Chema 发送总结信息。  

---

## 原则：  
- **YAGNI**（You Ain’t Gonna Need It）：不要编写未被请求的功能。  
- **DRY**：避免重复代码或逻辑。  
- **TDD**（Test-Driven Development）：始终先编写测试。  
- **保持上下文清晰**：每个任务使用新的子代理。  
- **以事实为依据**：在宣布任务完成之前，务必进行验证。  
- **计划至上**：如果需要偏离原计划，必须暂停并重新制定方案。  

---

## 特别针对 Elicita 的注意事项：  
- **绝对禁止使用任何演示数据或虚构数据**。  
- 每个包含用户界面的任务完成后，必须进行构建、重启 PM2 服务器并截取屏幕截图。  
- 使用的子代理模型为 `anthropic/claude-sonnet-4-6`。  
- 如果构建过程中出现问题，使用 `git checkout` 命令回退到之前的代码状态，并记录问题详情。