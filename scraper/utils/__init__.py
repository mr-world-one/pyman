IMPLICIT_TIMEOUT = 3
EXPLICIT_TIMEOUT = 5

# webdriver options arguments
SELENIUM_OPTIONS = [
    '--headless=new',
    '--disable-gpu',
    '--incognito',
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-blink-features=AutomationControlled',
    '--window-size=1920,1080',
    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
]

SELENIUM_EXPERIMENTAL_OPTIONS = {
    "profile.managed_default_content_settings.images": 2,  # відключення картинок
    "profile.managed_default_content_settings.stylesheets": 2,  # відключення css
    "excludeSwitches": ["enable-automation"],
    "useAutomationExtension": False,
}

MAX_ATTEMPTS = 3
DELAY = 0.8
