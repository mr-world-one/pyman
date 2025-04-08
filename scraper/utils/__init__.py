IMPLICIT_TIMEOUT = 3
EXPLICIT_TIMEOUT = 5

# webdriver options arguments
SELENIUM_OPTIONS = [
    '--headless',
    '--disable-gpu',
    '--incognito',
]

SELENIUM_EXPERIMENTAL_OPTIONS = {
    "profile.managed_default_content_settings.images": 2,  # відключення картинок
    "profile.managed_default_content_settings.stylesheets": 2,  # відключення css
}

MAX_ATTEMPTS = 3
DELAY = 0.8
