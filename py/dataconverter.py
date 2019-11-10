from pandas import DataFrame
from json import loads

def getCSV(input):
    obj = loads(input)
    dicter = listloop(obj, {}, '')
    df = DataFrame(data=dicter)
    #print(df)
    df.to_csv('exporter' + '.csv')

def getFrame(input, allowbracks):
    obj = loads(input)
    dicter = mainloop(obj, {}, '', allowbracks)
    removelist = []
    df = DataFrame(data=dicter)
    return df

def mainloop(input, dicter, recent, allowbracks):
    #iterate through each item in the outer list of dictionaries
    iterboi = 1

    for item in input:
        #print('new iter')
        if type(item) is dict:
            dictloop(item, dicter, recent, allowbracks)
        if type(item) is list:
            print('DODODODODODODODODODODODODODODODODODODODODODODODODasdfasdfasdfasdfasdffasd')

        for key, val in dicter.items():
            #print('iterboi is ' + str(iterboyo) + ' and the len of this val is ' + str(len(val)) + ', the key is ' + key)
            if (len(val) < iterboi):
                #print('motion')
                addon = []
                minidif = iterboi - len(val)
                if minidif == 1:
                    dicter.get(key).append('')
                else:
                    while (len(addon) < minidif):
                        #print('addon len is ' + str(len(addon)) + ', and iterboi is ' + str(iterboyo))
                        addon.append('')
                    #print(returndict.get(key))
                    dicter[key] = addon + dicter.get(key)
                    #print(returndict.get(key))
                # print(len(dicter.get(key)))

        iterboi+=1

    return dicter
    #print(dicter)

def dictloop(input, dicter, recent, allowbracks):
    #print('entering dictloop with  recent of ' + recent + ' and an input of ' + str(input))
    for key, val in input.items():
        #print('key is ' + key + ' and the val is ' + str(val))
        if not type(val) is dict and not type(val) is list:
            #print(recent)
            if not recent == '':
                newcent = recent + '-' + key
            else:
                newcent = key
            #newcent = recent+'-'+key
            if newcent not in dicter:
                temp = []
                temp.append(val)
                #print('creating a new entry for ' + newcent)
                dicter[newcent] = temp
            else:
                #print('appending ' + str(val) + ' to the key ' + str(key))
                dicter.get(newcent).append(val)
            continue
        if type(val) is dict:
            #print('prepare for recursion')
            if len(recent) > 1:
                stringtemp = recent + '-' + key
                #print('going though dictloop with new recent ' + stringtemp)
                dictloop(val, dicter, stringtemp, allowbracks)
                continue
            else:
                dictloop(val, dicter, key, allowbracks)
                continue
        if type(val) is list and allowbracks:
            print('LETS GET IT WE MADE IT KIND OF BUT ITS A START')
            recent = recent + ' list'
            listloop(val, dicter, recent, allowbracks)


def listloop(input, dicter, recent, allowbracks):
    #print('entering listloop oh my')
    iterguy = 1
    for goober in input:
        #print(goober)
        if type(goober) is list:
            #print('heyo')
            listloop(goober, dicter, recent, allowbracks)
        if type(goober) is dict:
            #print('prepare for recursion in the list oh moses help me')
            if len(recent) > 1:
                stringtemp = recent + str(iterguy)
                #print(stringtemp)
                #print('going though dictloop with new recent ' + stringtemp)
                dictloop(goober, dicter, stringtemp, allowbracks)
                iterguy += 1
                continue
            else:
                #print('yooooo')
                stringtemp = recent + str(iterguy)
                dictloop(goober, dicter, stringtemp, allowbracks)
                iterguy += 1
                continue

def invedit(input, search):
    obj = loads(input)

    returndict = {}
    returndict['labname'] = []
    returndict['labid'] = []
    returndict['username'] = []
    returndict['created'] = []
    returndict['count'] = []
    returndict['reordernum'] = []

    iterboyo = 1

    for item in obj:
        returndict.get('created').append(item.get('created'))
        returndict.get('labname').append(item.get('inventoryLocation').get('location').get('shortName'))
        returndict.get('labid').append(item.get('inventoryLocation').get('location').get('id'))
        returndict.get('username').append(item.get('user').get('username'))
        listthing = item.get('reportItems')
        for goober in listthing:
            #print(goober.get('item').get('name') + ', with a quan of ' + str(goober.get('quantity')))
            if (goober.get('item').get('name') == search):
                #print('appending quantity of ' + str(goober.get('quantity')))
                returndict.get('count').append(goober.get('quantity'))
                break
        listthingtwo = item.get('inventoryLocation').get('locationItems')
        for goobertwo in listthingtwo:
            if (goobertwo.get('item').get('name') == search):
                #print('hit')
                returndict.get('reordernum').append(goobertwo.get('reorderAmount'))
                break


        for key, val in returndict.items():
            #print('iterboi is ' + str(iterboyo) + ' and the len of this val is ' + str(len(val)) + ', the key is ' + key)
            if (len(val) < iterboyo):
                #print('motion')
                addon = []
                minidif = iterboyo - len(val)
                if minidif == 1:
                    returndict.get(key).append('')
                else:
                    while(len(addon) < minidif):
                        #print('addon len is ' + str(len(addon)) + ', and iterboi is ' + str(iterboyo))
                        addon.append('')
                    #print(returndict.get(key))
                    returndict[key] = addon + returndict.get(key)
                    #print(returndict.get(key))
                #print(len(dicter.get(key)))

        iterboyo+=1

    df = DataFrame(data=returndict)
    return df

def formpull(input):
    print('alex is a dunsparce')

    obj = loads(input)

    #remove the outer shell for "answer"
    innerpart = obj.get('answers')

    dicter = mainloop(innerpart, {}, '')

    df = DataFrame(data=dicter)
    return df

def formkeypull(input):
    print('doing a key thing')
    obj = loads(input)
    #for dict in the list, pull out items, from
    for formdict in obj:
        #take out the item thing
        itemlist = formdict.get("items")
        print(itemlist)
        print('jenna is cool')