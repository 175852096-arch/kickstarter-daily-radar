# 小白安装说明

## 你只需要做 4 件事

### 1. 上传文件

在你的 GitHub 仓库首页点击：

Add file → Upload files

把这个压缩包解压后的全部文件上传。

注意：`.github` 是隐藏目录，如果网页上传不方便，可以先上传其他文件，再按 README 的方式添加 workflow。

### 2. 打开 Actions

进入仓库顶部的：

Actions

如果看到 GitHub 提示 workflow 被阻止，按页面提示允许 workflow。

### 3. 手动测试

在 Actions 中找到：

Kickstarter Daily Radar

点击：

Run workflow

运行成功后，到：

reports/

查看今天的 Markdown 日报。

### 4. （推荐）加入 AI Key

如果要让日报自动分析“为什么值得关注”，需要一个 OpenAI API Key。

在 GitHub：

Settings → Secrets and variables → Actions → New repository secret

名称填写：

OPENAI_API_KEY

值填写你的 API Key。

不要把 API Key 写进代码，也不要把它发到聊天里。

## 日后你不用做什么

正常情况下，每天 09:00 GitHub Actions 会自动运行。
