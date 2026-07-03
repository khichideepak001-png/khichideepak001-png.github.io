"""
Stealth browser utilities for ErgoElite bot.
Provides human-like browser automation using playwright-stealth
to bypass Reddit, Pinterest, and Quora bot detection.
"""

import random
import time
from playwright.sync_api import sync_playwright, Page, BrowserContext

# Try importing playwright-stealth (v2.x with Stealth context manager)
try:
    from playwright_stealth import Stealth
    HAS_STEALTH = True
    print("[Stealth] playwright-stealth loaded OK")
except ImportError:
    HAS_STEALTH = False
    print("[Stealth] playwright-stealth NOT available — running without stealth patches")


# Realistic user agents (rotated randomly per session)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
]

# Screen resolutions for viewport randomization
VIEWPORTS = [
    {"width": 1920, "height": 1080},
    {"width": 1536, "height": 864},
    {"width": 1440, "height": 900},
    {"width": 1366, "height": 768},
    {"width": 1680, "height": 1050},
    {"width": 2560, "height": 1440},
]


def get_random_ua():
    """Return a random user agent string."""
    return random.choice(USER_AGENTS)


def get_random_viewport():
    """Return a random viewport size dict."""
    return random.choice(VIEWPORTS)


def human_delay(min_sec=0.5, max_sec=2.5):
    """Sleep for a random human-like duration."""
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)
    return delay


def human_type(page: Page, text: str, min_delay_ms=30, max_delay_ms=120):
    """
    Type text character-by-character with random delays
    to mimic human typing speed (50-100 WPM).
    """
    for char in text:
        page.keyboard.type(char)
        delay_ms = random.randint(min_delay_ms, max_delay_ms)
        time.sleep(delay_ms / 1000.0)
        # Occasional longer pause (simulating thought)
        if random.random() < 0.05:
            time.sleep(random.uniform(0.3, 0.8))


def human_scroll(page: Page, direction="down", distance=None):
    """Scroll the page in a human-like manner with variable speed."""
    if distance is None:
        distance = random.randint(200, 600)
    
    if direction == "down":
        page.mouse.wheel(0, distance)
    else:
        page.mouse.wheel(0, -distance)
    
    human_delay(0.3, 1.0)


def human_mouse_move(page: Page, x: int, y: int):
    """
    Move the mouse to (x, y) with slight jitter to
    avoid perfectly straight lines that trigger detection.
    """
    # Add small random offset
    jitter_x = x + random.randint(-5, 5)
    jitter_y = y + random.randint(-5, 5)
    
    page.mouse.move(jitter_x, jitter_y)
    human_delay(0.1, 0.3)


def human_click(page: Page, selector: str, timeout=10000):
    """
    Click an element with human-like behavior:
    1. Wait for it to be visible
    2. Scroll into view
    3. Move mouse to it (with jitter)
    4. Small pause
    5. Click
    """
    el = page.locator(selector).first
    el.wait_for(state="visible", timeout=timeout)
    el.scroll_into_view_if_needed()
    human_delay(0.2, 0.6)
    
    box = el.bounding_box()
    if box:
        # Click at a random position within the element, not dead center
        click_x = box["x"] + random.uniform(box["width"] * 0.2, box["width"] * 0.8)
        click_y = box["y"] + random.uniform(box["height"] * 0.2, box["height"] * 0.8)
        human_mouse_move(page, int(click_x), int(click_y))
        page.mouse.click(click_x, click_y)
    else:
        el.click()
    
    human_delay(0.3, 0.8)


def create_stealth_browser(pw, browser_type="chromium", headless=True, 
                            storage_state=None, channel=None):
    """
    Launch a stealth browser with all anti-detection patches applied.
    
    Returns: (browser, context, page)
    """
    ua = get_random_ua()
    viewport = get_random_viewport()
    
    # Browser launch arguments
    launch_args = [
        "--disable-blink-features=AutomationControlled",
        "--disable-infobars",
        "--no-first-run",
        "--no-default-browser-check",
        f"--window-size={viewport['width']},{viewport['height']}",
    ]
    
    launcher = getattr(pw, browser_type)
    
    launch_kwargs = {
        "headless": headless,
        "args": launch_args if browser_type == "chromium" else [],
    }
    if channel and browser_type == "chromium":
        launch_kwargs["channel"] = channel
    
    browser = launcher.launch(**launch_kwargs)
    
    context_kwargs = {
        "user_agent": ua,
        "viewport": viewport,
        "locale": "en-US",
        "timezone_id": "America/New_York",
        "color_scheme": "dark",
        "java_script_enabled": True,
    }
    if storage_state:
        context_kwargs["storage_state"] = storage_state
    
    context = browser.new_context(**context_kwargs)
    
    # Apply stealth scripts to the context
    if HAS_STEALTH:
        try:
            stealth = Stealth()
            stealth.apply_stealth_sync(context)
            print("[Stealth] Anti-detection patches applied OK")
        except Exception as e:
            # Fallback: apply basic anti-detection via JS injection
            print(f"[Stealth] Stealth v2 API failed ({e}), applying manual patches...")
            _apply_manual_stealth(context)
    else:
        _apply_manual_stealth(context)
    
    page = context.new_page()
    
    return browser, context, page


def _apply_manual_stealth(context: BrowserContext):
    """
    Manual stealth patches if playwright-stealth module isn't available
    or its API has changed. Covers the most common detection vectors.
    """
    stealth_js = """
    // Override navigator.webdriver
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    
    // Override navigator.plugins to look real
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5].map(() => ({
            length: 1,
            item: () => null,
            namedItem: () => null,
            description: 'Internal Plugin',
            filename: 'internal-plugin',
            name: 'Chrome PDF Plugin',
        }))
    });
    
    // Override navigator.languages
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    
    // Override chrome.runtime to prevent detection
    if (!window.chrome) window.chrome = {};
    if (!window.chrome.runtime) window.chrome.runtime = {};
    
    // Override permissions API
    const originalQuery = window.navigator.permissions?.query;
    if (originalQuery) {
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        )
    }
    """
    context.add_init_script(stealth_js)
    print("[Stealth] Manual anti-detection patches applied OK")
