import json
import urllib
import subprocess
from playwright.sync_api import sync_playwright

# Define capabilities for the first browser/OS combination (Windows 10, Chrome latest version)
capabilities_windows10_chrome_latest = {
    'browserName': 'Chrome',
    'browserVersion': 'latest',
    'LT:Options': {
        'platform': 'Windows 10',
        'build': 'Playwright Python Build-1',
        'name': 'Test Scenario-2 (Windows 10 Chrome-Latest)',
        'user': 'nainishk05',
        'accessKey': '7cvBWS7EO37gEW9xYmvgpQZA7z8VTGQybQP2hU6sUOg1tniDTE',
        'network': True,
        'video': True,
        'headless': False,
        'console': True,
        'tunnel': False,
        'tunnelName': '',
        'geoLocation': '',
    }
}

# Define capabilities for the second browser/OS combination (Windows 11, Chrome 120 version)
capabilities_windows11_chrome_l20 = {
    'browserName': 'Chrome',
    'browserVersion': 'latest',
    'LT:Options': {
        'platform': 'Windows 11',
        'build': 'Playwright Python Build-1',
        'name': 'Test Scenario-2 (Windows 11 Chrome-120)',
        'user': 'nainishk05',
        'accessKey': '7cvBWS7EO37gEW9xYmvgpQZA7z8VTGQybQP2hU6sUOg1tniDTE',
        'network': True,
        'video': True,
        'headless': False,
        'console': True,
        'tunnel': False,
        'tunnelName': '',
        'geoLocation': '',
    }
}


def run_test(capabilities):
    with sync_playwright() as playwright:
        playwrightVersion = str(subprocess.getoutput('playwright --version')).strip().split(" ")[1]
        capabilities['LT:Options']['playwrightClientVersion'] = playwrightVersion
        lt_cdp_url = 'wss://cdp.lambdatest.com/playwright?capabilities=' + urllib.parse.quote(json.dumps(capabilities))
        browser = playwright.chromium.connect(lt_cdp_url, timeout=120000)
        page = browser.new_page()
        try:
            page.goto("https://www.lambdatest.com/selenium-playground")
            page.click("//a[normalize-space()='Drag & Drop Sliders']")
            page.wait_for_timeout(5000)
            page.focus("//input[@value='15']")
            for _ in range(5):
                page.keyboard.press('ArrowRight')
            steps = 75
            for _ in range(steps):
                page.keyboard.press('ArrowRight')
            page.wait_for_timeout(5000)
            if page.inner_text("//output[@id='rangeSuccess']") == "95":
                set_test_status(page, "passed", "value 95 match")
            else:
                set_test_status(page, "failed", "not match")
        except Exception as err:
            print("Error:: ", err)
            set_test_status(page, "failed", str(err))
        browser.close()


def set_test_status(page, status, remark):
    page.evaluate("_ => {}",
                  "lambdatest_action: {\"action\": \"setTestStatus\", \"arguments\": {\"status\":\"" + status + "\", \"remark\": \"" + remark + "\"}}");


if __name__ == "__main__":
    run_test(capabilities_windows10_chrome_latest)
    run_test(capabilities_windows11_chrome_l20)
















































# import json
# import urllib
# import subprocess
# import asyncio
# from playwright.async_api import async_playwright
#
# capabilities = {
#     'browserName': 'Chrome',
#     'browserVersion': 'latest',
#     'LT:Options': {
#         'platform': 'Windows 10',
#         'build': 'Playwright Python Build-1',
#         'name': 'Test Scenario-2',
#         'user': 'nainishk05',
#         'accessKey': '7cvBWS7EO37gEW9xYmvgpQZA7z8VTGQybQP2hU6sUOg1tniDTE',
#         'network': True,
#         'video': True,
#         'headless': False,
#         'console': True,
#         'tunnel': False,
#         'tunnelName': '',
#         'geoLocation': '',
#     }
# }
#
# async def main():
#     playwrightVersion = str(subprocess.getoutput('playwright --version')).strip().split(" ")[1]
#     capabilities['LT:Options']['playwrightClientVersion'] = playwrightVersion
#
#     lt_cdp_url = 'wss://cdp.lambdatest.com/playwright?capabilities=' + urllib.parse.quote(
#         json.dumps(capabilities))
#
#     async with async_playwright() as playwright:
#         browser = await playwright.chromium.connect(lt_cdp_url, timeout=120000)
#         page = await browser.new_page()
#         try:
#             await page.goto("https://www.lambdatest.com/selenium-playground")
#
#             # Click "Drag & Drop Sliders" under "Progress Bars & Sliders".
#             await page.click("//a[normalize-space()='Drag & Drop Sliders']")
#             await page.wait_for_timeout(5000)
#
#
#             await page.focus("//input[@value='15']")
#             for _ in range(5):  # TODO: adjust the number of iterations to make sure the action is complete
#                 await page.keyboard.press('ArrowRight')
#
#
#             steps = 75
#             for _ in range(steps):
#                 await page.keyboard.press('ArrowRight')
#
#             await page.wait_for_timeout(5000)
#             # Validate whether the range value shows '95'
#
#             if await page.inner_text("//output[@id='rangeSuccess']") == "95":
#                 await set_test_status(page, "passed", "value 95 match")
#             else:
#                 await set_test_status(page, "failed", "not match")
#
#         finally:
#             await browser.close()
#
# async def set_test_status(page, status, remark):
#     await page.evaluate("_ => {}",
#                         "lambdatest_action: {\"action\": \"setTestStatus\", \"arguments\": {\"status\":\"" + status + "\", \"remark\": \"" + remark + "\"}}");
#
#
# asyncio.run(main())
