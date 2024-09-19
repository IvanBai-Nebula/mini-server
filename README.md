# mini_server

## 介绍

这是为本次小程序开发设计的后端服务。

## 软件架构

软件架构说明：项目当前划分以模块化的方式，分为四大基础模块若干小模块：

1. 用户模块。（包含用户信息、用户收藏、用户浏览记录、用户答题排行榜、用户健康数据等）
2. 媒体模块。（包含文章、音频、视频等）
3. 题目模块。（包含主题内容、题目等）
4. 通用模块。（包含基类定义、通用工具等）

## 技术栈（均为较新版本）

1. Python 3.10及以上版本
2. Django 5.0及以上版本
3. MySQL 8.0及以上版本

## 使用说明

1. 安装依赖包：运行命令 `pip install -r requirements.txt`
   。如果本地Python版本较低或希望不干扰现有环境，建议使用PyCharm内置的虚拟环境（该虚拟环境基于本地Python版本）或conda虚拟环境（需单独安装，支持配置多个不同版本的Python环境）。
2. 修改数据库配置：在`mini_server/settings.py`文件中的`DATABASES`部分，可将其设置为你本地的数据库。后续部署时将切换至服务器上的数据库。
