import framework

apiDriver = framework.APIFramework()
webDriver = framework.WebFramework()

baseURL = "https://qa-sandbox.apps.htec.rs/"

class API:
    class common:
        def login(user="miro@shizikot.net", password="Changeme1"):
            raw = apiDriver.postRequest("https://qa-sandbox.apps.htec.rs/api/users/login", {"email":user, "password":password })
            print(raw)
            apiDriver.setAuthorization(raw["token"])
    
    class reports:
        def readReports():
            raw = apiDriver.getRequest("https://qa-sandbox.apps.htec.rs/api/reports/all")
            print(raw)

class Web:
    def __init__(self, web):
        self.webDriver = web
        self.common = self.common(web)
        print(self.webDriver)

    class common:
        def __init__(self, web):
            self.webDriver = web

        def login(self, user="miro@shizikot.net", password="Changeme1"):
            if(self.webDriver.Find("a:contains('Logout')").exists()):
                print("Already logged in.")
                return
            if self.webDriver.getUrl().endswith("login"):
                print("Logging in...")
                self.webDriver.Find("a:contains('Login')").click()
                self.webDriver.Find("input[type=email]").waitExists().sendKeys(user)
                self.webDriver.Find(":password").waitExists().sendKeys(password)
                self.webDriver.Find(":contains('Submit'):last").waitExists().click()

