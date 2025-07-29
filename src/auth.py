from playwright.sync_api import sync_playwright

def refresh_cookie():
    """使用Playwright自动登录获取Cookie"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://weread.qq.com/")
        page.wait_for_selector("text=微信扫码登录", timeout=60000)  # 等待60秒扫码
        page.wait_for_load_state("networkidle")
        cookies = page.context.cookies()
        browser.close()
        return "; ".join([f"{c['name']}={c['value']}" for c in cookies])
