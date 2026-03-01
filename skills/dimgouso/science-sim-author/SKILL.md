---
name: science-sim-author
description: 根据提供的 SimSpec YAML 或 JSON 文件，生成一个自包含的交互式科学模拟程序，并将其整合到一个单独的 index.html 文件中。该程序适用于用户需要物理、化学、生物或 STEM 领域的演示内容，支持参数滑块、图表、探究式工作表、数据导出以及类似 PhET 的交互式体验。
homepage: https://clawhub.ai
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":[],"env":[],"config":[]},"os":["darwin","linux","win32"]}}
---
# 科学模拟工具作者

## 核心承诺

生成一个独立的 `index.html` 文件，该文件可以在离线环境下运行，能够在 2D 画布上展示 STEM 模拟结果，将模型参数以滑块的形式呈现给用户，绘制时间序列图，并包含一个探究工作表。

## 输入参数

接受一个格式为 YAML 或 JSON 的 `SimSpec` 对象，其中包含以下内容：
- `id`、`title`、`domain`
- `state`、`params`、`initial`、`equations`、`outputs`
- 可选参数：`level`、`dt`、`worksheet`、`success_criteria`

在生成任何内容之前，需根据 [templates/sim_spec_schema.json](templates/sim_spec_schema.json) 对输入数据进行验证。

## 输出要求

- 生成一个名为 `index.html` 的文件。
- 将所有 CSS 代码放在 `<style>` 标签中，将所有 JavaScript 代码放在 `<script>` 标签中。
- 不使用任何打包工具、包管理器、CDN、外部字体或运行时网络访问。
- 必须包含以下 DOM 元素 ID：`simCanvas`、`plotCanvas`、`runToggle`、`stepBtn`、`resetBtn`、`dtSlider`、`paramControls`、`readouts`、`statusBanner`、`worksheet`、`copyJsonBtn`、`downloadCsvBtn`。
- 必须提供控制面板、数据展示功能、一个时间序列图、本地 JSON 数据导出功能、本地 CSV 文件下载功能以及一个非空的工作表。

## 工作流程

1. 根据 [templates/sim_spec_schema.json](templates/sim_spec_schema.json) 对输入的 `SimSpec` 对象进行验证。
2. 对输入数据进行标准化处理：
   - 如果缺少 `dt`，则使用默认值 `default=0.01`、`min=0.001`、`max=0.05`。
   - 如果某个参数未指定 `step`，则计算 `step=(max-min)/100` 并进行适当的四舍五入处理。
   - 在生成 JavaScript 代码之前，将导数别名（如 `dx`、`dy`、`dvx`、`dvy`、`dq`、`dvc`）转换为标准的 `d<stateName>` 形式。
   - 默认的数据展示内容应为时间 `t` 以及所有状态变量的值（按状态顺序排列）。
3. 选择合适的渲染器：
   - 如果模拟涉及力学（`mechanics`）且包含 `x` 和 `y` 变量，则使用 `trajectory2d` 渲染器；
   - 如果模拟涉及力学且包含 `x` 和 `v` 变量，则使用 `oscillator1d` 渲染器；
   - 如果模拟涉及电磁学（`electromagnetism`）且包含 `q` 或 `vc` 变量，则使用 `circuit_rc` 渲染器；
   - 如果无法确定合适的渲染器，应要求用户提供更明确的 `SimSpec` 内容。
4. 使用预处理后的数据填充 [templates/sim_single_file_html.mustache](templates/sim_single_file_html.mustache) 模板。
5. 在返回最终的 `index.html` 文件之前，运行 [rubrics/validation_checklist.md](rubrics/validation_checklist.md) 进行检查。

## 模板占位符

需要填充以下变量：
- `sim_id`、`sim_title`、`domain`、`level`、`renderer_kind`
- `state_json`、`params_json`、`initial_json`、`equations_json`、`outputs_json`
- `worksheet_json`、`success_criteria_json`、`readout_fields_json`
- `dt_default`、`dt_min`、`dt_max`
- `model_step_logic_js`、`scene_draw_js`、`readout_map_js`

**注意事项**：
- JSON 占位符在插入之前必须进行序列化处理。
- 数据属性中使用的字符串占位符应为普通字符串。
- `model_step_logic_js` 必须返回一个导数对象，且不能使用 `eval` 或 `Function` 函数。
- `scene_draw_js` 和 `readout_map_js` 可以为空；如果不需要数据展示功能，可以使用 `return [];` 来实现空返回。

## 渲染和模型规则

- 使用模板中提供的 RK4 和 Euler 积分器进行计算。
- 物理模拟的步长固定，并使用 `requestAnimationFrame` 进行渲染。
- 如果某个状态值变为 `NaN` 或 `Infinity`，则自动暂停模拟。
- 限制轨迹历史数据和绘图历史数据的数量。
- 优先使用 `outputs` 中指定的一个图表进行显示；如果提供了多个图表，仅将第一个图表显示在界面上，其余图表作为元数据保留。

## 工作表规则

- 如果 `SimSpec` 提供了工作表内容，请保留该内容（除非工作表不完整）。
- 如果工作表中缺少某些类别的信息，可以使用 [rubrics/pedagogy_inquiry_prompts.md](rubrics/pedagogy_inquiry_prompts.md) 中提供的提示来生成缺失的内容。
- 工作表必须包含以下内容：
  - 3 个预测问题
  - 2 个测试问题
  - 2 个解释问题
  - 2 个关于误解的问题

## 安全规则

严格遵守 [rubrics/security_notes.md] 中的安全规范：
- 不允许用户执行 shell 命令。
- 不要求用户提供敏感信息或 API 密钥。
- 不允许获取远程资源或脚本。
- 不允许添加隐藏的遥测数据或分析功能。
- 不允许生成多个文件。

## 相关模板和参考资料

- 模板：[templates/sim_single_file_html.mustache](templates/sim_single_file_html.mustache)
- 规范：[templates/sim_spec_schema.json](templates/sim_spec_schema.json)
- 验证清单：[rubrics/validation_checklist.md](rubrics/validation_checklist.md)
- 教学提示：[rubrics/pedagogy_inquiry_prompts.md]
- 安全说明：[rubrics/security_notes.md]

**示例**：
- [examples/projectile_drag.yml](examples/projectile_drag.yml)
- [examples/spring_mass.yml](examples/spring_mass.yml)
- [examples/rc_circuit.yml](examples/rc_circuit.yml)