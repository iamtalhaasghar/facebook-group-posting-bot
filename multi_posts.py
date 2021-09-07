from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import time,os, random

FB_URL = "https://free.facebook.com/"

def readGroupsData():
    groups = list()
    groupsFile = 'groups'#input('Enter the name of target groups file (without .txt): ')
    groupsFile = open('%s.txt' % (groupsFile), encoding='utf-8')
    groupsFile.read()
    for g in groupsFile:
        g = g.strip()
        groups.append(eval(g))
    groupsFile.close() 
    return groups

def readFriendsData():
    groups = list()
    groupsFile = 'f'#input('Enter the name of target groups file (without .txt): ')
    groupsFile = open('%s.txt' % (groupsFile), encoding='utf-8')
    groupsFile.seek(0)
    for g in groupsFile:
        try:
            groups.append(eval(g))
        except:
            print(g)
        
    groupsFile.close() 
    return groups

def readPost(fileName):
    postFile = open(fileName)
    postText = postFile.read()
    postFile.close()
    return postText

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
    username = driver.find_element_by_name('email')
    password = driver.find_element_by_name('pass')
    loginButton = driver.find_element_by_name('login')
    username.send_keys(u_name)
    password.send_keys(u_pass)
    loginButton.click()
    time.sleep(5)
    not_now = driver.find_element_by_link_text('Not Now')
    if(not_now != None):
        not_now.click()
        time.sleep(5)
    
    

def startPostingInGroups(driver):
    groups = readGroupsData()
    msg = readPost("post.txt")
    postsCount = 0
    index = 0
    groupCount = len(groups)
    isPostAllowed = True
    while(isPostAllowed):
        grp = groups[index]
        index = (index + 1) % groupCount
        g = "%s/groups/%s" %(FB_URL, grp['id'])
        print("Post # %s || %s" %(postsCount+1, grp['name']))
        driver.get(g)
        time.sleep(3)
        try:
            post_form = driver.find_element_by_name('xc_message')
            post_form.send_keys(msg)
            post_btn = driver.find_element_by_name('view_post')
            time.sleep(3)
            post_btn.click()
            time.sleep(5)
            try:
                driver.find_element_by_xpath('''//div[@title="You can't use this feature at the moment"]''')
                isPostAllowed = False
                time.sleep(3)
                print("Group Posting Feature Disabled after %d posts" % (postsCount))
            except NoSuchElementException as ex:
                pass
            
            if(isPostAllowed):
                try:
                    driver.find_element_by_xpath('''//div[@title="Action Blocked"]''')
                    isPostAllowed = False
                    time.sleep(3)
                    print("Action Blocked after %d posts" % (postsCount))
                except NoSuchElementException as ex:
                    pass
            
            if(isPostAllowed):
                postsCount += 1

        except Exception as ex:
            print(ex)

    
def startCommenting(driver):
    groups = readGroupsData()
    msg = readPost("comment.txt")
    random.shuffle(groups)
    count = 1
    for g in groups:
        groupLink = "%s/groups/%s" %(FB_URL, g['id'])
        driver.get(groupLink)
        time.sleep(3)
        mainPage = driver.current_url

        commentTags = driver.find_elements_by_partial_link_text('Comment')
        commentLinks = list()
        for c in commentTags:
            href = c.get_attribute('href')
            commentLinks.append(href)

        for link in commentLinks:
            print("Comment # %d: %s"%(count, link))
            time.sleep(3)
            driver.get(link)
            time.sleep(3)
            commentText = driver.find_element_by_name("comment_text")
            commentText.send_keys(msg)
            commentButton = driver.find_element_by_css_selector('input[value="Comment"][type="submit"]')
            commentButton.click()
            count+= 1
        '''
        time.sleep(3)
        driver.get(mainPage)
        time.sleep(5)
        morePosts = driver.find_element_by_link_text('See more posts')
        morePostsLink = morePosts.get_attribute('href')
        time.sleep(3)
        driver.get(morePostsLink)
        time.sleep(5)
        '''

def leaveGroups(driver):
    groups = readGroupsData()
    for grp in groups:
        g = "%s/groups/%s" %(FB_URL, grp['id'])
        driver.get(g)
        time.sleep(3)
        try:
            group_info = driver.find_element_by_xpath("//a[text()='Info']")
            group_info.click()
            leave_group = driver.find_element_by_xpath("//a[text()='Leave Group']")
            leave_group.click()
            confirm_leave = driver.find_element_by_xpath("//input[@value='Leave Group']")
            confirm_leave.click()
        except Exception as ex:
            print(ex)

def unfriendAllFriends(driver):
    
    friends = readFriendsData()
    counter = len(friends)
    for f in friends:
        link = "%s/%s" %(FB_URL, f['id'])
        driver.get(link)
        time.sleep(3)
        try:
            more_option = driver.find_element_by_xpath("//a[text()='More']")
            more_option.click()
            unfriend = driver.find_element_by_xpath("//a[text()='Unfriend']")
            unfriend.click()
            confirm_btn = driver.find_element_by_xpath("//input[@value='Confirm']")
            confirm_btn.click()
            print("Done: ",f['name'])
        except Exception as ex:
            print(ex)
        counter -=1
        print("Left: ",counter)
def main():
    
    u_name = '?'
    u_pass = '?'


    opts = webdriver.ChromeOptions()
    brave_location = r"C:\Program Files\Brave Browser\BraveSoftware\Brave-Browser\Application\brave.exe"
    opts.binary_location = r"C:\chrome 74.0\Chrome-bin\chrome.exe"
    opts.binary_location = brave_location
    driver = webdriver.Chrome(options = opts)
    driver.get(FB_URL)
    try:
        login(driver, u_name,u_pass)
    except Exception as ex:
        print(ex)
    finally:
        logout(driver)
    

main()
input('Press any key to continue...')
