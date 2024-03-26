# 文件共享服务

后台界面图
![图片](./web/static/images/1.png)

生成 orm 
```python
flask-sqlacodegen mysql://root:123456@127.0.0.1:3306/file_server?charset=utf8mb4 --outfile "common/models/Model.py"  --flask
```