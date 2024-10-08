from selenium_driverless import webdriver
import asyncio
import pyautogui

screenshot_path = '123.png'  # Укажите путь к вашему скриншоту

async def click_element_on_screen(screenshot_path):
    try:
        location = pyautogui.locateOnScreen(screenshot_path, confidence=0.8)  # Поиск на основе скриншота
        if location:
            center = pyautogui.center(location)
            pyautogui.click(center)
            return True  # Успешный клик, выход из функции
    except pyautogui.ImageNotFoundException:
        pass
    return False

async def get_title(driver):
    try:
        return await driver.execute_script("return document.title")
    except Exception as e:
        return None

async def get_cf_clearance_cookie(driver):
    cookies = await driver.get_cookies()
    for cookie in cookies:
        if cookie['name'] == 'cf_clearance':
            return cookie['value']
    return None

async def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en")  # Предпочтительный язык английский
    async with webdriver.Chrome(options=options) as driver:
        await driver.get('https://nopecha.com/demo/cloudflare', wait_load=True)
        await asyncio.sleep(10)  # Ждем 10 секунд для загрузки страницы

        while True:
            title = await get_title(driver)
            if title is None:
                await asyncio.sleep(1)
                continue
            
            print(f"Title: {title}")

            if "Just a moment" in title:
                if await click_element_on_screen(screenshot_path):
                    print("Элемент найден и клик выполнен")
                else:
                    print("Элемент не найден, повторная попытка")
                await asyncio.sleep(1)  # Подождать перед повторной попыткой
            else:
                # Получаем cookie cf_clearance
                cf_clearance = await get_cf_clearance_cookie(driver)
                print(f"Title: {title}")
                print(f"cf_clearance: {cf_clearance}")
                
                # Закрываем браузер
                await driver.quit()
                break

asyncio.run(main())
