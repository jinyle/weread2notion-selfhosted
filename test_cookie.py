# 新增临时测试脚本 test_cookie.py
import os
from weread import WeReadAPI

cookie = "wr_fp=2254754768; wr_localvid=afc3288068debb8afcc413c; wr_name=Delphin; wr_gender=2; wr_vid=9300920; wr_rt=web%40HaUUVb66Gpfj7u6HrRL_AL; wr_pf=NaN; webwx_data_ticket=gSdbZ57Q4RqnxRHuAMXL03V7; wr_gid=255171478; _qpsvr_localtk=0.0756057118260588; uin=o0244104022; skey=@hg9P2rufj; RK=yFmlwO4uT/; ptcz=f19bbd35649d18424401cb385963add4792f5f2b2f163ce79f84daf62f57b6b3; wr_avatar=https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FPiajxSqBRaEKy4XBibFOicw9RxvJbciaotzyXKcrJ7uEV7xiar2or6l5Q3msU3FRByuBDA68GfFa9Hj6RxtkKlZQP5w%2F132; wr_skey=pFElvRaN"  # 替换为实际Cookie
api = WeReadAPI(cookie)
books = api.get_bookshelf()
print("书架数据:", books)  # 正常应返回书籍列表
