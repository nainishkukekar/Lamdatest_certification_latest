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
        'name': 'Test Scenario-3 (Windows 10 Chrome-Latest)',
        'user': 'nainishkukekar',
        'accessKey': 'bNutSgMdjh2YsQnTW4KuJ65SqG7H1OFReBWlpGnLiUInUzF0Vr',
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
        'name': 'Test Scenario-3 (Windows 11 Chrome-120)',
        'user': 'nainishkukekar',
        'accessKey': 'bNutSgMdjh2YsQnTW4KuJ65SqG7H1OFReBWlpGnLiUInUzF0Vr',
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
            page.click("//a[normalize-space()='Input Form Submit']")
            page.wait_for_timeout(1000)
            page.fill("#name", "John Doe")
            page.fill("#inputEmail4", "john.doe@example.com")
            page.fill("#inputPassword4", "1234567890")
            page.fill("#company", "123 Main St")
            page.fill("#websitename", "New York")
            page.fill("#inputCity", "New York")
            page.fill("#inputAddress1", "123 Main St")
            page.fill("#inputAddress2", "Apt 101")
            page.fill("#inputState", "New York")
            page.fill("#inputZip", "10001")
            page.select_option('select[name="country"]', label="United States")
            print("Form filled successfully.")
            page.click("//button[normalize-space()='Submit']")
            page.wait_for_timeout(5000)
            paragraph_element = page.query_selector('p.success-msg')
            inner_text = paragraph_element.text_content()
            expected_text = "Thanks for contacting us, we will get back to you shortly."
            if inner_text.strip() == expected_text:
                set_test_status(page, "passed", "Success messsage validation passed ")
            else:
                set_test_status(page, "failed", "Success messsage validation Failed")
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
