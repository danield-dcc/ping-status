import os, platform, csv
from datetime import date, datetime


input_results = []
txt_results = []
ping_result = []
loop = True
initial = True


def verify_platform():
    packagesNumber = 5
    if(platform.system().lower == 'windows'):
        #comando para windows é -n
        return "-n " + str(packagesNumber) + " "
    else:
        #comando para linux/mac é -n
        return "-c " + str(packagesNumber) + " "

def mount_ping_cmd(domain, packageParameter, fileName):

    #deleta o arquivo teste.txt, caso ele já existe
    if(os.path.exists("teste.txt")):
         os.remove("teste.txt")

    cmd = f'ping {str(packageParameter)} {str(domain)} >> {fileName}'
    return cmd.replace("\n", "")

def executePing(cmd):
    result = os.system(str(cmd))
    return result

def verifyStatusUrl(ping_return, domain):
    if(ping_return == 0):
        print("\n---------------")
        print("Status: " + domain + " ONLINE")
        return "ONLINE"

    else:
        print("\n---------------")
        print("Status: " + domain + " OFFLINE")
        return "OFFLINE"

def getDate():
    today = date.today()
    return today.strftime("%d-%m-%Y")

def getTime():
    time = datetime.now()
    return time.strftime("%H:%M:%S")

def readFile(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()


    print("---------------------PINGANDO--------------")
    for line in lines:
        print(line)
    file.close()
    print("--------------------- FIM--------------")

    return lines



def getSiteIp(file_name):
    lines = readFile(file_name)
    ipSliceBegins = lines[1].index("(")
    ipSliceEnds = lines[1].index(")")
    siteIp = lines[1][ipSliceBegins + 1 : ipSliceEnds]
    return siteIp

def getSiteTTL(file_name):
    lines = readFile(file_name)
    ipSliceBegins = lines[1].find("ttl=")
    return lines[1][ipSliceBegins + 4 : ipSliceBegins + 6]

def getPingTime(file_name):
    lines = readFile(file_name)
    timeSliceBegins = lines[1].find("time=")
    timeSliceEnds = lines[1].find("ms")
    timeList=[]
    for line in lines:
        timeList.append(line[timeSliceBegins + 5 : timeSliceEnds])

    #remove empty string from list
    while("" in timeList):
        timeList.remove("")

    while("\n" in timeList):
        timeList.remove("\n")    

    print("timeList", timeList)    

    # convert string to int
    integer = [eval(i) for i in timeList]

    media = sum(integer)/len(timeList)
    return media

def getLostPackages(file_name):
    lines = readFile(file_name)
    lost = []
    for line in lines:
        if(line.find("% packet loss") != -1):
            index = line.find("% packet loss")
            lost.append(line[index -1 : index ])
    return lost


def printFinalResults(final_results):
    print("URL --------------| IP ----------------------- | Status ------- | Data ------- | Hora -------")
    for result in final_results:
        print(f'{result["domain"]:19} {result["siteIp"]:28} {result["status"]:16} {result["data"]:14} {result["time"]}')
    print('\n')

def verify_if_csv_exist():
    if(os.path.exists("teste.txt")):
        return True
    
    return False

def read_csv_file():
    csv_list = []
    if(os.path.exists("teste.txt")):
        with open('logIpsCSV.csv', mode="r") as file:
            reader = csv.reader(file, dialect='excel', delimiter = '\t')
            for row in reader:
                print(f'Arquivo: {row}')
                csv_list.append(row)
        return csv_list
    
    return csv_list          


def save_csv_file(final_results):
    
    with open('logIpsCSV.csv', mode="w") as logIpsCSV_file:
        logIpsCSV_file = csv.writer(logIpsCSV_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_list = read_csv_file()
        print("values", csv_list)
        # if len(csv_list) == 0:
        #       logIpsCSV_file.writerow(['URL', "IP" ,"Status","Data","Hora"])

        if(verify_if_csv_exist() == False):
            logIpsCSV_file.writerow(['URL', "IP" ,"Status","Data","Hora"])

        for result in final_results:
            logIpsCSV_file.writerow([f'{result["domain"]}', f'{result["siteIp"]}', f'{result["status"]}', f'{result["data"]}', f'{result["time"]}'])



def initPingProcess(domain):
    # domain = "www.google.com"
    packs = verify_platform()
    file_name = "teste.txt"
    cmd = mount_ping_cmd(domain, packs, file_name)
    ping_return = executePing(cmd)
    status = verifyStatusUrl(ping_return, domain)
    day = getDate()
    time = getTime()
    siteIp = getSiteIp(file_name)
    siteTTL = getSiteTTL(file_name)
    pingTime = getPingTime(file_name)
    lostPackages = getLostPackages(file_name)

    print("\nURL                 | STATUS  | DATA         | HORA      | IP                        | TTL    | Tempo(média)  | Pacotes perdidos")
    print(f'{domain:{21}}',f'{status:{9}}',f'{day:{14}}',f'{time:{11}}',f'{siteIp:{28}}', f'{siteTTL:{8}}', f'{"%.2f" % pingTime}',f'{"ms":{10}}'  f'{lostPackages[0]}%')

    input_results.append({"domain":domain.replace("\n", ""), "siteIp":siteIp, "status":status, "time":time, "data":day})


def readIpFile():
    file = open("ip_url.txt", "r")
    url_lines = file.readlines()

    for url in url_lines:
        packs = verify_platform()

        packs = verify_platform()
        file_name = "logIps.txt"
        cmd = mount_ping_cmd(url, packs, file_name)
        
        print("-----Pingando URL: ", url)
        ping_return = executePing(cmd)
        status = verifyStatusUrl(ping_return, url)
        day = getDate()
        time = getTime()
        siteIp = getSiteIp(file_name)
        siteTTL = getSiteTTL(file_name)
        pingTime = getPingTime(file_name)
        lostPackages = getLostPackages(file_name)
        domain = url.replace('\n',"")

        print("\nURL                 | STATUS  | DATA         | HORA      | IP                        | TTL    | Tempo(média)  | Pacotes perdidos")
        print(f'{domain:{21}}',f'{status:{9}}',f'{day:{14}}',f'{time:{11}}',f'{siteIp:{28}}', f'{siteTTL:{8}}', f'{"%.2f" % pingTime}',f'{"ms":{10}}'  f'{lostPackages[0]}%')

        txt_results.append({"domain": domain, "siteIp":siteIp, "status":status, "time":time, "data":day})
    
    



def add_url():
    loop = True
    initial = True
    while(loop):
        print("\n--------------BEM VINDO ------------")
        if(initial == True):
            # val = input("Digite uma URL: ").lower()
            val = 'www.google.com'
            initPingProcess(val)
            initial = False

        cont = input("\nVOCE QUE PINGAR MAIS UMA URL? [S]IM OU [N]AO: ")

        if(cont[:13].upper() == "S"):
            domain = input("Digite o IP ou URL que você que pingar: ")
            initPingProcess(domain)

        elif(cont[:4].upper() == "N"):
            print("\n#################### FIM DE PROGRAMA ####################\n")
            loop = False
            printFinalResults(input_results)
            break
        else:
            print("Comando invalido, tente novamente")

def read_txt():
    readIpFile()
    read_csv_file()    
    printFinalResults(txt_results)
    save_csv_file(txt_results)
    

while True:
  print('+========================================+')
  print('|            Teste de PING               |')
  print('|========================================|')
  print('|1. Adicionar url                        |')
  print('|2. Ler arquivo de texto                 |')
  print('|9. Sair                                 |')
  print('+========================================+')
  option = int(input('Opção: '))
  if option == 1:
    add_url()
  elif option == 2:
    read_txt()
  else:
    break