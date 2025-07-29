from notion_client import Client

class NotionSync:
    def __init__(self, token, database_id):
        self.notion = Client(auth=token)
        self.database_id = database_id

    def create_page(self, book_name, highlight):
        """在Notion数据库创建笔记条目"""
        properties = {
            "书名": {"title": [{"text": {"content": book_name}}]},
            "日期": {"date": {"start": highlight["date"]}},
            "类型": {"select": {"name": highlight["type"]}},
            "内容": {"rich_text": [{"text": {"content": highlight["text"]}}]},
            "批注": {"rich_text": [{"text": {"content": highlight.get("note", "")}}]}
        }
        self.notion.pages.create(parent={"database_id": self.database_id}, properties=properties)
