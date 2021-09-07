
hardworker = '?'
api = "?"

PUBLIC_GROUP = 'public group'
CLOSED_GROUP = 'closed group'

def listAllMyGroups():
    # the is the deprecated way. It only scraps first 25 groups
    '''
    import time
    from facepy import GraphAPI
    graph = GraphAPI(hardworker)
    groups = graph.get('me/groups')
    return groups['data']
    '''

    # new way
    from bs4 import BeautifulSoup as bs
    f = open('remove_list.html')
    data = bs(f.read(), 'html.parser')

    aTags = data.find_all('a')
    allSpans = data.find_all('span')

    allLinks = list()


    for i in aTags:
        linkData = dict()
        temp = i.get('href')
        temp = temp.replace('/groups/', '')
        temp = temp.replace('/?ref=group_browse', '')
        linkData['id'] = temp
        allLinks.append(linkData)
    counter = 0
    for i in allSpans:
        groupName = i.string
        if(groupName != None):
            theLink = allLinks[counter]
            theLink['name'] = groupName.strip()
            counter += 1
    return allLinks

def saveGroupsToFile(groupData):
    f = open('groups.txt', 'w', encoding='utf-8')
    for g in groupData:
        f.write(str(g))
        f.write("\n")

    f.close()

def getGroupStatistics(group):
    from bs4 import BeautifulSoup as bs
    from urllib.request import Request
    from urllib.request import urlopen
 
    headers = {'User-Agent': 'Chrome 74.0'}

    url = 'https://en-gb.facebook.com/groups/%s' % (group)
    request = Request(url, headers=headers)
    site = urlopen(request)
    site = bs(site.read(), 'html.parser')

    # find the tag with this class, it is a div
    status_div = site.find(class_='_19s_')
    if(status_div == None):
        print('Unable to find group status. You might need to login.')
        return 0
    # find the span tag inside previously found div and extract text from that span
    status = status_div.find('span').text
    if(status.lower() == PUBLIC_GROUP):
        # open all meta tags in head
        for i in site.find_all('meta'):
            # check the content attribute of all meta tags
            string = i.get('content')
            # if it contains a phrase like 'X' members
            if(string != None and 'has' in string and 'member' in string):
                # extract the number of members
                index1 = string.find('has')
                index2 = string.find('member')
                members = string[index1+3:index2]
                members = members.strip()
                members = members.replace(',','')
                try:
                    members = int(members)
                except:
                    return 0
                return members
                break
                  
    else:
        
        code = str()
        # find all 'code' tags
        codes = site.find_all('code')
        for c in codes:
            temp = c.string
            temp = str(temp)
            temp = temp.strip()
            # if the comment in this code tag startswith this line then this code contains our data
            if(temp.startswith('<div class="_4-u2 _3-96 _4-u8">')):
                code = temp
                break    

        # convert code to html
        site = bs(code, 'html.parser')
        # extract the desired data
        stats = site.find_all(class_='_63om _6qq6')

        posts_today = '0'
        total_members = '0'
        if(len(stats) == 2):
            posts_today = stats[0].text
            total_members = stats[1].text
        # if there were no posts today then
        else:
            total_members = stats[0].text
            
        total_members = total_members.replace(',','')
        stats = site.find_all(class_='_63op _6qqa')
        recent_posts = stats[0].text
        recent_members = stats[1].text
        total_members = int(total_members)
        print("Recent Members: ",recent_members)
        print("Posts Today: ",posts_today)
        print("Recent Posts: ",recent_posts)
        return total_members

    
def sortGroups(groups):
    total = len(groups)
    for i in range(total-1):
        index = i + 1
        for j in range(index, total):
            a = groups[j].get('members', 0)
            b = groups[index].get('members', 0)
            if(a > b) :
                index = j
        temp = groups[i]
        groups[i] = groups[index]
        groups[index] = temp

    
#if __name__=="__main__":
myGroups = listAllMyGroups()
print('Total Groups in File: %s' % len(myGroups))
groupsFile = open('groups.txt','a+', encoding='utf-8')
oldGroups = groupsFile.readlines()
oldGroups = [eval(g) for g in oldGroups]
oldIds = [g['id'] for g in oldGroups]
count = 0
for g in myGroups:
    if(g['id'] not in oldIds):
        print('Group : %s' % (g['name']))
        g['members'] = getGroupStatistics(g['id'])
        print('Total Members: %d' %(g['members']))
        print('*' * 10)
        oldGroups.append(g)
        count += 1

sortGroups(oldGroups)
saveGroupsToFile(oldGroups)

