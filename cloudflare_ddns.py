import requests
import json
import sys

def cloudflare_ddns(myIp, useCDN, domain, subDomian, ipType, cF_email, cF_ApiKey):
    if subDomian == "":
        requestDomain = domain
    else:
        requestDomain = subDomian + "." + domain

    baseUrl = "https://api.cloudflare.com/client/v4"
    headers = {"X-Auth-Email": cF_email, "X-Auth-Key": cF_ApiKey, "Content-Type": "application/json"}

    # get zone
    zonIdUrl = f"{baseUrl}/zones"
    pageNum = 1
    total_pages = None
    zonesDict = {}
    while True:
        zone = requests.request("get", zonIdUrl, headers=headers, params={"page": pageNum})
        if (zone.status_code != 200):
            print(f"connect fail; email wrong:403; api wrong:400; headers wrong:400; url wrong: 404, now is: {zone.status_code}")
            break
        tmpDict = json.loads(zone.text)
        zonesDict[tmpDict["result"][0]["name"]] = tmpDict["result"][0]["id"]
        total_pages = tmpDict["result_info"]["total_pages"]
        if pageNum == total_pages:
            break

    # get domain id
    zoneID = zonesDict.get(domain, 0)
    if zoneID == 0:
        raise TypeError(f"this cloudflare account have't : {domain}")
    dns_recordsUrl = f"{baseUrl}/zones/{zoneID}/dns_records"
    dns_record = requests.request("get", dns_recordsUrl, headers=headers)
    dns_recordDict = json.loads(dns_record.text)


    # get requestDomain id
    recordID = None
    for i in range(len(dns_recordDict["result"])):
        if dns_recordDict["result"][i]["name"] == requestDomain:
            print("hit :", dns_recordDict["result"][i]["name"])
            recordID = dns_recordDict["result"][i]["id"]
            if useCDN != "keep":
                useCDN = dns_recordDict["result"][i]["proxied"]
            else:
                useCDN = True if useCDN == "yes" else False
            break

    # change dns record
    recordEditUrl = f"{baseUrl}/zones/{zoneID}/dns_records/{recordID}"
    payload = {"type": ipType, "name": requestDomain, "content": myIp, "ttl":120, "proxied":useCDN}
    changeDns = requests.request("put", recordEditUrl, headers=headers, json=payload) # or data=json.dumps(payload)
    print(f"\n    Last Response status_code: {changeDns.status_code}; \"**if 200 is ok, other is noway;**\" \n")
    print(f"    Last Response json : \n         {changeDns.json()}")



if __name__ == "__main__":
    paramenter_help = """
        # only support python3; need: pip3 install requests;
        # https://api.cloudflare.com/#dns-records-for-a-zone-update-dns-record
        # parameters:
            -e: cloudflare login email: 
                example: fevefun@hotmail.com;
            -k: cloudflare Global Key:  
                > goto -> cloudflare Homepage -> My Profile -> API Keys -> Global API Key -> View;
            -d: will change domain: 
                example:  gamefunc.top;
            -sd: subdomain: 
                default is ""。example: www;
            -t: IP Type:
                ipv4=A, ipv6=AAAA。 default: A;
            -ip:
                will change ip. default:  auto get from web;
            -cdn:
                proxied, Whether the record is receiving the performance and security benefits of Cloudflare;
                [yes | no | keep]; default: keep set; 
            
        # how to use(1): 
            example: 
                # change gamefunc.top:
                    python3 cloudflare_ddns.py -e fevefun@hotmail.com -k 1234567 -d gamefunc.top 
                # change www.gamefunc.top:
                    python3 cloudflare_ddns.py -e fevefun@hotmail.com -k 1234567 -d gamefunc.top -sd www
                # direct set ip:
                    python3 cloudflare_ddns.py -e fevefun@hotmail.com -k 1234567 -d gamefunc.top -sd home -t A -ip 192.168.1.1
                # if change to ipv6:
                    python3 cloudflare_ddns.py -e fevefun@hotmail.com -k 1234567 -d gamefunc.top -sd ipv6 -t AAAA
        # how to use(2):
            direct change "paramets" dict variable;
            
        # crontab -e
            0,10,20,30,40,50 * * * * /usr/bin/python3 /etc/hahaha/cloudflare_ddns.py -e fevefun@hotmail.com -k 1234567 -d gamefunc.top 
            2,12,22,32,42,52 * * * * /usr/bin/python3 /etc/hahaha/cloudflare_ddns.py -e fevefun@hotmail.com -k 1234567 -d gamefunc.top -sd www
    """

    paramets = { "-h": paramenter_help,
                 "-e": "fevefun@hotmail.com",
                 "-k": "12345678CloudFlareGlobalApiKey",
                 "-d": "gamefunc.top",
                 "-sd": "",
                 "-t": "A",
                 "-ip": None,
                 "-cdn": "keep"}

    inputParamets = sys.argv

    if ("--help" in inputParamets) or ("-h" in inputParamets) :
        print(paramets["-h"])
        sys.exit(0)

    for parameter in paramets.keys():
        if inputParamets.count(parameter) > 1:
            raise TypeError(f"{parameter} input > 1")

    for parameter in paramets.keys():
        try:
            index =  inputParamets.index(parameter)
            paramets[parameter] = inputParamets[index+1]
            print(f"{parameter} => {inputParamets[index+1]}")
        except:
            pass

    if paramets["-ip"] is None:
        if paramets["-t"] == "A":
            myIp = requests.request("get", "http://ipv4.icanhazip.com")
        elif paramets["-t"] == "AAAA":
            myIp = requests.request("get", "http://ipv6.icanhazip.com")
        else:
            raise TypeError("-t wrong: ipv4 set it A, ipv6 set it AAAA")

        if myIp.status_code != 200:
            raise TypeError(f"can't get public ip {myIp.status_code}")

        paramets["-ip"] = myIp.text.strip()

        # import netifaces
        # myIp = netifaces.ifaddresses('ppp0')[2][0]['addr']

    # exec
    cloudflare_ddns(paramets["-ip"], paramets["-cdn"], 
                    paramets["-d"], paramets["-sd"], paramets["-t"],
                    paramets["-e"], paramets["-k"])
