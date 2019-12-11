import asyncio, re, os.path
from os import system, name
from proxybroker import Broker


async def countryProxy(proxies):
    print("\n.-_-._-_/*[Alfix00's Gather proxy]*\.-_-._-_ \n")
    list_proxy = []
    choice = str(input("Do you wanna prox from some specific country? \n\n\t[Y = YES] [other = Random]: ")).upper()
    settings = False
    country = ""
    if choice == "Y":
        settings = True
        country_list()
        print("[*] Digit only the tag of the country (ex: RU, DE, FR, ... )\n\n[i]-> Insert [0] to stop the loop [i]")
        while(country != "0"):
            country = str(input("\nInsert country: ")).upper()
            ok = checkCountry(country)
            if country != "0" and ok:
                list_proxy.append(country)
        print("\nYou have added: \n")
        print(*list_proxy, sep=",")
    if choice != "Y":
        print("\n\t[/] No preference selected. [/] \n\n[*] -> Finding random proxy <- [*]\n")

    pattern = str(input("\nDo you want save the pattern of proxies [HTTP/HTTPS/...] ? [Y = YES] [other = NO]: "))
    savePattern = False
    if pattern == "Y":
        print("\n[+] You chose to save pattern [+]\n")
        savePattern = True
    elif pattern != "Y":
        print("\n[-] No pattern saving [-]\n")
    print("\n\n[*] The process may get some times... \n\n")
    cont = 0
    try:
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            geo = str(proxy._geo)
            geo_formatted = geo[geo.find("=")+1:geo.find(",")].replace("'","").replace(" ","")
            filename = "./proxy_folder/proxy_"+geo_formatted+".txt"
            if not settings or ((geo_formatted in list_proxy or geo_formatted == country) and settings):
                with open(filename, 'a+') as f:
                    cont = cont + 1
                    print('-> ',cont,') added ',proxy)
                    if savePattern is True:
                        proto = 'https' if 'HTTPS' in proxy.types else 'http'
                        row = '%s://%s:%d\n' % (proto, proxy.host, proxy.port)
                        proxy = proxyList(proxy.host,proxy.port,proto,proxy._timeout)
                        list_proxy.append(proxy)
                        f.write(row)
                    elif savePattern is False:
                        row = '%s:%d\n' % (proxy.host, proxy.port)
                        list_proxy.append(proxy)
                        f.write(row)
    except KeyboardInterrupt:
        print("\nFinish!! All proxy was saved in proxy.txt file")

def checkFolder():
    if not os.path.isfile("./proxy_folder"):
        try:
            os.mkdir("proxy_folder")
        except OSError:
            pass

def checkCountry(country):
    if len(country) != 2:
        print("\nError! Please digit only the tag of the country (ex: RU, DE, FR, UK ... )")
        return False
    return True


def country_list():
    print("\n----------------------------------------------------------------[You choice: YES]---------------")
    print("\n[-] Channel Example: ")
    print("\n\
           IT - Italian\n\
           US - United States\n\
           IN - India\n\
           GB - Grand Britain\n\
           RU - Russia\n\
           FR - France\n\
           CO - Columbia\n\
           CZ - Czech\n\
           DE - German\n\
           KO - Korean\n\
           PL - Polish\n\
           ES - Spanish\n\
           UK - Ukrainian\n\
           DA - Danish\n\
           EL - Greek \n\
           \nFor each more, check other tags on: https://www.andiamo.co.uk/resources/iso-language-codes/ \n")
    print("--------------------------------------------------------------------------------------------------")


def main():
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    checkFolder()
    tasks = asyncio.gather(
        broker.find(types=['HTTP', 'HTTPS'], limit=None),
        countryProxy(proxies)
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)


if __name__ == '__main__':
    main()

