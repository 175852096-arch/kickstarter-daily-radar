# Kickstarter 每日新品雷达

这是一个适合小白用户的 GitHub Actions 自动化项目。

## 目标

每天新加坡时间 09:00 自动运行，生成一份中文日报：

- 过去约 24 小时发现的新 Kickstarter 项目
- TOP 10 值得关注项目
- 产品亮点
- 爆款潜力评分
- 商业机会
- 风险提醒
- 重点观察项目

## 重要说明

本版本采用“公开新闻/RSS 发现层 + 规则评分”的方式，不直接高频抓取 Kickstarter 项目页面。
Kickstarter 官方支持 Discover、Advanced Search 和 Just Launched 等发现方式；其官方支持页面也说明新上线项目会出现在 Just Launched 中。

由于不同地区/时间段的公开 RSS 可用性可能变化，本项目把发现源写成可配置项。默认使用 Google News RSS 搜索 Kickstarter 项目作为发现层。如果后续接入你有权限使用的 Kickstarter 数据/API，只需要替换 `scripts/collect.py` 的发现源即可。

## 第一次使用

1. 把整个项目上传到 GitHub 仓库。
2. 打开仓库的 Actions。
3. 如果 GitHub 要求确认 workflow，点击允许。
4. 手动运行一次 `Kickstarter Daily Radar`。
5. 查看 `reports/` 是否生成日报。

## 可选：AI 深度分析

如果你希望日报真正做到“分析产品亮点、商业机会、风险”，可以在 GitHub 仓库 Secrets 中加入：

- `OPENAI_API_KEY`

没有这个 Key 时，系统仍然可以运行，但会使用基础规则分析，不会调用 AI。

## 时间

每天 09:00，Asia/Singapore。
GitHub Actions 的 cron 使用 UTC，因此配置为 01:00 UTC。
