# Pack Doc Publish
非公开内部文档整理小型解决方案

实现功能：

+ 常用错词、敏感词替换
+ markdown -> html -> exe
+ 版本控制
+ 直接内网服务器发布




主要依赖工具：

+ [mkdocs](https://www.mkdocs.org/)：静态网站生成，markdown编写文档，将markdown转换成完整html静态网站
+ git:版本控制
+ [golang+go.rice](https://github.com/GeertJohan/go.rice)：提供httpserver+将htnl静态网站打包到二进制可执行文件
+ [fabric](http://www.fabfile.org/): 执行远程shell


主控安装上边的工具，其他参与者只需有git即可。

第一步：初始化文档目录

```shell
$ mkdocs new ProjectNameDoc
$ cd ProjectNameDoc && git init
$ echo "site" >> .gitignore
```
如果不不需要划分开发和用户，上边就初始化完成了。需要区分只需要使用创建几个分支即可，比如：

+ user分支：只包含用户使用文档
+ dev分支：只包含开发文档
+ master分支：包含所有文档，该分支只合并user，dev分支，不进行任何编辑性操作。

**注意**：根据mkdocs文档那个进行相关的文档配置（比如说版权信息，目录划分等等）

第二部：编辑文档

就是git checkout 、编辑markdown、git pull/push

第三步：打包发布

根据实际需求，修改`pack_doc_publish.py`中的配置，运行`pack_doc_publish.py`（需要`chmod +x`可执行权限） 或 `python3 pack_doc_publish.py`即可
