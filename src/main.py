import os
import requests
import json
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 从环境变量获取配置
WEREAD_COOKIE = os.getenv("WEREAD_COOKIE", "")
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
NOTION_DB_ID = os.getenv("NOTION_DB_ID", "")

def debug_cookie(cookie):
    """深度调试Cookie有效性"""
    logger.info(f"Cookie长度: {len(cookie)}字符")
    logger.info(f"Cookie内容（部分）: {cookie[:50]}...")
    
    # 检查关键字段
    required_keys = ['wr_vid', 'wr_sid', 'wr_skey']
    missing_keys = [key for key in required_keys if key not in cookie]
    
    if missing_keys:
        logger.warning(f"缺少关键Cookie字段: {', '.join(missing_keys)}")
    
    # 测试API连接
    test_urls = {
        "用户信息": "https://i.weread.qq.com/user/notebooks",
        "书架数据": "https://i.weread.qq.com/shelf/friendCommon?type=1",
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Cookie": cookie,
        "Referer": "https://weread.qq.com/"
    }
    
    for name, url in test_urls.items():
        try:
            logger.info(f"测试API: {name} ({url})")
            response = requests.get(url, headers=headers, timeout=10)
            logger.info(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"响应包含字段: {list(data.keys())}")
                
                # 特别检查用户信息
                if name == "用户信息":
                    if "books" in data:
                        logger.info(f"获取到 {len(data['books'])} 本书籍")
                    else:
                        logger.warning("响应中未找到'books'字段")
            else:
                logger.warning(f"错误响应: {response.text[:200]}")
                
        except Exception as e:
            logger.error(f"测试失败: {str(e)}")
    
    return bool(not missing_keys and response.status_code == 200)

def get_bookshelf(cookie):
    """获取书架数据（带详细错误处理）"""
    url = "https://i.weread.qq.com/shelf/sync?synckey=0&lectureSynckey=0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Cookie": cookie,
        "Referer": "https://weread.qq.com/"
    }
    
    try:
        logger.info("请求书架数据...")
        response = requests.get(url, headers=headers, timeout=15)
        logger.info(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # 检查响应结构
            if "books" in data:
                books = data["books"]
                logger.info(f"获取到 {len(books)} 本书籍")
                return books
            else:
                logger.warning("响应中未找到'books'字段")
                logger.debug(f"完整响应: {json.dumps(data, indent=2)}")
        else:
            logger.warning(f"错误响应: {response.text[:200]}")
            
    except Exception as e:
        logger.error(f"请求异常: {str(e)}")
    
    return []

def main():
    logger.info("="*60)
    logger.info("微信读书同步到Notion - 调试版")
    logger.info("="*60)
    
    # 步骤1: 深度调试Cookie
    logger.info("开始Cookie深度调试...")
    cookie_valid = debug_cookie(WEREAD_COOKIE)
    
    if not cookie_valid:
        logger.error("❌ Cookie无效，请检查并更新")
        return
    
    # 步骤2: 获取书架数据
    logger.info("获取书架数据...")
    books = get_bookshelf(WEREAD_COOKIE)
    
    if not books:
        logger.error("❌ 书架数据为空，请检查微信读书账号状态")
        logger.info("可能原因:")
        logger.info("1. 微信读书账号没有书籍")
        logger.info("2. Cookie已过期")
        logger.info("3. API限制（尝试更换User-Agent）")
        return
    
    logger.info(f"成功获取 {len(books)} 本书籍，开始同步...")
    
    # 这里添加同步到Notion的代码
    # 由于是调试版，暂时省略实际同步逻辑
    
    logger.info("✅ 同步流程完成（调试版）")

if __name__ == "__main__":
    main()
