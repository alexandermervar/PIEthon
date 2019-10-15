import pandas as pd
import json

def getCSV(input):
    obj = json.loads(input)
    dicter = listloop(obj, {}, '')
    df = pd.DataFrame(data=dicter)
    #print(df)
    df.to_csv('exporter' + '.csv')

def getFrame(input, allowbracks):
    obj = json.loads(input)
    dicter = mainloop(obj, {}, '', allowbracks)
    removelist = []
    df = pd.DataFrame(data=dicter)
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
    obj = json.loads(input)

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
            print(goober.get('item').get('name') + ', with a quan of ' + str(goober.get('quantity')))
            if (goober.get('item').get('name') == search):
                print('appending quantity of ' + str(goober.get('quantity')))
                returndict.get('count').append(goober.get('quantity'))
        listthingtwo = item.get('inventoryLocation').get('locationItems')
        for goobertwo in listthingtwo:
            if (goobertwo.get('item').get('name') == search):
                #print('hit')
                returndict.get('reordernum').append(goobertwo.get('reorderAmount'))


        for key, val in returndict.items():
            print('iterboi is ' + str(iterboyo) + ' and the len of this val is ' + str(len(val)) + ', the key is ' + key)
            if (len(val) < iterboyo):
                #print('motion')
                addon = []
                minidif = iterboyo - len(val)
                if minidif == 1:
                    returndict.get(key).append('')
                else:
                    while(len(addon) < minidif):
                        print('addon len is ' + str(len(addon)) + ', and iterboi is ' + str(iterboyo))
                        addon.append('')
                    print(returndict.get(key))
                    returndict[key] = addon + returndict.get(key)
                    print(returndict.get(key))
                #print(len(dicter.get(key)))

        for key,val in returndict.items():
            print ('key is ' + key + ' and val here is ' + str(val[iterboyo-1]))

        iterboyo+=1

    df = pd.DataFrame(data=returndict)
    return df

def formpull(input):
    print('alex is a dunsparce')

    obj = json.loads(input)

    #remove the outer shell for "answer"
    innerpart = obj.get('answers')

    dicter = mainloop(innerpart, {}, '')

    df = pd.DataFrame(data=dicter)
    return df

def formkeypull(input):
    print('doing a key thing')
    obj = json.loads(input)
    #for dict in the list, pull out items, from
    for formdict in obj:
        #take out the item thing
        itemlist = formdict.get("items")
        print(itemlist)
        print('jemma is cool')







"""
OLD CRAP

filething = 'contacts_spring_17.txt'


with open (filething, encoding="utf8") as f:
    textfile=f.read()


endMark = False
    

#print(len(textfile))


index = 1
keydict = {}
stringhold = ""
appendages = []
lastinsert = ""
keything = ""
readfile = ''


def getFrame(input):
    print('entering rascals fun zone')
    global indexsta
    global keydict
    global stringhold
    global appendages
    global lastinsert
    global keything
    index = 1
    keydict = {}
    stringhold = ""
    appendages = []
    lastinsert = ""
    keything = ""
    endMark = False

    #readfile = input

    dict = iterWork([],stringhold,index, keydict, input, lastinsert, keything)
    print('cleaning')
    print(dict)
    dict = cleanDict(keydict)

    print('passing back the frame')

    return pdExport(dict)

def getCSVExport(input):
    print('entering rascals fun zone')
    global indexsta
    global keydict
    global stringhold
    global appendages
    global lastinsert
    global keything
    index = 1
    keydict = {}
    stringhold = ""
    appendages = []
    lastinsert = ""
    keything = ""
    endMark = False

    #readfile = input

    dict = iterWork([],stringhold,index, keydict, input, lastinsert, keything)
    dict = cleanDict(keydict)

    #print('passing back the frame')

    csvExport(dict)
    return pdExport(dict)

#print("\",\"")

def iterWork(appendages, stringhold, index, keydict, readfile, lastinsert, keything):
    #print("open iterWork at index " + str(index))
    #for key,value in keydict.items():
        #print("key is " + key + " and the value length is " + str(len(value)) + " also the index is " + str(index))
    while (index < len(readfile)-1):
        endMark=False
        #print(stringhold + " " + str(index) + " " + str(appendages))
        #print (keydict)
        #print(str(index))
        #print(appendages)
        tempchar = readfile[index]
        stringhold+=tempchar
        #stringhold = stringhold.strip()
        #print(stringhold)
        if (stringhold == "\",\""):
            #print("hitthat")
            stringhold = ""
            #index += 1
            continue
        if (stringhold[0] == "\""):
            #print("successone")
            if (stringhold[-1] == ":" and stringhold[-2] == "\"" and len(stringhold.strip()) > 1):
                #print("hitone")
                keything = ""
                for stringlet in appendages:
                    keything+=stringlet
                keything += stringhold[1:-2]
                #print("keything is " + keything)
                if keything not in keydict:
                    keydict[keything] = []
                    #print(keything + " empty list value instantiated")
                lastinsert = str(stringhold[1:-2])
                stringhold = ""
                index += 1
                while (index < len(readfile)):
                    tempchar = readfile[index]
                    stringhold += tempchar
                    #print(stringhold + " Spookyloopy")
                    if (tempchar == "["):
                        storage = brakDealtwo(index+1,readfile, keything)
                        index = int(storage)
                        stringhold == ""
                        break
                    if (tempchar == "{"):
                        #print("uhoh")
                        #print(appendages)
                        stringhold = ""
                        xval = iterWork(appendages, stringhold, index, keydict, readfile, lastinsert, keything)
                        #print("LEAVING THE THING REEEEE")
                        appendages = appendages[:-1]
                        stringhold = ""
                        #print("xval is " + str(xval))
                        try:
                            index=int(xval[0])+1
                            appendages=xval[1][:]
                        except TypeError:
                            pass
                        #print("exit iterWork")
                        return [index-1, appendages]
                    if (tempchar == "}"):
                        keydict[keything].append(stringhold[:-1])
                        #print(stringhold[:-1] + " added as a value to closebrak key " + keything)
                        if (index+2 >= len(readfile)):
                            #print("uno")
                            return [index, appendages]
                        elif (readfile[index+2] == "{"):
                            #print("dos")
                            appendages = appendages[:-3]
                        else:
                            #print("tres")
                            appendages = appendages[:-1]
                        #print("fofofofofo")
                        #index+=1
                        #print(appendages)
                        endMark = True
                        break
                    if (len(stringhold) > 2 and stringhold[-1] == "\"" and stringhold[-2] == ","):
                        #print("Hit")
                        #print(stringhold)
                        if(stringhold[0] == "\"" and stringhold[-1] == "\"") :
                           keydict[keything].append(stringhold[1:-3])
                           #print(stringhold[1:-3] + " added as a value to 1 key " + keything)
                        else:
                           keydict[keything].append(stringhold[:-2])
                           #keydict[keything].append(stringhold[2:-3])
                           #print(stringhold[:-2] + " added as a value to 2 key " + keything)
                           #print(keydict)
                        index-=2
                        break
                    if (len(stringhold) > 2 and stringhold[-1] == "{" and stringhold[-2] == ","):
                        keydict[keything].append(stringhold[1:-4])
                        #print(stringhold[1:-4] + " added as a value to 3 key " + keything)
                        break
                    if (index == len(readfile)-1):
                        #print("madeit")
                        #print(stringhold[1:-3])
                        keydict[keything].append(stringhold[1:-3])
                        #print(stringhold[1:-3] + " added as a value to 4 key " + keything)
                    index+=1
                stringhold = ""
                index+=1
                if(endMark):
                    #print("lololololololololol")
                    #appendages = appendages[:-1]
                    lastinsert = ""
                    return [index, appendages]
                    #print(appendages)
                #print("This is the thing")
                continue
            elif (stringhold[len(stringhold)-2] == "\"" and len(stringhold) > 2):
                #print("hittwo")
                stringhold = ""
                index+=1
                continue
            else:
                #print("string is building")
                index+=1
                continue
        elif (stringhold[0] == "["):
            #print("entering brakDeal")
            storage = brakDeal(index+1, readfile)
            stringhold=""
            #print(index)
            index = int(storage)
        elif (stringhold == "{"):
            #print("openbrackfind")
            if (len(lastinsert) != 0):
                lastinsert+="-"
            appendages.append(lastinsert)
            #print("ENTERING RECURSION")
            #print(appendages)
            keydict.pop(lastinsert[:-1], None)
            xval = iterWork(appendages, "", index+1, keydict, readfile, lastinsert, keything)
            #print("exiting the open loop")
            appendages = appendages[:-1]
            stringhold = ""
            #print("xval is " + str(xval))
            #print("thingthingthing " + str(xval[0]))
            try:
                index=int(xval[0])+1
                appendages=xval[1][:]
            except TypeError:
                pass
            continue
        elif (stringhold == "}"):
            #print("closebrackfind")
            appendages = appendages[:-1]
            #print("exitIterwork")
            return [index, appendages]
        else:
            #print("continuation")
            stringhold = ""
            index+=1
    print("exit iterWork")
    return [index, appendages]

def brakDeal(index, readfile):
    #print("enter brakdeal")
    #indexhold = int(index)
    while (index < len(readfile)-1):
        tempchar = readfile[index]
        #print("brakDeal char is " + tempchar)
        if (tempchar=="["):
            #print("open")
            storage = brakDeal(index+1, readfile)
            index = int(storage)
        elif (tempchar=="]"):
            #print("exit brakdeal")
            return index+1
        else:
            index+=1
    #print("exit loop at indexhold " + str(index))

def brakDealtwo(index, readfile, keything):
    #print("enter brakdeal2")
    keydict[keything].append("null")
    while (index < len(readfile)-1):
        tempchar = readfile[index]
        #print("brakDeal char is " + tempchar + " and the index is " + str(index))
        if (tempchar=="["):
            #print("open")
            storage = brakDeal(index+1, readfile)
            index = int(storage)
        elif (tempchar=="]"):
            #print("exit brakdeal2")
            return index+1
        else:
            index+=1


xval = iterWork(appendages, stringhold, index, keydict, textfile, lastinsert, keything)

try:
    index=int(xval[0])+1
    appendages=xval[1][:]
except TypeError:
    pass

#print(index)
#print(keydict)



#print(keydict)

#print("DataComplete")

removeList = []


def cleanDict(keydict):
    for key, value in keydict.items():
        #print(key)
        #print(len(value))

        if (len(value) < len(keydict['id'])):
            removeList.append(key)


    for item in removeList:
        keydict.pop(item, None)

    return keydict

def pdExport(keydict):
    #pd.DataFrame(data=keydict).to_csv('exporter' + '.csv')
    df = pd.DataFrame(data=keydict)
    return df

def csvExport(keydict):
    pd.DataFrame(data=keydict).to_csv('PIEthonExport' + '.csv')
    return True

#print("Exported")
"""
