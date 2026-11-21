# 汪卓燃个人网站 · 前端交接

这是 wang-zhuoran.jackandwzr.chatgpt.site 公开第 3 版的完整静态站。首页和四个案例均有中文、English、Bahasa Melayu 三种版本，共 15 页。交接基线为 2026 年 11 月 22 日，源码提交为 `1dfd3e0f71077c62e1efcf2e7ccbd7211a26865a`。[查看线上基线](https://wang-zhuoran.jackandwzr.chatgpt.site/)

## 先跑起来

在解压后能看见 `build.py` 的目录打开终端。包内已备好可运行的 `dist/`，直接执行下列命令，再用浏览器打开 http://127.0.0.1:8000/ 。

~~~sh
python -m http.server 8000 --bind 127.0.0.1 --directory dist
~~~

英文入口是 `/en.html`，马来文入口是 `/ms.html`。本地服务器可用 Ctrl+C 停止。macOS 或 Linux 若使用 `python3`，以下命令也将 `python` 换成 `python3`。

## 改一处，怎样看到结果

| 想改的东西 | 编辑位置 | 如何预览 |
|---|---|---|
| 颜色、字体、留白、断点、导航样式 | `dist/style.css` | 保存后刷新浏览器 |
| 全站页眉、导航、语言切换、页脚、SEO 标签 | `build.py` 的 `page()` | 重新构建后刷新 |
| 首页、案例详情、启迪流程展示 | `build.py` 的 `homepage()`、`casepage()`、`workflow()` | 重新构建后刷新 |
| 三语文案、指标、经历、图注、流程状态 | `portfolio.json` | 重新构建后刷新 |
| 实际加载的四张研究图 | `dist/assets/` | 同路径替换可直接刷新。改名要同步更新模板 |
| 棕榈油图表的“查看大图”查看器 | `dist/zoom.js` | 保存后刷新。关闭 JavaScript 时图片链接直接打开原图 |
| 滚动渐显动效 | `dist/site.js` | 保存后刷新。关闭 JavaScript 或系统设为“减少动态效果”时内容直接显示 |
| 网页字体（Instrument Serif、Inter，自托管，OFL 许可） | `dist/fonts/` | 保存后刷新 |
| 首页数字带、方向标签、其他项目、教育、工具、语言、工作之外 | `portfolio.json` 每种语言的 `profile` | 重新构建后刷新 |
| 工作经历（含起止时间） | `portfolio.json` 的 `jobs`：机构、岗位、说明、关联案例 slug、时间 | 重新构建后刷新 |
| 界面短文案（跳转链接、语言代码、查看大图等）与案例重点模块 | `portfolio.json` 每种语言的 `ui` 和 `highlights` | 重新构建后刷新 |

~~~sh
python build.py --site-url https://wang-zhuoran.jackandwzr.chatgpt.site
python tools/check_site.py --site-url https://wang-zhuoran.jackandwzr.chatgpt.site
~~~

用线上基线地址构建时，页面内导航、样式和图片仍由本地服务器提供。该参数设置 canonical、hreflang、Open Graph URL 和 sitemap。接入自有域名后改为实际 HTTPS 地址。保留 `dist/style.css`、`dist/zoom.js`、`dist/site.js`、`dist/fonts/` 和 `dist/assets/`，它们是源码的一部分；生成器只重写 HTML、robots.txt 和 sitemap.xml。

## 技术栈与部署

- Python 静态生成器以标准库读取 JSON、渲染 HTML 并生成站点地图。本包用 Python 3.12 验证。前端是原生 HTML 和 CSS，启迪页的流程展开使用浏览器原生 `details/summary`。当前站点无需安装包、Node、数据库或 API 密钥。
- 生产站由 ChatGPT Sites 托管。`.openai/hosting.json` 记录原站标识和发布目录。运行本地命令即可开发。
- `.github/workflows/pages.yml` 是可选的 GitHub Pages 发布工作流。将来放进本人仓库，在 Pages 设置启用 GitHub Actions 后，由工作流读取该仓库的实际发布地址重新构建。个人域名待注册。域名、DNS、HTTPS 与 Search Console 的迁移步骤见 [DEPLOYMENT.md](DEPLOYMENT.md)。
- 只将 `dist/` 作为静态站发布目录。此交接包提供完整工程，包含开发文档和未部署的素材索引。

## 交接入口

| 文件或目录 | 用途 |
|---|---|
| [CLAUDE.md](CLAUDE.md) | 改版目标、按优先级排列的任务和逐条验收条件 |
| [content/README.md](content/README.md) | 栏目、15 条路径、逐页文案和素材索引 |
| `content/shared/` | 各语言共用的界面文案、现版文字标识的可复用文件 |
| `content/home/`、`content/palm-oil/` 等 | 按页型拆出的三语编辑参考与所用图片 |
| `dist/` | 已生成的全站，可本地预览及静态托管 |
| `tools/check_site.py` | 验证页面、内部链接、图表与 SEO 标记 |

## 2026-11-22 改版记录（CLAUDE.md P0 · 1–3）

- **P0 · 1 首页与手机导航**：手机页眉压成两行（姓名标识与 中 / EN / MS 语言代码一行，作品与经历一行），读屏仍读完整语言名。首页首屏依次为学位、姓名、方向、简介和 LinkedIn，代表研究卡片紧随其后。删除重复的“精选作品 ↓”按钮，作品卡片改为整卡一个链接，键盘 Tab 依次经过：跳到正文、导航、语言、LinkedIn、四个案例。新增“跳到正文”链接。
- **P0 · 2 详情页统一**：四个案例共用同一骨架：类别 · 研究/实习标签、标题、导语、作者署名与研究范围、指标条、重点模块、正文、其他作品卡片。棕榈油四张原图保留，点击可在页内查看大图（适应屏幕 / 原图 / 2 倍，可横向滚动看坐标轴）；无 JavaScript 时打开原图文件。黑色系突出螺纹盘面利润公式及“估算”说明；中信突出两套 14 页 QFI 材料及目录；启迪的四个流程节点改为可键盘展开的步骤卡，并新增 12 项 SOP 覆盖范围模块。
- **P0 · 3 三语与 SEO**：URL、canonical、hreflang、sitemap、JSON-LD 不变。`tools/check_site.py` 新增一项检查：每页的语言按钮必须指向同一篇文章的对应语言版本。全部正文为静态 HTML。
- 新增文案均为三语，写在 `portfolio.json` 的 `ui` 与 `highlights` 中；重点模块只复述案例正文已有的内容与数字。

## 2026-11-22 改版第二轮（视觉升级与内容扩充）

- 视觉：深色首屏（大号衬线姓名、方向标签、代表研究入口、关键数字带、研究品种滚动条），作品区改为代表研究大卡片加三张带封面的案例卡，经历改为带时间的时间线，新增其他项目、背景与能力、联系区块；全站深色页眉与页脚，跟随系统的深色模式，克制的滚动渐显。字体自托管，所有设备显示一致。
- 内容：新增鼎盛家族办公室实习、各段经历时间、沪深 300 多因子回测（注明历史回测）与铜采购套保方案（注明模拟练习）、教育背景、工具与证书、语言、运动经历。全部为站主提供的事实，三语同步。
- CLAUDE.md P1 · 5 联系入口：首页与每个案例页底部均有“在 LinkedIn 联系我”。
- 已在 Google Search Console 验证 GitHub Pages 地址并提交 sitemap；首页的 `google-site-verification` 标签不要删除。

## SEO 设置（2026-11-22）

- `build.py` 的 `structured_data()` 生成 Person 结构化数据：中英文名、Wang Zhuoran、Jack Wang、学校、语言、研究领域、所在地、LinkedIn 与邮箱。
- 社交分享卡片在 `dist/og/og-zh.png`、`og-en.png`、`og-ms.png`（1200×630），由 `og:image` 与 `twitter:card` 引用；网站图标为 `dist/favicon.svg`、`favicon-48.png`、`apple-touch-icon.png`。改名或改方向后需要重新生成分享卡片。
- Google Search Console 资源为 `https://jackwzr1111-ui.github.io/zhuoran-wang-site/`（网址前缀），已提交 `sitemap.xml`。
