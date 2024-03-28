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
        'name': 'Test Scenario-1 (Windows 10 Chrome-Latest)',
        'user': 'nainishk05',
        'accessKey':'7cvBWS7EO37gEW9xYmvgpQZA7z8VTGQybQP2hU6sUOg1tniDTE',
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
        'name': 'Test Scenario-1 (Windows 11 Chrome-120)',
        'user': 'nainishk05',
        'accessKey':'7cvBWS7EO37gEW9xYmvgpQZA7z8VTGQybQP2hU6sUOg1tniDTE',
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
            page.click("//a[normalize-space()='Simple Form Demo']")
            page.wait_for_timeout(1000)
            title = page.title()
            print("Title:: ", title)
            if "Selenium" in title:
                set_test_status(page, "passed", "Title matched")
            else:
                set_test_status(page, "failed", "Title did not match")
            welcome_message = "Welcome to LambdaTest"
            page.fill("//input[@id='user-message']", welcome_message)
            page.click("//*[@id='showInput']")
            assert page.text_content("//p[@id='message']") == welcome_message
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
