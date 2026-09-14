---
title: "Artifactory 是什么"
date: 2026-09-14T23:09:31+08:00
lastmod: 2026-09-14T23:09:31+08:00
author: "Luca"
tags: ["Tech"]
draft: false
slug: "20260914-artifactory"
---

Artifactory 是 JFrog 做的软件包仓库，可以把它理解成开发团队的软件仓库。Python 包、npm 包、Docker 镜像、编译好的程序，都可以放进去，供其他项目或服务器下载。

Git 保存源代码和修改记录。Artifactory 保存开发时用到的软件包，以及代码打包后的成品。

拿一个 Python 服务来说：代码提交到 GitHub 后，自动构建程序通过 Artifactory 下载依赖，完成测试，再把做好的 Docker 镜像上传到 Artifactory。部署时，生产服务器从这里下载指定版本的镜像。

除了保存团队自己的包，它还能代理 PyPI、npm 等公共仓库，把下载过的包缓存下来。后续构建可以复用缓存，减少重复下载和对外网的依赖。开发工具里出现 `artifactory` 地址，通常就是在通过这样的仓库取包。

多个项目共享内部包、集中保存发布版本时，会用到这类工具。它可以部署在自己的服务器上，也可以使用 JFrog 的云服务。

来源：[JFrog Artifactory 概览](https://docs.jfrog.com/artifactory/docs/jfrog-artifactory)、[仓库类型](https://docs.jfrog.com/artifactory/docs/repository-management)。
