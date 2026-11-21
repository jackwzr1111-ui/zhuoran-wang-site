# 栏目与素材索引

首页呈现两组信息。精选作品以棕榈油研究领衔，下接黑色系、中信期货和启迪会员项目；工作经历涵盖中信期货、启迪之星（马来西亚）和广发证券。页脚提供机构业务训练室与 LinkedIn 入口。KL Commodity Desk 文章列表列入下一轮开发任务。

| 素材目录 | 中文 URL | English URL | Bahasa Melayu URL |
|---|---|---|---|
| [home](home/) · 主页 | `/` | `/en.html` | `/ms.html` |
| [palm-oil](palm-oil/) · 棕榈油 | `/work/palm-oil.html` | `/work/palm-oil-en.html` | `/work/palm-oil-ms.html` |
| [ferrous](ferrous/) · 黑色系 | `/work/ferrous.html` | `/work/ferrous-en.html` | `/work/ferrous-ms.html` |
| [citic-futures](citic-futures/) · 中信期货 | `/work/citic-futures.html` | `/work/citic-futures-en.html` | `/work/citic-futures-ms.html` |
| [tusstar-membership](tusstar-membership/) · 启迪会员体系 | `/work/tusstar-membership.html` | `/work/tusstar-membership-en.html` | `/work/tusstar-membership-ms.html` |

每个目录里的 `zh-CN.md`、`en.md` 和 `ms.md` 均从上线版内容提取。首页和棕榈油目录附该页使用的 WebP 原图；其余三个案例的内容以文字、HTML 公式或原生折叠流程呈现。黑色系与启迪文案包含这些组件的可见文字。

**品牌与共用元素**放在 [shared](shared/) 目录。线上页眉直接排印“Zhuoran Wang”。`wordmark.html` 提取了现有链接样式；`wordmark.svg` 是可交给设计工具使用的同文字版本，实际字形取决于设备字体。页面中没有使用公司 Logo。

**正式编辑位置**为根目录 `portfolio.json`（三种语言分别为一条记录）、`build.py`（页型、公共组件与语言链接）和 `dist/assets/`（正式图片）。每项 `cases` 按顺序包含 slug、品类、标题、摘要、范围或数据时点、正文章节、指标。每项 `jobs` 包含机构、岗位、说明和关联案例 slug。图表标签顺序对应 `build.py` 的 `FIGURES`。本目录便于挑选文案与素材，改版提交以正式编辑位置为准。
