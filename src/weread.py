import requests
from datetime import datetime

class WeReadAPI:
    def __init__(self, cookie):
        self.cookie = cookie
        self.session = requests.Session()
        self.session.headers = {"Cookie": cookie}
    
    def get_bookshelf(self):
        """获取书架书籍列表"""
        url = "https://i.weread.qq.com/shelf/friendCommon"
        return self.session.get(url).json().get("books", [])
    
    def get_highlights(self, book_id):
        """获取书籍划线和笔记（自动区分类型）"""
        url = f"https://i.weread.qq.com/book/{book_id}/highlights"
        data = self.session.get(url).json()
        return [
            {
                "book_id": book_id,
                "text": item["markText"].strip(),
                "note": item.get("abstract", "").strip(),
                "type": "note" if "chapterTitle" in item else "highlight",
                "date": datetime.fromtimestamp(item["createTime"]).isoformat()
            }
            for item in data
        ]
