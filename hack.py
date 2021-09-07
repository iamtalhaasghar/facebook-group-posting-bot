from bs4 import BeautifulSoup as bs
from urllib.request import Request
from urllib.request import urlopen
PUBLIC_GROUP = 'Public Group'
headers = {'User-Agent': 'Chrome 74.0'}
counter = 0
g = {'id':'1991145924444488', 'name':'test'}
url = 'https://en-gb.facebook.com/groups/%s' % (g['id'])
print('Group # %d: %s, id: %s' %(counter, g['name'], g['id']))
request = Request(url, headers=headers)
site = urlopen(request)
site = bs(site.read(), 'html.parser')

# find the tag with this class, it is a div
status_div = site.find(class_='_19s_')
if(status_div == None):
    print('Unable to find group status. You might need to login.')
    exit()
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
            g['members'] = int(members)
            print(members)
            print('*' * 10)
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
    g['members'] = int(total_members)
    print("Total Members: ",total_members)
    print("Recent Members: ",recent_members)
    print("Posts Today: ",posts_today)
    print("Recent Posts: ",recent_posts)
    print('*' * 10)
