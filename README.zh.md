# selfDaily

[English](README.md) | [简体中文](README.zh.md)

selfDaily 是一个本地优先的 Markdown 日记网页应用。现在它通过一个很小的
Python 本地服务把日记保存为本地 Markdown 文件，所以你可以在不同浏览器之间
读取同一批日记，不再依赖浏览器缓存。

## 今天更新了什么

- 新增 `selfdaily-server.py`，用于启动页面并把日记保存到本地文件。
- 新增本地私有日记目录：`DailyNote/YYYY-MM-DD.md`。
- 新增 `.gitignore`，确保 `DailyNote/` 不会上传到 GitHub。
- 新增日常使用脚本：
  - `start-selfdaily.ps1`
  - `open-selfdaily.ps1`
  - `install-selfdaily-startup.ps1`
- 新增短路径：
  - `http://localhost:5177/`
  - `http://localhost:5177/note`
- 保留浏览器 `localStorage` 作为兜底和迁移来源：服务器没开时仍可临时写，服务器开启后可迁移到 `DailyNote/`。

## 本地启动

```powershell
python selfdaily-server.py
```

然后打开：

```text
http://localhost:5177/
```

下面这些地址也可以：

```text
http://localhost:5177/note
http://localhost:5177/daily-journal-ui.html
```

## 日常使用

安装当前用户的开机启动快捷方式：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install-selfdaily-startup.ps1
```

安装后，Windows 登录时会自动启动 SelfDaily 本地服务。手动打开日记可以运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\open-selfdaily.ps1
```

如果想在浏览器地址栏里用 `note` 打开，可以在浏览器里新增站点搜索/快捷关键字：

```text
快捷字：note
URL：http://localhost:5177/
```

有些浏览器需要输入 `note` 后，再按 `Tab` 或空格，然后回车。

## 数据与隐私

日记会保存到本地：

```text
DailyNote/YYYY-MM-DD.md
```

`DailyNote/` 已经被 Git 忽略。你的私人日记只留在本机，不会上传到 GitHub。

如果服务器没运行，应用会退回浏览器 `localStorage`。当服务器重新运行后，用同一个浏览器打开同一个 HTML 文件，可以把缓存里的日记合并回 `DailyNote/`。

## 当前功能

- 每个日期一篇日记
- 保存为 `DailyNote/` 里的本地 Markdown 文件
- Markdown 编辑器和实时预览
- 日历和日记列表
- 标题、心情、能量、标签字段
- 按日期、标题、标签、正文搜索
- 今日模板和复盘模板
- 导出当前日记为 Markdown
- 备份和导入日记数据
- 亮色/暗色主题

## 项目来源

这个项目基于 `woyin2024/lengyi-markdown-editor` 改造，目标是做成一个适合个人长期维护的日记项目。
