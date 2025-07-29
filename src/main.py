import os
from weread import WeReadAPI
from notion import NotionSync
from auth import refresh_cookie

def main():
    # 从环境变量获取配置
    weread_cookie = os.getenv("WEREAD_COOKIE")
    notion_token = os.getenv("NOTION_TOKEN")
    notion_db_id = os.getenv("NOTION_DB_ID")
    
    # 自动刷新Cookie（若手动配置则跳过）
    if not weread_cookie or "wr_rt" not in weread_cookie:
        weread_cookie = refresh_cookie()
    
    # 初始化API
    weread_api = WeReadAPI(weread_cookie)
    notion_sync = NotionSync(notion_token, notion_db_id)
    
    # 遍历书架书籍并同步笔记
    for book in weread_api.get_bookshelf():
        book_id = book["bookId"]
        book_name = book["title"]
        for highlight in weread_api.get_highlights(book_id):
            notion_sync.create_page(book_name, highlight)

if __name__ == "__main__":
    main()
# 在 notion.create_page 调用后添加：
try:
    notion_sync.create_page(book_name, highlight)
    print(f"✅ 已同步：{book_name} - {highlight['text'][:20]}...")
except Exception as e:
    print(f"❌ 同步失败：{e}")
    # 将错误写入日志文件
    with open("error.log", "a") as f:
        f.write(f"{datetime.now()}: {str(e)}\n")
