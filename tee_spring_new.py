from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time,os, random

FB_URL = "https://web.facebook.com"


def logout(driver):
    "This method is used to logout from current logged in facebook account."
    
    try:
        logoutButton = driver.find_element_by_id("mbasic_logout_button")
        logoutButton.click()
    except Exception as e:
        pass
    
    try:
        dontSave = driver.find_element_by_xpath('''//input[@value="Don't Save and Log Out"]''')
        dontSave.click()
    except Exception as e:
        pass    
    
    
    try:
        gearIcon = driver.find_element_by_xpath("//img[@alt='gear']")
        gearIcon.click() 
    except Exception as e:
        pass
    
    
    try:
        removeInfo = driver.find_element_by_xpath('''//input[@value="Remove saved login information"]''')
        removeInfo.click()    
    except Exception as e:
        pass
    

def login(driver, u_name, u_pass):
    "This method takes in the user credentials and logins to that facebook account"
    username = driver.find_element_by_id('email')
    password = driver.find_element_by_id('pass')
    loginButton = driver.find_element_by_id('loginbutton')
    username.send_keys(u_name)
    password.send_keys(u_pass)
    loginButton.click()
   
def searchGroups(driver, keyword):
    query = driver.find_element_by_name("query")
    query.send_keys(keyword)
    search = driver.find_element_by_xpath("//input[@value='Search' and @type='submit']")
    search.click()
    more = driver.find_element_by_link_text("More")
    more.click()
    groups = driver.find_element_by_link_text("Groups")
    groups.click()
    shouldLoop = True
    groupsDict = dict()
    while(shouldLoop):
        try:
            driver.find_element_by_xpath("//span[contains(text(),'End of Results')]")
            shouldLoop = False
        except NoSuchElementException:
            groups_list = driver.find_element_by_id("BrowseResultsContainer")
            code = groups_list.get_attribute("innerHTML")
            soup = BS(code, 'lxml')
            img_with_alt = lambda tag: tag.has_attr("alt")
            img_tags = soup.find_all(img_with_alt)
            for img in img_tags:
                # <a href="/groups/111111111/?..."><img></img></a>
                href = img.parent.get("href") 
                href = href.split("?")[0]
                href = href.replace("/groups/","")
                groupItem = {'name':img.get("alt")}
                groupsDict[href] = groupItem
            see_more = driver.find_element_by_xpath("//div[@id='see_more_pager']/child::a")
            see_more.click()
    return groupsDict


def fetchGropusInfo(driver, groupsDict):
    url = "%s/groups" % (FB_URL)
    for gropuId in groupsDict:
        driver.get('%s/%s' % (url, gropuId))
        groupType = driver.find_element_by_xpath("//div[contains(text(),'group')]")
        membersCount = driver.find_element_by_xpath("//a[contains(text(),'Members')]/ancestor::td/following-sibling::td/span")
        group = groupsDict[gropuId]
        group['type'] = groupType.text.strip()
        group['members'] = membersCount.text.strip()


def main():
    u_name = '?'
    u_pass = '?'
    opts = webdriver.ChromeOptions()
    opts.binary_location = r"C:\chrome 74.0\Chrome-bin\chrome.exe"
    driver = webdriver.Chrome()
    driver.get(FB_URL + '/login')
    
    try:
        login(driver, u_name, u_pass)
        time.sleep(3)
        
        groupsDict = searchGroups(driver, "cricket")
        groupsDict = {'1485868211654446':{'name':'MS DHONI FANS'}, '545156472637462':{'name':'Troll World Cricket'}}
        fetchGropusInfo(driver, groupsDict)
        for i in groupsDict:
            print(i, groupsDict[i])
        
    except Exception as ex:
        print(ex)
    finally:
        pass
        #logout(driver)
    #driver.quit()
    

main()
input('Press any key to continue...')
