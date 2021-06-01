from framework import APIFramework
from pageObjects import API as pages
import pageObjects
import framework
import time
# pages.common.login()
# pages.reports.readReports()

web = framework.WebFramework()
web.startChrome()
web.driver.get("https://qa-sandbox.apps.htec.rs/")
web.Find("a:contains('Login')").click()
po = pageObjects.Web(web)
print(po)
po.common.login()
time.sleep(5)

web.driver.quit()