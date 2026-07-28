from playwright.sync_api import sync_playwright

class PlayWrightResourceManager:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()
        self.has_performed_clean_up = False
    
    def close_resources(self):
        if self.has_performed_clean_up:
            return
        
        try:
            self.browser.close()    
        except Exception:
            pass
        
        try:
            self.playwright.stop()
        except Exception:
            pass
        
        self.has_performed_clean_up = True
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.close_resources()
