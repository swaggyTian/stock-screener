# 📈 A股智能选股器

一个基于 Streamlit 的网页选股工具，免费使用 akshare 数据源。

## ✨ 功能特点

- 📊 **实时行情** - 沪深A股全市场数据
- 🎯 **多维筛选** - 市值、PE、涨跌幅、换手率等
- 🏭 **行业过滤** - 支持主流行业板块筛选
- 📋 **灵活排序** - 按任意字段升序/降序排列
- 📥 **数据导出** - 支持 CSV/Excel 下载

## 🚀 本地运行

### 1. 安装依赖

```bash
cd stock-screener
pip install -r requirements.txt
```

### 2. 启动应用

```bash
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501

## 🌐 部署到 Streamlit Cloud（免费）

### 步骤：

1. **创建 GitHub 仓库**
   - 将 `stock-screener` 文件夹内容推送到 GitHub
   - 需要文件：`app.py` 和 `requirements.txt`

2. **注册 Streamlit Cloud**
   - 访问 https://streamlit.io/cloud
   - 用 GitHub 账号登录

3. **创建新应用**
   - 点击 "New app"
   - 选择你的 GitHub 仓库
   - 选择分支（main/master）
   - 输入入口文件：`app.py`
   - 点击 Deploy

4. **完成！**
   - 等待部署（约1-2分钟）
   - 获得一个公开的网页链接，如：`https://your-name-streamlit-app.streamlit.app`

## 📱 使用说明

1. 在左侧侧边栏设置筛选条件
2. 点击"🔄 加载最新数据"刷新数据
3. 查看筛选结果表格
4. 点击下载按钮导出数据

## ⚠️ 注意事项

- 数据来源：东方财富（akshare）
- 数据更新：实时行情，有一定延迟
- 免责条款：本工具仅供个人学习研究，不构成投资建议

## 📦 项目结构

```
stock-screener/
├── app.py              # 主程序
├── requirements.txt    # 依赖
└── README.md          # 说明文档
```

---

**有问题？随时问我！**
