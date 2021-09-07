keys = input('Enter group keywords :')
group_keys = keys.split(' ')
group_keys = [k.strip() for k in group_keys]
groups = list()
groupsFile = open('groups.txt', encoding='utf-8')
for g in groupsFile:
    group = eval(g)
    keyPresent = True
    upto = len(group_keys)
    counter = 0
    while(counter < upto and keyPresent != False):
        if(group_keys[counter].lower() not in group['name'].lower()):
            keyPresent = False
        counter += 1
    if(keyPresent):
        groups.append(group)
        print(group)
groupsFile.close()
groupsFile = open('%s.txt' % (keys), 'w', encoding='utf-8')
for i in groups:
    groupsFile.write(str(i))
    groupsFile.write("\n")
groupsFile.close()



