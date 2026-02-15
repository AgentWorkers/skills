---
name: sonic-build
description: 使用 `sonic-buildimage` 工具来构建 SONiC（用于云中开放网络的软件）交换机镜像。该工具适用于构建 VS/ASIC 镜像、配置构建并行性/内存/缓存设置、调试构建失败问题、管理子模块、清理构建产生的临时文件以及优化构建性能。支持所有平台（VS、Broadcom、Mellanox、Marvell、Nvidia-Bluefield）。
---

# SONiC 镜像构建

## 快速入门

```bash
cd sonic-buildimage
make init
make configure PLATFORM=vs   # or broadcom, mellanox, etc.
make SONIC_BUILD_JOBS=4 target/sonic-vs.img.gz
```

**开发构建（跳过测试）：** 添加 `BUILD_SKIP_TEST=y`。

## 构建架构

通过 GNU Make 进行两阶段构建：`slave.mk` → `sonic-slave` Docker 容器：

1. **Bookworm 阶段** — 将所有软件包（`.deb` 文件、Python wheel 文件以及 Docker 镜像）编译到 `target/debs/bookworm/` 目录中。
2. **Trixie 阶段** — 从第 1 阶段的软件包中组装最终的 Docker 镜像，并将其保存到 `target/debs/trixie/` 目录中。

`Makefile` 会为每个构建阶段调用不同的 `BLDENV` 值来运行 `Makefile.work` 脚本。`configure` 目标会为每个发行版创建相应的目录。

## 配置

所有配置选项都位于 `rules/config` 文件中。可以在 `rules/config.user` 文件中进行自定义（该文件会被 Git 忽略，且配置更改会在重新基线操作后保持不变）。

### 关键配置选项

| 配置项 | 默认值 | 推荐值 | 功能 |
|------|---------|-------------|--------|
| `SONIC_CONFIG_BUILD_JOBS` | 1 | 4 | 并行构建顶层软件包 |
| `SONIC_CONFIGMAKE_JOBS` | `$(nproc)` | 默认值 | 每个软件包使用的编译线程数 |
| `BUILD_SKIP_TEST` | `n` | `y`（开发模式） | 跳过单元测试 |
| `SONIC_BUILD_MEMORY` | 未设置 | 24GB | Docker 的 `--memory` 参数；用于指定容器的内存限制 |
| `SONIC_DPKG_CACHE_METHOD` | 未设置 | `rwcache` | 用于增量构建的 `.deb` 包缓存机制 |
| `DEFAULT_BUILD_LOG_TIMESTAMP` | 未设置 | `simple` | 在构建日志中添加时间戳 |
| `SONIC_CONFIG_USE_NATIVE_DOCKERD_FOR_BUILD` | 未设置 | `y` | 使用宿主机上的 Docker 守护进程，而非 DinD |

### 推荐的 `rules/config.user` 配置

```makefile
SONIC_CONFIG_BUILD_JOBS = 4
BUILD_SKIP_TEST = y
SONIC_BUILD_MEMORY = 24g
DEFAULT_BUILD_LOG_TIMESTAMP = simple
```

## 并行性

**经验法则：** `JOBS × 6GB ≤ 可用内存大小`。

- `JOBS=1`：构建时间约 3 小时，需要约 10GB 内存。
- `JOBS=4`：显著提升构建速度，需要约 20GB 内存。
- `JOBS=8`：在内存小于 48GB 的情况下可能导致内存不足（OOM）。

**为什么 `JOBS=1` 时构建速度较慢？** 因为有 64/194 个软件包依赖于 `libswsscommon`（这是一个关键路径的瓶颈）。当 `JOBS=1` 时，大部分 CPU 核心处于空闲状态。

## 内存保护

如果不对并行构建进行限制，可能会导致任何宿主机进程触发内核的 OOM（Out of Memory）保护机制。

```bash
# Container-scoped OOM (host stays healthy):
SONIC_BUILD_MEMORY = 24g
# Or via CLI:
make SONIC_BUILDER_EXTRA_CMDLINE="--memory=24g" ...
```

## 缓存

### DPKG 缓存（软件包级别）
```makefile
SONIC_DPKG_CACHE_METHOD = rwcache
SONIC_DPKG_CACHE_SOURCE = /var/cache/sonic/artifacts
```

### 版本缓存（下载内容）
```makefile
SONIC_VERSION_CACHE_METHOD = cache
```

## 重新构建单个软件包

```bash
make target/debs/bookworm/sonic-utilities_1.2-1_all.deb
make target/docker-syncd-vs.gz
ls target/debs/bookworm/ | grep <name>
```

## 清理构建结果

**何时需要清理构建结果？** 在切换分支、执行重新基线操作或遇到无法解释的构建失败时。

```bash
rm -rf target/*   # always full clean, not selective
make configure PLATFORM=vs
make SONIC_BUILD_JOBS=4 target/sonic-vs.img.gz
```

**注意：** 过期的构建产物（如 `.bin` 文件或 squashfs 格式的文件）可能会导致 `make` 命令错误地跳过某些构建步骤。

## 子模块

**使用 SSH 进行克隆比使用 HTTPS 更可靠**（因为 HTTPS 可能会返回 HTTP 500 错误）。

## 常见问题与解决方法**

有关详细的故障排除信息，请参阅 `references/troubleshooting.md`。

## 先决条件**

有关宿主机环境（Docker、Python、jinjanator）的配置要求，请参阅 `references/prerequisites.md`。

## VS 平台相关说明

有关 Visual Studio 平台的特定配置信息（如 TAP 设备、端口映射、sai.profile 文件以及操作速度等），请参阅 `references/vs-platform.md`。

## 提交 Pull Request (PR)

- 每个 PR 应只包含一个提交（推送前需要使用 `squash` 命令压缩代码）
- 使用 `git commit -s` 命令进行 DCO（Developer Code Review）签名
- 在强制推送之前先重新基线到最新的 master 分支
- 添加测试代码——至少运行一次 `BUILD_SKIP_TEST=n` 命令
- 推送后监控持续集成（CI）流程的结果