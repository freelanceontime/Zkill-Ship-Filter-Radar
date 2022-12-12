from bs4 import BeautifulSoup
from websocket import create_connection
import json
import requests
from discord import SyncWebhook

allianceid = 99001105
corpid = 98512964
shiptype1 = [44996,22440,22428,22430,22436] # Blackops
shiptype2 = [23919,22852,3628,23913,3514,42125,23917] # Supers
shiptype3 = [32790,32207,32209,2834,2836,3516,3518,32788,33397,33395,33673,33675,35779,35781,42246,42245,45530,45531,48636,48635,60765,60764] # AT Ships
shiptype4 = [45647,42243,19724,34339,73792,19722,73787,34341,19726,73793,34343,19720,34345,73790,42124,52907] # Dreads

killstream = '{"action":"sub","channel":"killstream"}'
systemstartid = "30003335"
jumprange = 10
webhookchannel = "https://discord.com/api/webhooks/1044558007385722951/KQfA8QbAViUeEAubTwjtcPmnX380Vze2DK1AO-IZfXmZseDaTlRF0chfBQQrha6rgAvp"
webhookchannel2 = "https://discord.com/api/webhooks/1044994782746919033/wJ1OiKFF0OWFvJQIcnPfwj_a4FF70T7_nvm2s3eRT3DKwsOCrQpbW3_qgXQDLPKM92Mg"

def test():
    sendkill1 = False
    sendkill2 = False
    sendkill3 = False
    sendkill4 = False
    print("New Connection Established")
    ws = create_connection("wss://zkillboard.com/websocket/")
    ws.send(killstream)
    
    while True:
        urls = []
        systems = []
        attackers = []
        shiptypes = []
        result =  ws.recv()
        data = json.loads(result)
        urls.append(data['zkb']['url'])
        systems.append(data['solar_system_id'])
        attackers.append(data['attackers'])

        attackernumber = len(attackers[0])

        for shipids in range(attackernumber):
            try:
                shiptypes.append(data['attackers'][shipids]['ship_type_id'])
            except KeyError:
                print("Ship ID Error")

        for i in range(len(urls)):
            
            killurl = str(urls[i])
            urljumps = "https://evemaps.dotlan.net/route/" + str(systemstartid) + ":" + str(systems[i])

            for ship in shiptypes:
                if ship in shiptype1:
                    
                    try:
                        page = requests.get(urljumps)
                        soup = BeautifulSoup(page.content, 'html.parser', on_duplicate_attribute='ignore')

                        tab = soup.find("table",{"class":"tablelist table-tooltip"})
                        number_of_rows = tab.findAll(lambda tab: tab.name == 'tr' and tab.findParent('table'))
                        jumpsaway1 = (len(number_of_rows) - 1)
                    except AttributeError:
                        print("Jspace")
                    
                    if jumpsaway1 <= jumprange:
                        sendkill1 = True
                    else:
                        print("Not in Specified Range")
                
                elif ship in shiptype2:
                    
                    try:
                        page = requests.get(urljumps)
                        soup = BeautifulSoup(page.content, 'html.parser', on_duplicate_attribute='ignore')

                        tab = soup.find("table",{"class":"tablelist table-tooltip"})
                        number_of_rows = tab.findAll(lambda tab: tab.name == 'tr' and tab.findParent('table'))
                        jumpsaway2 = (len(number_of_rows) - 1)
                    except AttributeError:
                        print("Jspace")
                    
                    if jumpsaway2 <= jumprange:
                        sendkill2 = True
                    else:
                        print("Not in Specified Range")

                elif ship in shiptype3:
                    
                    try:
                        page = requests.get(urljumps)
                        soup = BeautifulSoup(page.content, 'html.parser', on_duplicate_attribute='ignore')

                        tab = soup.find("table",{"class":"tablelist table-tooltip"})
                        number_of_rows = tab.findAll(lambda tab: tab.name == 'tr' and tab.findParent('table'))
                        jumpsaway3 = (len(number_of_rows) - 1)
                    except AttributeError:
                        print("Jspace")
                    
                    if jumpsaway3 <= jumprange:
                        sendkill3 = True
                    else:
                        print("Not in Specified Range")

                if ship in shiptype4:
                    
                    try:
                        page = requests.get(urljumps)
                        soup = BeautifulSoup(page.content, 'html.parser', on_duplicate_attribute='ignore')

                        tab = soup.find("table",{"class":"tablelist table-tooltip"})
                        number_of_rows = tab.findAll(lambda tab: tab.name == 'tr' and tab.findParent('table'))
                        jumpsaway4 = (len(number_of_rows) - 1)
                    except AttributeError:
                        print("Jspace")
                    
                    if jumpsaway4 <= jumprange:
                        sendkill4 = True
                    else:
                        print("Not in Specified Range")        
                else:
                    print("Ship is not Present")    
            

            if sendkill1 == True:
                webhook = SyncWebhook.from_url(webhookchannel)    
                webhook.send("Kill Found in Specified Range with a BlackOps")
                webhook.send(killurl)
                print("kill reported")
                sendkill1 = False

            if sendkill2 == True:
                webhook = SyncWebhook.from_url(webhookchannel)    
                webhook.send("Kill Found in Specified Range with a SuperCarrier")
                webhook.send(killurl)
                print("kill reported")
                sendkill2 = False

            if sendkill3 == True:
                webhook = SyncWebhook.from_url(webhookchannel2)    
                webhook.send("Kill Found in Specified Range with an Alliance Tournament Ship")
                webhook.send(killurl)
                print("kill reported")
                sendkill3 = False

            if sendkill4 == True:
                webhook = SyncWebhook.from_url(webhookchannel)    
                webhook.send("Kill Found in Specified Range with a Dreadnought")
                webhook.send(killurl)
                print("kill reported")
                sendkill4 = False

while True:
    try:
        test()
    except:
        print("Connection Lost")
        pass

