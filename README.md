# Pay for Tools - 消费记录管理系统

一个简洁美观的消费记录管理系统，采用 Claymorphism 设计风格。

## 功能特性

- 📝 记录消费信息（商家、金额、时间、订单号、分类）
- 📊 按月份统计支出
- 🏷️ 按分类统计支出
- 📸 支付凭证截图存档
- 💬 支出备注管理

## 技术栈

- **后端**: Flask + SQLite
- **前端**: Claymorphism UI 设计
- **配色**: 靛蓝主色 (#4F46E5) + 绿色强调 (#22C55E)
- **字体**: Baloo 2 (标题) + Comic Neue (正文)

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python init_db.py
```

### 3. 运行服务

```bash
python app.py
```

### 4. 访问

http://localhost:5007

## 部署

默认端口：5007

## 分类

- API/AI服务
- 云服务
- 数码配件
- 游戏/娱乐
- 日用百货
- 软件开发
- 其他

## 数据库结构

查看 `schema.sql` 了解数据库结构。

使用 `init_db.py` 初始化数据库。

## License

MIT
