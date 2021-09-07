

def listAllMyFriends():

    from bs4 import BeautifulSoup as bs
    f = open('friends_list.html', encoding='utf-8')
    data = bs(f.read(), 'html.parser')
    f.close()
    aTags = data.find_all('a')
    allLinks = list()

    friendsData = list()
    for i in aTags:
        href = i.get('href')
        if('profile_friend_list' in href):
            href = href.split('&')[0]
            href = href.replace('?fref=profile_friend_list','')
            href = href.replace('profile.php?id=','')
            href = href.split('/')[-1]
            if(href not in allLinks):
                allLinks.append(href)
                friend = dict()
                friend['id'] = href
                friend['name'] = i.img.get('aria-label')
                friendsData.append(friend)
    return friendsData

def saveFriendsToFile(data):
    f = open('friends.txt', 'w', encoding='utf-8')
    for g in data:
        f.write(str(g))
        f.write("\n")

    f.close()

    
#if __name__=="__main__":
myFriends = listAllMyFriends()
saveFriendsToFile(myFriends)
