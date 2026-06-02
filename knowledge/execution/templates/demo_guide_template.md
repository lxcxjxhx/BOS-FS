# 演示指南 — [项目名称]

---

## 📋 前置条件

在开始演示之前，请确保满足以下条件：

| 类别 | 要求 |
|------|------|
| **操作系统** | [Windows 10+ / macOS 11+ / Ubuntu 20.04+] |
| **运行环境** | [Python 3.9+ / Node.js 18+ / Java 17+ 等] |
| **依赖工具** | [git / docker / 其他必要工具] |
| **权限要求** | [管理员权限 / 特定API密钥 / 网络访问] |
| **推荐配置** | [CPU ≥ 4核, RAM ≥ 8GB, 磁盘 ≥ 10GB] |

---

## 📥 安装

### 步骤 1：克隆项目

```bash
git clone [仓库地址]
cd [项目名称]
```

### 步骤 2：安装依赖

```bash
# 使用包管理器安装依赖
[安装命令，如: pip install -r requirements.txt]
# 或
[安装命令，如: npm install]
```

### 步骤 3：验证安装

```bash
# 运行版本检查或健康检测
[验证命令，如: 项目名称 --version]
```

**预期输出**：`[期望看到的输出内容]`

---

## ⚙️ 配置

### 步骤 4：创建配置文件

```yaml
# config.yaml — 项目配置文件

# === 基础配置 ===
app:
  name: "[项目名称]"          # 应用名称
  port: 8080                  # 服务端口
  debug: false                # 调试模式（生产环境设为false）

# === 数据库配置 ===
database:
  host: "localhost"           # 数据库地址
  port: 5432                  # 数据库端口
  name: "[数据库名]"          # 数据库名称
  user: "[用户名]"            # 连接用户名
  # password 通过环境变量 DB_PASSWORD 设置，勿明文写入

# === AI/模型配置 ===
model:
  provider: "[供应商]"        # 模型供应商（如 openai/anthropic）
  api_key_env: "API_KEY"      # API密钥环境变量名
  default_model: "[模型名]"   # 默认使用的模型

# === 日志配置 ===
logging:
  level: "INFO"               # 日志级别: DEBUG / INFO / WARN / ERROR
  format: "json"              # 日志格式: text / json
```

### 步骤 5：设置环境变量

```bash
# Linux / macOS
export API_KEY="your-api-key-here"
export DB_PASSWORD="your-db-password"

# Windows (PowerShell)
$env:API_KEY = "your-api-key-here"
$env:DB_PASSWORD = "your-db-password"
```

---

## ▶️ 运行

### 步骤 6：启动服务

```bash
# 开发模式（含热重载）
[启动命令，如: 项目名称 run --dev]

# 生产模式
[启动命令，如: 项目名称 run --prod]
```

### 步骤 7：访问服务

```bash
# 检查服务状态
[健康检查命令，如: curl http://localhost:8080/health]
```

**预期输出**：

```json
{"status": "healthy", "version": "1.0.0"}
```

---

## ✅ 验证清单

演示完成后，请逐项确认：

- [ ] **服务启动成功**：进程运行中，无报错日志
- [ ] **健康检查通过**：`/health` 接口返回 `healthy`
- [ ] **[核心功能1]**：[描述预期结果]
- [ ] **[核心功能2]**：[描述预期结果]
- [ ] **[核心功能3]**：[描述预期结果]
- [ ] **性能达标**：响应时间 < [X]ms，无内存泄漏
- [ ] **日志正常**：无 ERROR 级别异常输出

---

## ❓ 常见问题

### Q1: [常见问题1，如：启动时报端口占用]

**A**：[解决方案，如：修改配置中的 `port` 值，或关闭占用端口的进程]

```bash
# 查看占用端口的进程
[排查命令，如: lsof -i :8080]
```

### Q2: [常见问题2，如：API密钥未配置]

**A**：[解决方案，如：检查环境变量是否正确设置，重启服务]

### Q3: [常见问题3，如：依赖安装失败]

**A**：[解决方案，如：检查网络连接，使用镜像源重试]

```bash
# 使用镜像源安装
[命令示例，如: pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple]
```

---

## 🧹 清理（可选）

演示结束后，如需清理环境：

```bash
# 停止服务
[停止命令]

# 清理临时文件
[清理命令]

# 删除测试数据
[删除命令]
```
