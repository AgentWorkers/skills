# 自动测试生成器

该工具能够为 OpenClaw 的各项技能自动生成基本的单元测试/集成测试，有助于提升代码质量并防止代码在开发过程中出现退化（即功能错误）。

## 使用方法

```bash
node skills/auto-test-generator/index.js <skill-name>
```

## 工作原理

1. 扫描目标技能目录。
2. 分析 `index.js` 文件中导出的模块。
3. 生成一个 `test.js` 文件，其中包含基本的测试用例（例如检查模块是否能够正确加载、以及检查 `--help` 命令是否能够正常使用）。
4. 立即运行生成的测试。

## 示例

```bash
node skills/auto-test-generator/index.js skill-health-monitor
```

**输出结果：**
- 会在 `skills/skill-health-monitor` 目录下生成 `test.js` 文件。
- 运行该测试文件。
- 显示测试结果（成功或失败）。