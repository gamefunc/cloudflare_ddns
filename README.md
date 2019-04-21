# cloudflare_ddns
cloudflare ddns for python3 ; support ipv4 and ipv6;

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
