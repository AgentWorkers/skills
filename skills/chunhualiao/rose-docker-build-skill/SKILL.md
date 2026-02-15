---
name: rose-docker-build
description: 使用 autotools 或 CMake 在 Docker 容器中构建 ROSE 编译器。此方法适用于设置 ROSE 开发环境、从源代码编译 ROSE 以及解决 ROSE 构建过程中的问题。ROSE 需要 GCC 7-10 版本，但大多数现代系统并不支持这些版本，因此推荐使用 Docker 来解决这一兼容性问题。
---

# ROSE Docker 构建

在隔离的 Docker 容器中构建 ROSE 源到源编译器。

## 为什么使用 Docker？

ROSE 需要 GCC 7-10 版本。现代系统通常使用 GCC 11 或更高版本，这会导致构建失败。Docker 可以提供：
- 正确的 GCC 版本（推荐使用 9.x 版本）
- 所有依赖项都已预先安装
- 可复现的构建过程
- 允许在主机上进行编辑，并在容器中完成构建

## 快速入门（使用 Autotools）

```bash
# 1. Clone ROSE
git clone git@github.com:rose-compiler/rose.git
cd rose && git checkout weekly

# 2. Create Docker environment
mkdir ../rose-docker && cd ../rose-docker

# 3. Build and run container (see Dockerfile below)
docker build -t rose-dev .
docker run -d --name rose-dev -v $(pwd)/../rose:/rose/src rose-dev

# 4. Build ROSE inside container
docker exec rose-dev bash -c 'cd /rose/src && ./build'
docker exec rose-dev bash -c 'mkdir -p /rose/build && cd /rose/build && \
  /rose/src/configure --prefix=/rose/install \
    --enable-languages=c,c++ \
    --with-boost=/usr \
    --with-boost-libdir=/usr/lib/x86_64-linux-gnu \
    --disable-binary-analysis \
    --disable-java'
docker exec rose-dev bash -c 'cd /rose/build && make core -j$(nproc)'
docker exec rose-dev bash -c 'cd /rose/build && make install-core'
```

## 快速入门（使用 CMake）

使用 CMake 进行构建需要 CMake 4.x 版本（CMake 3.16 版本会导致 ROSETTA 生成失败）。

```bash
# 1. Clone ROSE
git clone git@github.com:rose-compiler/rose.git
cd rose && git checkout weekly

# 2. Create Docker environment and build container
mkdir ../rose-docker && cd ../rose-docker
docker build -t rose-dev -f Dockerfile.cmake .
docker run -d --name rose-cmake -v $(pwd)/../rose:/rose/src:ro rose-dev

# 3. Configure with CMake
docker exec -w /rose/build rose-cmake cmake /rose/src \
  -DCMAKE_INSTALL_PREFIX=/rose/install \
  -DENABLE_C=ON \
  -DENABLE_TESTS=OFF \
  -DCMAKE_BUILD_TYPE=Release

# 4. Build (use -j4 to avoid OOM on 16GB systems)
docker exec -w /rose/build rose-cmake make -j4

# 5. Test
docker exec rose-cmake /rose/build/bin/rose-compiler --version
```

### CMake 配置选项

| 选项          | 描述                                      |
|-----------------|-----------------------------------------|
| `ENABLE_C=ON`      | 启用 C/C++ 分析（使用 EDG 前端）                   |
| `ENABLE_binary_ANALYSIS=ON` | 启用二进制代码分析（不需要 EDG）                   |
| `ENABLE_TESTS=OFF`     | 跳过测试编译（加快构建速度）                   |
| `CMAKE_BUILD_TYPE=Release` | 优化构建版本                         |

### CMake 与 Autotools 的比较

| 特性                | Autotools                | CMake                          |
|------------------|------------------|-----------------------------------------|
| 稳定性            | ✅ 已成熟                   | ⚠️ 更新版本                         |
| C/C++ 分析          | ✅ 支持                     | ✅ 支持（需进行相应配置）                     |
| 构建目标            | `make core`                | `make`（完整构建）                        |
| 增量构建            | 较慢                     | 较快                             |
| 集成到 IDE           | 有限                     | 非常出色                         |

## Dockerfile 文件

### 使用 Autotools 的 Dockerfile

```dockerfile
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles

RUN apt-get update && apt-get install -y \
    build-essential g++ gcc gfortran \
    automake autoconf libtool flex bison \
    libboost-all-dev libxml2-dev \
    git wget curl vim \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash developer
RUN mkdir -p /rose/src /rose/build /rose/install && chown -R developer:developer /rose
USER developer
WORKDIR /rose
CMD ["tail", "-f", "/dev/null"]
```

### 使用 CMake 的 Dockerfile

```dockerfile
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential g++ gcc gfortran \
    flex bison \
    libboost-all-dev libxml2-dev libreadline-dev \
    zlib1g-dev libsqlite3-dev libpq-dev libyaml-dev \
    libgmp-dev libmpc-dev libmpfr-dev \
    git wget curl vim \
    gnupg software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Install CMake 4.x from Kitware (Ubuntu 20.04 has 3.16 which is too old)
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | apt-key add - \
    && echo 'deb https://apt.kitware.com/ubuntu/ focal main' > /etc/apt/sources.list.d/kitware.list \
    && apt-get update && apt-get install -y cmake \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash developer
RUN mkdir -p /rose/src /rose/build /rose/install && chown -R developer:developer /rose
USER developer
WORKDIR /rose
CMD ["tail", "-f", "/dev/null"]
```

## EDG 二进制文件的处理

进行 C/C++ 分析时需要 EDG（C++ 前端）二进制文件。构建过程会检查：

### 使用 Autotools 的情况：
1. 从现有的 tarball 文件中提取构建目录
2. 源代码位于 `src/frontend/CxxFrontend/roseBinaryEDG-*.tar.gz` 目录下
3. 从 `edg-binaries.rosecompiler.org` 网站下载所需的二进制文件

### 使用 CMake 的情况：
1. 源代码同样位于 `src/frontend/CxxFrontend/roseBinaryEDG-*.tar.gz` 目录下（CMake 会自动检测）
2. 根据构建时的 GCC 版本下载相应的二进制文件
3. 自动将 `libroseEDG.a` 链接到 `librose.so` 文件中

如果服务器无法访问，确保源代码目录中包含 EDG 二进制文件（这些文件通常位于 `weekly` 分支中）。

## 常用命令

### 使用 Autotools 的命令

```bash
# Rebuild after source changes
docker exec rose-dev bash -c 'cd /rose/build && make core -j8'

# Install
docker exec rose-dev bash -c 'cd /rose/build && make install-core'
```

### 使用 CMake 的命令

```bash
# Rebuild after source changes  
docker exec -w /rose/build rose-cmake make -j4

# Install
docker exec -w /rose/build rose-cmake make install
```

### 两种构建方式的通用命令

```bash
# Test ROSE compiler
docker exec rose-dev /rose/install/bin/rose-compiler --version
docker exec rose-cmake /rose/build/bin/rose-compiler --version

# Source-to-source test
docker exec rose-dev bash -c 'echo "int main(){return 0;}" > /tmp/test.c && \
  /rose/install/bin/rose-compiler -c /tmp/test.c && cat rose_test.c'

# Enter container shell
docker exec -it rose-dev bash
docker exec -it rose-cmake bash
```

## 构建时间

| 构建系统          | 首次构建          | 增量构建          |
|------------------|------------------|------------------|
| Autotools (`make core -j8`)    | 约 60-90 分钟        | 几秒钟至几分钟                    |
| CMake (`make -j4`)      | 约 35 分钟        | 几秒钟至几分钟                    |
- `librose.so` 文件大小：CMake 构建方式约为 200 MB；Autotools 构建方式（包含调试信息）约为 1.3 GB |
- 内存使用：在 16GB 内存系统中使用 `-j4` 以避免内存不足（OOM）问题 |

## 故障排除

| 故障类型            | 解决方案                                      |
|------------------|-----------------------------------------|
| EDG 下载失败        | 使用 `weekly` 分支（其中包含 EDG 二进制文件）             |
| CMake：ROSETTA 生成失败    | 升级到 CMake 4.x 版本                   |
| CMake：EDG 链接错误      | 确保使用最新的 CMake 修复补丁（PR #250）             |
| CMake：quadmath 相关错误      | 添加 `-lquadmath` 参数或使用最新修复补丁             |
| 权限问题            | 检查卷挂载权限                         |
| 内存不足           | 降低 `-j` 参数的值（减少并行构建的线程数）             |
| Boost 库未找到        | 在 `configure/cmake` 配置文件中检查 Boost 库的安装路径     |

## 使用示例代码进行测试

```bash
# Create factorial test
cat << 'EOF' | docker exec -i rose-cmake tee /tmp/factorial.cpp
#include <iostream>
int factorial(int n) { return n <= 1 ? 1 : n * factorial(n-1); }
int main() {
    for(int i = 0; i <= 10; i++)
        std::cout << "factorial(" << i << ") = " << factorial(i) << std::endl;
    return 0;
}
EOF

# Run through ROSE (source-to-source transformation)
docker exec -w /tmp rose-cmake /rose/build/bin/rose-compiler factorial.cpp

# Compile and run the transformed code
docker exec -w /tmp rose-cmake g++ rose_factorial.cpp -o factorial_test
docker exec -w /tmp rose-cmake ./factorial_test
```

## 预期输出结果

```
factorial(0) = 1
factorial(1) = 1
...
factorial(10) = 3628800
```