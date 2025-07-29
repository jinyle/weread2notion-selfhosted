# 新增临时测试脚本 test_cookie.py
import os
from weread import WeReadAPI

cookie = "你的Cookie"  # 替换为实际Cookie
api = WeReadAPI(cookie)
books = api.get_bookshelf()
print("书架数据:", books)  # 正常应返回书籍列表
