import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

DRIVER_PATH = "msedgedriver.exe"

# variable to be finetuned
JOB_DESC_COMMON_WORDS = ["create", "develop", "manage", "participate", "handle", "control", "help", "prepare", "respond", "report"]
WORD_MIN = 10
WORD_MAX = 30

webdriver_service = Service(DRIVER_PATH)

webdriver_options = Options()
webdriver_options.add_argument("--headless")

driver = webdriver.Edge(service=webdriver_service, options=webdriver_options)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":'Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0'})
driver.get("https://jobs.vn.indeed.com/viewjob?jk=9181f15ccc37fe18&tk=1hj7vel0fk3qi801&from=hp&xpse=SoBA67I3GoIMRSg0sD0LbzkdCdPP")
allStrings = driver.find_element(By.XPATH, "/html/body").text.split("\n")

filteredStrings = []

def checkIfStringHasCommonWord(str):
    if str.find("is a") != -1:  # obviously not a description
        return False

    for commonWords in JOB_DESC_COMMON_WORDS:
        if commonWords in str.lower().split():
            return True
    return False


for string in allStrings:
    strLength = len(string.split())
    if WORD_MIN < strLength < WORD_MAX:
        if checkIfStringHasCommonWord(string):
            filteredStrings.append(string)


for string in filteredStrings:
    print(string)


driver.close()