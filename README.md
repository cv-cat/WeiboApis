<div align="center">
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
    </a>
    <a href="https://fastapi.tiangolo.com/">
        <img src="https://img.shields.io/badge/FastAPI-0.115%2B-009688" alt="FastAPI">
    </a>
</div>

# 🐦 Weibo Platform

**✨ 专业的微博数据采集与发布解决方案，支持微博内容抓取、搜索及图文/视频发布**

当你需要让 AI Agent 感知微博内容生态——自动采集热点舆论、分析用户动态、驱动内容运营策略——第一道墙往往不是模型能力，而是**平台数据获取能力的缺失**。

本项目做的事很简单：把这道墙拆掉。

**⚠️ 严禁用于爬取用户隐私、违规商业用途！本项目仅供学习与技术研究使用，后果自负。**

## 🌟 功能特性

- ✅ **微博内容采集**
  - 通过移动端 API 获取微博帖子详情
  - 支持关键词搜索微博内容
  - 获取指定用户的全部发布微博（含翻页）
- 📤 **微博内容发布**
  - 支持发布**图文**微博（最多 15 张图）
  - 支持发布**视频**微博（含上传进度轮询）
  - 支持设置话题、地点、可见范围
- 🚀 **高性能服务**
  - 基于 FastAPI + Uvicorn 异步服务
  - 支持 Docker 一键部署

## 📁 项目结构

```
weibo/
├── app.py                      # FastAPI 入口
├── apis/
│   ├── weibo_apis.py           # PC 端接口（用户信息、发帖、评论）
│   ├── weibo_mobile_apis.py    # 移动端接口（搜索、帖子详情）
│   └── weibo_creator_apis.py   # 创作者接口（上传图片/视频、发布微博）
├── utils/
│   ├── weibo_utils.py          # 公共请求头、Cookie 工具
│   ├── weibo_mobile_utils.py   # 移动端请求头
│   └── weibo_creator_utils.py  # 创作者端签名、上传参数工具
├── Dockerfile
└── requirements.txt
```

## 🛠️ 快速开始

### ⛳ 运行环境

- Python 3.10+

### 🎯 本地安装

```bash
pip install -r requirements.txt
```

### 🚀 运行项目

```bash
python app.py
```

服务启动后访问 http://localhost:9999/docs 查看交互式 API 文档。

### 🎨 Cookie 配置

在浏览器中打开 [weibo.com](https://weibo.com)，**登录账号**后按 `F12` 打开开发者工具，点击「网络」→ 找任意一个 API 请求 → 复制请求头中的 `Cookie` 字段值。

> ⚠️ 注意：必须登录后获取的 Cookie 才有效，其中 `XSRF-TOKEN` 字段用于接口鉴权，缺失将导致请求失败。

将获取到的 Cookie 字符串作为 `cookies_str` 参数传入接口，格式如下：

```
SCF=xxx; SUB=xxx; XSRF-TOKEN=xxx; ...
```

## 📡 接口说明

### POST `/get_work_info`

通过移动端接口获取**单条微博**的详细信息。

**请求参数**

| 字段      | 类型  | 必填 | 说明           |
|---------|-----|----|--------------|
| work_id | str | 是  | 微博 ID（帖子 ID）|

**请求示例**

```bash
curl -X POST http://localhost:9999/get_work_info \
  -H "Content-Type: application/json" \
  -d '{"work_id": "5073209014095008"}'
```

**响应示例**

```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "work_info": {
      "status": {
        "id": "5073209014095008",
        "text": "微博正文内容",
        "user": { "name": "用户昵称" },
        "pic_ids": []
      }
    }
  }
}
```

---

### POST `/search_work`

通过移动端接口**搜索**微博内容。

**请求参数**

| 字段    | 类型  | 必填 | 说明       |
|-------|-----|----|----------|
| query | str | 是  | 搜索关键词    |
| page  | int | 是  | 页码（从 1 开始）|

**请求示例**

```bash
curl -X POST http://localhost:9999/search_work \
  -H "Content-Type: application/json" \
  -d '{"query": "人工智能", "page": 1}'
```

**响应示例**

```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "works": {
      "data": {
        "cards": [...]
      }
    }
  }
}
```

---

### POST `/get_user_posted`

获取**指定用户**发布的微博列表（需登录 Cookie）。

**请求参数**

| 字段          | 类型  | 必填 | 说明                        |
|-------------|-----|----|---------------------------|
| user_id     | str | 是  | 微博用户 ID                   |
| page        | int | 是  | 页码                        |
| since_id    | str | 否  | 翻页游标（上一页响应中的 `since_id`）   |
| cookies_str | str | 是  | 微博登录 Cookie 字符串           |

**请求示例**

```bash
curl -X POST http://localhost:9999/get_user_posted \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "5266778656",
    "page": 1,
    "cookies_str": "SCF=xxx; SUB=xxx; XSRF-TOKEN=xxx"
  }'
```

**响应示例**

```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "data": {
      "list": [...],
      "since_id": "5073209014095007"
    }
  }
}
```

## 🐳 Docker 部署

```bash
docker build -t weibo-platform .
docker run -d -p 9999:9999 weibo-platform
```

## 🍥 日志

| 日期       | 说明                                     |
|----------|----------------------------------------|
| 26/04/10 | 项目初始化，完成微博内容采集与图文/视频发布 API 封装，文件命名规范化 |

## 🤝 欢迎贡献 PR

本项目欢迎任何形式的贡献！如果你有新功能想法、Bug 修复或文档改进，欢迎提交 PR。

- Fork 本仓库并在新分支上开发
- 保持代码风格与现有代码一致
- PR 描述中请简要说明改动内容和目的
- 也欢迎通过 Issue 提出建议或报告问题

## 🧸 额外说明
1. 感谢 star⭐ 和 follow📰！不时更新
2. 作者的联系方式在主页里，有问题可以随时联系我
3. 可以关注下作者的其他项目，欢迎 PR 和 issue
4. 感谢赞助！如果此项目对您有帮助，请作者喝一杯奶茶~~ （开心一整天😊😊）
5. thank you~~~
