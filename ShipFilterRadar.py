from bs4 import BeautifulSoup
from websocket import create_connection
import json
import requests
from discord import SyncWebhook

allianceid = 99001105
corpid = 98512964
shiptype1 = [44996,22440,22428,22430,22436]
shiptype2 = [23919,22852,3628,23913,3514,42125,23917]
alliancekillstream = '{"action":"sub","channel":"alliance:99001105"}'
killstream = '{"action":"sub","channel":"killstream"}'
systemstartid = "30003335"
jumprange = 10
webhookchannel = ""

def test():
    sendkill1 = False
    sendkill2 = False
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
                if ship == shiptype1[0] or ship == shiptype1[1] or ship == shiptype1[2] or ship == shiptype1[3] or ship == shiptype1[4]:
                    
                    try:
                        page = requests.get(urljumps)
                        soup = BeautifulSoup(page.content, 'html.parser', on_duplicate_attribute='ignore')

                        tab = soup.find("table",{"class":"tablelist table-tooltip"})
                        number_of_rows = tab.findAll(lambda tab: tab.name == 'tr' and tab.findParent('table'))
                        jumpsaway = (len(number_of_rows) - 1)
                    except AttributeError:
                        print("Jspace")
                    
                    if jumpsaway <= jumprange:
                        sendkill1 = True
                    else:
                        print("Not in Specified Range")
                elif ship == shiptype2[0] or ship == shiptype2[1] or ship == shiptype2[2] or ship == shiptype2[3] or  ship == shiptype2[4] or ship == shiptype2[5] or ship == shiptype2[6]:
                    
                    try:
                        page = requests.get(urljumps)
                        soup = BeautifulSoup(page.content, 'html.parser', on_duplicate_attribute='ignore')

                        tab = soup.find("table",{"class":"tablelist table-tooltip"})
                        number_of_rows = tab.findAll(lambda tab: tab.name == 'tr' and tab.findParent('table'))
                        jumpsaway = (len(number_of_rows) - 1)
                    except AttributeError:
                        print("Jspace")
                    
                    if jumpsaway <= jumprange:
                        sendkill2 = True
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
                sendkill1 = False

        ws.close()

while True:
    try:
        test()
    except:
        print("Connection Lost")
        pass

