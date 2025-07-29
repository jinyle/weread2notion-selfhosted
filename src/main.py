import os
import logging
from datetime import datetime
from weread import WeReadAPI
from notion import NotionSync
from auth import refresh_cookie

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 控制台输出
        logging.FileHandler('sync.log')  # 日志文件
    ]
)

def main():
    try:
        # 从环境变量获取配置
        weread_cookie = os.getenv("WEREAD_COOKIE")
        notion_token = os.getenv("NOTION_TOKEN")
        notion_db_id = os.getenv("NOTION_DB_ID")
        
        # 验证环境变量
        if not all([weread_cookie, notion_token, notion_db_id]):
            missing = []
            if not weread_cookie: missing.append("WEREAD_COOKIE")
            if not notion_token: missing.append("NOTION_TOKEN")
            if not notion_db_id: missing.append("NOTION_DB_ID")
            raise EnvironmentError(f"缺少必需的环境变量: {', '.join(missing)}")

        # 自动刷新Cookie（若手动配置无效）
        if not weread_cookie or "wr_rt" not in weread_cookie:
            logging.warning("⚠️ Cookie无效或过期，尝试自动刷新...")
            weread_cookie = refresh_cookie()
            logging.info("✅ Cookie刷新成功")

        # 初始化API
        weread_api = WeReadAPI(weread_cookie)
        notion = NotionSync(notion_token, notion_db_id)  # 修正变量名
        
        # 获取书架数据
        bookshelf = weread_api.get_bookshelf()
        if not bookshelf:
            logging.warning("⚠️ 书架数据为空，请检查微信读书账号状态")
            return
        
        logging.info(f"📚 检测到 {len(bookshelf)} 本书籍，开始同步笔记...")
        
        # 遍历书籍并同步笔记
        for book in bookshelf:
            book_id = book["bookId"]
            book_name = book["title"]
            logging.info(f"📖 正在处理《{book_name}》(ID: {book_id})")
            
            # 获取书籍笔记
            highlights = weread_api.get_highlights(book_id)
            if not highlights:
                logging.warning(f"⚠️ 本书无笔记: 《{book_name}》")
                continue
                
            # 同步到Notion
            success_count = 0
            for highlight in highlights:
                try:
                    # 检查是否重复（可选）
                    # if not notion.check_duplicate(highlight["text"]):
                    notion.create_page(book_name, highlight)
                    success_count += 1
                except Exception as e:
                    logging.error(f"❌ 笔记同步失败: {str(e)}", exc_info=True)
            
            logging.info(f"✅ 《{book_name}》同步完成: {success_count}/{len(highlights)} 条笔记")
        
        logging.info("🎉 同步任务完成")

    except Exception as e:
        logging.critical(f"🔥 同步进程崩溃: {str(e)}", exc_info=True)
        with open("crash.log", "a") as f:
            f.write(f"{datetime.now().isoformat()}: {str(e)}\n")

if __name__ == "__main__":
    main()
