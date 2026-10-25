"""用 Playwright 真實操作 Gradio 版老湯：點湯、問問題、提示、破案、AI 現煮、公布湯底，每個階段截圖。"""
import sys, time, json, os
from playwright.sync_api import sync_playwright

URL, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
log = []

QUESTIONS = {
    "最後一班車": (["站務員是在練習嗎？", "廣播是給人聽的嗎？", "這跟動物有關嗎？"],
                   ["牠平常會睡在軌道上？", "我知道了：有一隻貓習慣睡在軌道上，站務員每天末班車後廣播，是為了把牠嚇到月台上，免得隔天第一班車撞到牠。"]),
    "關燈的理髮師": (["關燈是為了省電嗎？", "關燈是為了那位客人嗎？", "跟客人的健康有關嗎？"],
                     ["日光燈會讓他不舒服？", "我知道了：那位客人有對閃光敏感的疾病，像癲癇，日光燈閃爍會讓他發作，所以理髮師只靠門口不會閃的自然光幫他剪。"]),
}

def bots(page):
    els = page.locator('[data-testid="bot"]')
    return [els.nth(i).inner_text().strip() for i in range(els.count())]

def wait_until(fn, timeout=900, every=0.8):
    t0 = time.time()
    while time.time() - t0 < timeout:
        v = fn()
        if v:
            return v
        time.sleep(every)
    raise TimeoutError("timed out")

def ask(page, text):
    before = len(bots(page))
    box = page.get_by_placeholder("問是非題，例如：這跟錢有關嗎？")
    box.fill(text)
    box.press("Enter")
    reply = wait_until(lambda: (lambda b: b[-1] if len(b) > before and b[-1] else None)(bots(page)))
    time.sleep(1.0)      # 讓計分板更新完
    log.append({"q": text, "a": reply})
    print("  Q:", text, "\n  A:", reply.replace("\n", " ")[:120], flush=True)
    return reply

def click_button(page, name):
    page.get_by_role("button", name=name).click()

def choose(page, value):
    page.locator("label", has_text=value).first.click()

def shot(page, name):
    time.sleep(0.6)
    page.screenshot(path=f"{OUT}/{name}.png", full_page=True)
    print("shot", name, flush=True)

def board_text(page):
    return page.locator("text=湯面").first.inner_text() if page.locator("text=湯面").count() else ""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=1.5)
    page.goto(URL)
    page.wait_for_selector("text=老湯的深夜海龜湯店", timeout=60000)
    shot(page, "app_1_start")

    # 第一局：店內菜單・進階
    choose(page, "進階")
    click_button(page, "點一碗湯 🍲")
    intro = wait_until(lambda: (lambda b: b[-1] if b and "湯面" in b[-1] else None)(bots(page)))
    title = next((t for t in QUESTIONS if t in intro), None)
    print("puzzle:", title, flush=True)
    log.append({"event": "new_game", "intro": intro})
    first, rest = QUESTIONS[title]
    for q in first:
        ask(page, q)
    shot(page, "app_2_midgame")

    before = len(bots(page))
    click_button(page, "給點提示 💡")
    hint = wait_until(lambda: (lambda b: b[-1] if len(b) > before and "提示" in b[-1] else None)(bots(page)))
    log.append({"event": "hint", "a": hint}); print("  hint:", hint, flush=True)
    time.sleep(1.0)
    shot(page, "app_3_hint")

    for q in rest:
        ask(page, q)
    shot(page, "app_4_solved")

    # 第二局：AI 現煮・困難
    choose(page, "困難")
    choose(page, "AI 現煮")
    page.get_by_placeholder("例如：校園、便利商店、捷運").fill("捷運")
    old = bots(page)[-1]
    click_button(page, "點一碗湯 🍲")
    intro2 = wait_until(lambda: (lambda b: b[-1] if b and "湯面" in b[-1] and b[-1] != old else None)(bots(page)))
    log.append({"event": "new_game_ai", "intro": intro2}); print("AI puzzle intro:", intro2[:150], flush=True)
    shot(page, "app_5_ai_puzzle")
    ask(page, "這跟錢有關嗎？")
    before = len(bots(page))
    click_button(page, "我放棄，公布湯底 🫠")
    rev = wait_until(lambda: (lambda b: b[-1] if len(b) > before and "湯底" in b[-1] else None)(bots(page)))
    log.append({"event": "reveal", "a": rev}); print("  reveal:", rev[:150], flush=True)
    time.sleep(1.0)
    shot(page, "app_6_reveal")
    browser.close()

json.dump(log, open(f"{OUT}/app_log.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("done")
