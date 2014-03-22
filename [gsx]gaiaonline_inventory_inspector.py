'''/
Author: @king
Date: 3/22/2014
Description: Gaiaonine "Inventory" inspector
Website: http://www.glitch.sx
Keywords: gaiaonline, avatar, forum, login, forms, python, hack, cheat, bot, script, tool, mechanize, automated
'''
import mechanize, urllib, re, string, getpass
# Build web-browser for autmation of tasks
br = mechanize.Browser()
# Some mechanize hacks          
br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this
# Finish web-browser, the header is what you send back that specifies what browser and os you are using
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
cookie_jar = mechanize.CookieJar() # Cookie jar is important, you won't stay logged in if you don't use it
br.set_cookiejar( cookie_jar )

def main_loop():
    '''/
    main loop function
    '''
    while True:
        print("[-] Welcome to King's inventory check - www.glitch.sx")
        username = raw_input("Enter your username:") #raw_input is a function to get data from end user
        password = raw_input("Enter your password:")
        if(gaia_login(username,password)): #Call our login function to perform the login
            print("[+] Finding net worth")
            id_list = get_inventory_id_list()
            item_list = get_inventory_item_list()
            #-initialize networth with current gold
            net_worth = int(get_gold())
            for iid,item in zip(id_list,item_list):
                qnty = int(1)
                try:#-check for quanity
                    #-...Sloppy hacked together quanity check...
                    delete = "(',)"
                    q1 = re.search("\((\d+)\)",item).groups(1)
                    qnty = int(q1.translate(None,delete))
                except:
                    pass
                #-..again a sloppy fix for the right item numbers to value
                fixed_id = iid[0:iid.find('.')]
                v = value(fixed_id,qnty)
                print(item, v)
                net_worth = net_worth + v
            print(net_worth)
        #-loop-
        next_ = raw_input("[+] login to another account (y/n)?")
        if next_ == 'y':
            gaia_logout() #Call log-out so we can use another account
        else:
            break # end the loop and quit if user doesnt input y.

def gaia_login(username, password):
    '''/
    this will be our login function
    takes the parameters username, and password
    this are the account details used for login
    '''
    url = "http://www.gaiaonline.com" #url of gaiaonline homepage
    br.open(url) #using our browser made earlier we can opn the site
    br.select_form(nr=0) #this identifies what forum to use.
    br["username"] = username
    br["password"] = password
    br.submit() # fill in login information. send request
    if "Welcome back" in br.response().get_data():
        return True
def gaia_logout():
    '''/
    this is a simple function to clear the cookie jar effectively logging the user out.
    '''
    cookie_jar.clear()

def get_gold():
    '''/
    return the amount of gold user has at the moment
    '''
    url = "http://www.gaiaonline.com"
    response = br.open(url).read()
    return str( re.search('<span id="go1d_amt">(.*?)</span>', response).group(1) ).replace(',', '')

def get_inventory_id_list():
    '''/
    return list of item names, and quanity
    '''
    url = "http://www.gaiaonline.com/inventory/ajax/"
    response = br.open(url).read()
    return re.findall('''data-slot="(.*?)"''', response)

def get_inventory_item_list():
    url = "http://www.gaiaonline.com/inventory/ajax/"
    response = br.open(url).read()
    return re.findall('''title="(.*?)"''', response)

def value( item_id, q ):
    '''/
    return integer value of item id
    q is a  multiplier for quanity.
    '''
    url = "http://www.gaiaonline.com/inventory/itemdetail/" + item_id
    response = br.open(url).read()
    #-Initilize values incase nothing found..
    sellback_value = int(0)
    avg_value = int(0)
    #-Find sellback value
    try:
        sellback_value = int( re.search("Sellback Value: (.*?)g",response).group(1) )
    except:
        pass
    #-find average
    try:
        avg_value = int( re.search("Avg. Market Price: (.*?)g",response).group(1) )
    except:
        pass
    #determine value
    if sellback_value > avg_value:
        return sellback_value * q
    else:
        return avg_value * q
    
main_loop() #start the program
