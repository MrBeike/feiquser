# feiquser
a tool to collect users account and offer search service.
> 主要是飞秋经常找不到好友，有时候又不记得对方IP地址，很是麻烦。可以选一台机器作为主机，提前多刷点好友出来，然后解析保存好友信息，然后利用飞秋机器人的功能，构造简单的查询服务。
  
## 功能说明
- userParser.py
> 1.利用飞秋软件提供的接口导出好友信息，并解析存储。
- webService.py
> 2.利用飞秋软件提供的“飞秋机器人”功能实现飞秋好友IP查询功能。（仅限1中已存储的好友信息。）
-  msger.py
> 利用简单的飞鸽协议实现与飞秋通信。（仅简单尝试，未完整实现。飞秋兼容飞鸽协议，且飞秋协议未公开。网上参考资料不多）

## 参考资料
> 飞秋官方博客 http://blog.sina.com.cn/s/articlelist_3233466723_0_1.html
> 飞秋机器人设置：http://blog.sina.com.cn/s/blog_c0bac9630101ao4i.html
> 飞秋接口信息  http://blog.sina.com.cn/s/blog_c0bac9630101ao0r.html