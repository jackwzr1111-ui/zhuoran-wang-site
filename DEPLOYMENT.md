# 汪卓燃个人网站

静态网站源码。中文、English、Bahasa Melayu 共 15 个页面，包含个人主页、棕榈油研究、黑色系研究、中信期货和启迪之星案例及公开图表。

## 域名与托管

1. 通过你自己的注册商账号注册姓名域名，确认首年和续费价格。使用你自己控制的 GitHub 账号建立网站仓库。GitHub Free 支持从公开仓库发布 GitHub Pages。[GitHub Pages 与自定义域名](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages)
2. 把解压后的源码放到仓库根目录，包含 `.github/workflows/pages.yml`，默认分支设为 `main`。在仓库的 Settings → Pages → Build and deployment → Source 选择 GitHub Actions。该工作流读取实际的 Pages 地址，更新 `main` 后重新生成、发布页面。[GitHub Pages 工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
3. 在 GitHub 账号的 Pages 设置验证自定义域名，再在仓库设置添加该域名，按 GitHub 指示配置 DNS，启用 Enforce HTTPS。域名就绪后在 Actions 页面运行 **Publish portfolio**，让页面、语言链接和网站地图统一使用自定义域名。[验证域名](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages) · [配置域名](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
4. 新域名的各条路径能访问后，再让旧地址逐页转发到新地址，并更新简历和 LinkedIn 的站点链接。[Google 网站迁移说明](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes)

## 自行生成与发布

把 `https://www.example.com` 替换成确定后的公开主地址。Python 3 仅用标准库。

```sh
python build.py --site-url https://www.example.com
python -m http.server 8000 --bind 127.0.0.1 --directory dist
```

根域名构建完成后，可在 `http://127.0.0.1:8000/` 检查页面，再把 `dist/` 发布到静态托管。GitHub Pages 工作流会自动执行生成步骤。文案在 `portfolio.json`，图表和样式分别在 `dist/assets/` 和 `dist/style.css`。修改或新增案例时，在三种语言的 `cases` 中使用同一个 slug。发布后保留已有页面路径。

## 搜索收录与更新

- 在 [Google Search Console](https://search.google.com/search-console/) 建立 Domain 资源，用 DNS TXT 验证，提交新域名的 `/sitemap.xml`，用「网址检查」检查首页与主要案例的收录和 Google 选定的规范网址。[所有权验证](https://support.google.com/webmasters/answer/9008080) · [提交网站地图](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- 首页覆盖「汪卓燃」与「Zhuoran Wang」。案例页用具体问题做标题，延续原报告的图表、数据口径和结论。每次更新保留文章路径，在 Search Console 的「效果」按查询和页面查看曝光、点击与点击率。[Search Console 指南](https://developers.google.com/search/docs/monitor-debug/search-console-start)
