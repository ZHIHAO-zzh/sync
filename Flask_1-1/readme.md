
# Yuedazi 项目

## 项目简介

`Yuedazi` 是一个基于 Flask 的活动管理与社交平台，用户可以注册、登录、创建活动、参与活动，并通过实时聊天功能与其他用户交流。项目使用 MySQL 数据库存储数据，通过 Flask-SocketIO 实现实时聊天功能，并使用 Alembic 进行数据库迁移管理。

### 功能特点
- 用户注册与登录（支持记住我功能）
- 创建、编辑、删除活动
- 参与或退出活动
- 实时聊天（基于活动和用户对）
- 活动广场（支持搜索和排序）
- 个人主页（编辑用户信息、注销账号）
- 自动删除过期活动（每小时检查）

## 环境要求

在部署项目之前，请确保你的电脑满足以下要求：

- **操作系统**：Windows、macOS 或 Linux
- **Python**：版本 3.8 或以上
- **MySQL**：版本 5.7 或以上（推荐 8.0）
- **pip**：Python 包管理工具（通常随 Python 安装）
- **Git**：用于克隆项目（可选）

## 安装步骤

以下是从零开始部署项目的详细步骤。

### 1. 克隆或下载项目

如果你有 Git，可以通过以下命令克隆项目：

```bash
git clone <项目仓库地址>
cd yuedazi
```

或者直接下载项目压缩包并解压到本地目录，例如 `yuedazi`。

### 2. 设置 Python 虚拟环境

为了避免依赖冲突，建议使用虚拟环境。

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

激活虚拟环境后，命令行前会出现 `(venv)` 提示。

### 3. 安装依赖

项目依赖列在 `requirements.txt` 中，使用以下命令安装：

```bash
pip install -r requirements.txt
```

### 4. 安装并配置 MySQL

#### 4.1 安装 MySQL
- **Windows**：下载 MySQL 安装程序（[MySQL Community Server](https://dev.mysql.com/downloads/mysql/)），按照提示安装。
- **macOS**：使用 Homebrew 安装：
  ```bash
  brew install mysql
  ```
- **Linux (Ubuntu)**：
  ```bash
  sudo apt update
  sudo apt install mysql-server
  ```

#### 4.2 启动 MySQL 服务
- **Windows**：通过服务管理器启动 MySQL，或使用命令：
  ```cmd
  net start mysql
  ```
- **macOS/Linux**：
  ```bash
  sudo systemctl start mysql  # Ubuntu/Debian
  # 或者
  brew services start mysql  # macOS with Homebrew
  ```

#### 4.3 配置 MySQL
登录 MySQL（默认安装后 root 用户可能没有密码）：

```bash
mysql -u root -p
```

按提示输入密码（如果没有设置密码，直接回车）。

创建数据库 `yuedazi`：

```sql
CREATE DATABASE yuedazi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

设置 root 用户密码为 `666666`（与 `config.py` 中的配置一致）：

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '666666';
FLUSH PRIVILEGES;
```

退出 MySQL：

```sql
EXIT;
```

#### 4.4 验证 MySQL 配置
确保 `config.py` 中的数据库 URI 正确：

```python
SQLALCHEMY_DATABASE_URI = 'mysql://root:666666@localhost/yuedazi?charset=utf8mb4'
```

如果你的 MySQL 用户名、密码或数据库名不同，请修改此配置。

### 5. 初始化数据库

#### 5.1 运行数据库迁移
项目使用 Alembic 管理数据库迁移。运行以下命令初始化数据库：

```bash
flask db upgrade
```

这会根据 `migrations` 文件夹中的迁移脚本创建必要的表（`user`、`activity`、`participation`、`message`）。

#### 5.2 验证数据库
登录 MySQL，检查表是否创建成功：

```bash
mysql -u root -p
```

输入密码 `666666`，然后：

```sql
USE yuedazi;
SHOW TABLES;
```

你应该看到以下表：
- `user`
- `activity`
- `participation`
- `message`

### 6. 运行项目

#### 6.1 修改 `run.py`（可选）
为了避免调试模式下 `use_reloader` 导致的 SocketIO 端口冲突，建议修改 `run.py`：

```python
from app import create_app, socketio
import eventlet

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)
```

#### 6.2 启动应用
运行以下命令启动项目：

```bash
python run.py
```

你应该看到类似以下输出：

```
Database URI: mysql://root:666666@localhost/yuedazi?charset=utf8mb4
 * Serving Flask app 'app' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

### 7. 访问项目

打开浏览器，访问：

```
http://localhost:5000
```

你将看到“活动广场”页面。如果没有活动，会显示“暂无活动”。

## 测试流程

以下是一个简单的测试流程，帮助你验证项目功能。

### 1. 注册用户
1. 点击导航栏的“注册”链接。
2. 填写信息：
   - 用户名：`user1`
   - 邮箱：`user1@example.com`
   - 密码：`password1`
   - 确认密码：`password1`
3. 点击“注册”，成功后会跳转到登录页面。

重复上述步骤，注册第二个用户：
- 用户名：`user2`
- 邮箱：`user2@example.com`
- 密码：`password2`

### 2. 登录并创建活动
1. 使用 `user2` 登录。
2. 点击“创建活动”，填写：
   - 标题：`Test Activity`
   - 描述：`This is a test activity.`
   - 开始时间：`2025-03-21 10:00`
   - 结束时间：`2025-03-21 12:00`
   - 地点：`Test Location`
   - 最大参与人数：`10`
3. 点击“创建活动”，成功后会跳转到活动广场，显示新创建的活动。

### 3. 参与活动并发起聊天
1. 注销 `user2`，使用 `user1` 登录。
2. 在活动广场点击 `Test Activity`，进入活动详情页面。
3. 点击“参与活动”，确认成功加入。
4. 在“活动创建者”部分，点击“与 user2 聊一聊”。
5. 进入聊天页面，发送一条消息，例如：“你好，user2！”。
6. 确认消息是否显示在聊天窗口中。

### 4. 检查最近聊天
1. 返回活动广场（`/`）。
2. 在“最近聊天”部分，确认是否显示与 `user2` 的会话。

## 常见问题解答

### 1. 启动时提示 `ModuleNotFoundError: No module named 'mysqlclient'`
- **原因**：缺少 MySQL 数据库驱动。
- **解决**：
  1. 确保已安装 `mysqlclient`：
     ```bash
     pip install mysqlclient
     ```
  2. 如果仍然失败，可能需要安装 MySQL 开发库：
     - **Ubuntu/Debian**：
       ```bash
       sudo apt-get install libmysqlclient-dev
       ```
     - **macOS**：
       ```bash
       brew install mysql-connector-c
       ```
     - **Windows**：安装 `mysql-connector-c`，然后重新安装 `mysqlclient`。

### 2. 启动时提示 `Access denied for user 'root'@'localhost'`
- **原因**：MySQL 用户名或密码错误。
- **解决**：
  1. 确认 MySQL root 用户密码是否为 `666666`。
  2. 如果不同，修改 `config.py` 中的 `SQLALCHEMY_DATABASE_URI`，或者重置 MySQL 密码：
     ```sql
     ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '新密码';
     ```

### 3. 聊天功能不生效（消息不显示）
- **原因**：可能是 SocketIO 连接问题。
- **解决**：
  1. 确保 `run.py` 中 `use_reloader=False`。
  2. 检查浏览器控制台是否有错误（F12 打开开发者工具）。
  3. 确保 `chat.html` 和 `index.html` 中的 SocketIO 地址正确：
     ```javascript
     const socket = io('http://' + document.domain + ':' + location.port, {
         transports: ['websocket']
     });
     ```

### 4. 数据库迁移失败
- **原因**：可能是数据库未创建或迁移脚本有问题。
- **解决**：
  1. 确保 `yuedazi` 数据库已创建。
  2. 运行：
     ```bash
     flask db upgrade
     ```
  3. 如果仍然失败，删除 `migrations` 文件夹，重新初始化：
     ```bash
     flask db init
     flask db migrate
     flask db upgrade
     ```

## 项目结构

```
yuedazi/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   ├── templates/
│   │   ├── activity_create.html
│   │   ├── activity_detail.html
│   │   ├── activity_edit.html
│   │   ├── activity_manage.html
│   │   ├── base.html
│   │   ├── chat.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── profile.html
│   │   └── register.html
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   └── routes.py
├── migrations/
│   ├── versions/
│   │   ├── 0035a381a617_increase_password_hash_length_to_255.py
│   │   ├── 1edca2b11346_add_conversation_id_to_message.py
│   │   └── e4c589b5a036_initial_migration_with_all_tables.py
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── config.py
├── requirements.txt
└── run.py
```

## 贡献

欢迎提交问题或改进建议！请通过 GitHub Issues 提交 bug 报告或功能请求。

## 许可证

本项目采用 MIT 许可证，详情请见 `LICENSE` 文件（如果有）。

---

以上 `README.md` 提供了从零部署项目的完整指南，涵盖了环境配置、安装步骤、运行方法、测试流程以及常见问题解答。用户可以按照步骤逐步操作，确保项目成功运行。如果需要进一步调整或补充内容，请告诉我！