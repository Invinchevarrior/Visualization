# DeeoContact
一个前端:)

# 目录

- [快速开始](#快速开始)
  - [写在前面](#写在前面)
  - [如何使用](#如何使用)
  - [前端](#前端)
    - [配置Nginx](#配置nginx)

# 快速开始

## 写在前面

1. 推荐使用 [Visual Studio Code](https://code.visualstudio.com/)进行开发，无论是 `Python` 还是 `前端` 。
2. 推荐使用 `WSL2` 作为运行环境， 然后使用VSCode `连接到WSL` 进行开发。
3. 以下教程**全部**使用上述环境。

## 如何使用

1. 前端文件**直接**放入仓库
2. 后端文件放入 `server` 文件夹
3. 自己本地的测试文件等非项目所需的文件，使用 `.gitignore` 文件忽略。
> [!NOTE]
> `.gitignore` 文件格式如下：
> ```
> 文件夹名 #忽略整个文件夹
> 文件夹名/文件名 #忽略某个文件夹中的某个文件
> 文件名 #忽略某个文件
> ```

## 前端

### 配置Nginx

0. 为什么要使用Nginx

    如果你想要模拟正常的网页浏览，启动一个本地http服务是必要的。这是因为，直接使用浏览器打开文件使用的 `file` 协议无法解析es6（即JavaScript）等语法，所以我们需要启动一个本地http服务，从而可以通过 `http` 协议访问页面。

> [!IMPORTANT]
> 以下代码假设用户目录为 `/home/user` 请自行更改 \
> *Linux* 中默认 `~/` 文件夹为当前用户目录

1. 下载 `nginx` :
   ``` bash
    sudo apt install nginx
   ```
2. 在本地创建一个 `www` 文件夹用于存放工程文件，并在其中创建nginx配置文件夹:
   ``` bash
    cd ~
    mkdir www
    cd www
    mkdir nginx-config
   ```
3. 修改nginx配置文件，使得上一条中创建的文件夹中的配置能够被正常读取。
    ``` bash
        sudo vim /etc/nginx/nginx.conf
    ```
    打开后在 `http` 板块中添加一条 `include` 配置，最后样例如下
    ``` shell
        ...
        http {
        ...
        include /etc/nginx/conf.d/*.conf;
	    include /etc/nginx/sites-enabled/*;
        include /home/user/www/nginx-config/*; # 这一句为新增
        ...
        }
        ...
    ```
4. 以nginx默认服务配置文件为例，编写能够访问本地页面的配置文件
    > nginx默认的配置文件为 `/etc/nginx/sites-available/default`
    ```bash
        sudo cp /etc/nginx/sites-available/default ~/www/nginx-config/deepcontact
        vim ~/www/nginx-config/deepcontact
    ```
    你需要在 `server` 模块中进行如下操作：
     - 删去 `listen` 字段的 `default_server` 字段
     - 修改 `root` 字段的值为 `/home/user/www`
     - 修改 `server_name` 字段的值为 `localhost`

    最后的结果示例如下：
    ``` shell
        ...
        server {
            listen 80;
            listen [::]:80;
            root /home/user/www;
            index index.html index.htm index.nginx-debian.html;
            server_name localhost;
            ...
        }
        ...
    ```
5. 将编写的网页文件放入上述文件夹(~/www/)，并访问URL测试是否正常。
> [!NOTE]
> 1. 如果遇到网页无法加载，可以查看Nginx日志，一般为 `/var/log/nginx/access.log` 和 `/var/log/nginx/error.log`
> 2. 如果 `error.log` 报错 `Nginx stat() failed (13: Permission Denied)`, 可以查看[这篇博文](https://blog.csdn.net/ZeroCore_Zero/article/details/136265868)解决。