import requests
from selenium import webdriver
import selenium
import json
import time
import os

class APIFramework:
    def __init__(self):
        self.token = None

    def setAuthorization(self, token):
        self.token = token

    def getRequest(self, url):
        result = None
        if self.token is None:
            result = requests.get(url=url)
        else:
            result = requests.get(url=url, headers={"Authorization":f"Bearer {self.token}"})
        return result.content
        
    def postRequest(self, url, data, type="application/json"):
        result = None
        if self.token is None:
            result = requests.post(url=url, json=data)
        else:
            result = requests.post(url=url, headers={"Authorization":f'Bearer {self.token}', "Content-Type":type}, json=data)

        if result.text.startswith("{"):
            print("json response")
            return json.loads(result.text)

        print("raw response")
        return str(result.content)

# An interface between the WebDriver and WebElements, keeping the way to the WebElement, but not its instance
# This approach allows for "refreshing" of the WebElement each time it is queried
# Builder pattern is used to allow for fluid (one-liner) element querying and manipulation
class Selector:
    def __init__(self, web, path):
        self.web = web
        self.path = path

    def get(self):
        self.web.injectJQuery()
        res = self.web.driver.execute_script(f"return [miro(\"{self.path}\")[0],miro(\"{self.path}\")[0].outerHTML]")
        # selenium.webdriver.remote.webelement.WebElement(parent, id_)
        print(f"Got '{res[1]}'")
        return res[0]

    def click(self):
        self.get().click()
        return self

    def exists(self):
        try:
            if self.get() is not None:
                return True
            else:
                return False
        except:
            return False

    def waitExists(self, timeout=10, interval=0.333):
        start = time.time()
        while(not self.exists()):
            time.sleep(interval)
            if(time.time() - start >= timeout):
                return None
        return self

    def sendKeys(self, text):
        self.get().send_keys(text)
        return self

# main framework class
class WebFramework:
    def __init__(self):
        self.driver = None

    def getUrl(self):
        return self.driver.current_url


    def startChrome(self):
        print("starting chrome")
        print(os.getcwd())
        path = [f for f in os.listdir(f"{os.getcwd()}\\practice\\src") if f.endswith('.exe')][0]
        print(path)
        # print(os.listdir(f"{os.getcwd()}\\practice\\src\\"))
        if os.name == 'posix':
            self.driver = webdriver.Chrome("./chromedriver")
        else:
            self.driver = webdriver.Chrome(f"{os.getcwd()}\\practice\\src\\{path}")
            # print("aman")
        
    
    # injects jQuery in separate global variable without interfering with existing jQuery version
    # different frameworks using the $ like Angular or React would retain their version of jQuery
    def injectJQuery(self):
        res = 0
        res = self.driver.execute_script('''
            if (document.getElementById("injectQuery") != null) { return 1;}
            var script = document.createElement("script");
            script.id = "injectQuery";
            script.setAttribute("src", "https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js");
            document.body.appendChild(script);
            return 0;
        ''')
        if res == 0:
            print("injected jQuery")
            time.sleep(0.5)
            self.driver.execute_script('window.miro = jQuery;')
            self.driver.execute_script("window.miro.noConflict(true);")
        else:
            print("skipped injection")

    def Find(self, path):
        elem = Selector(self, path)
        return elem
