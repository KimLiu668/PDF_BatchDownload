import urllib.request
import re
import os
import xlrd
import datetime
from tqdm import tqdm
import threading

def getrawurl():
    data = xlrd.open_workbook(r'C:\Users\Kliu2\Desktop\007.xlsx')
    table = data.sheet_by_name(u'Sheet1')
    raw_url = table.col_values(5)[1:]
    temp = []
    for i in raw_url:
        reglex = re.compile(r'MonthlyReport/(.*?).pdf')
        code = re.findall(reglex,i)
        temp.append(code[0])
    urls = []
    for i in temp:
        url =r'http://www.nordea.lu/sitemod/upload/Root/FundReports/MonthlyReport/'+str(i)+'.pdf'
        urls.append(url)
    return urls   
    
def getFile(url):
    file_name = url.split('/')[-1]
    u = urllib.request.urlopen(url)
    f = open(file_name, 'wb')
    block_sz = 8192
    # time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(time)
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        f.write(buffer)
    f.close()
    # print ("Sucessful to download" + " " + file_name)


def GetPdf(Begin,End,Num,progress):
    for i in range(Begin,End):
        if i < Num:
            mutex.acquire()
            url = urls[i]
            getFile(url)
            mutex.release()
            progress.update(1)
            

            
        
os.mkdir('pdf_download')
os.chdir(os.path.join(os.getcwd(), 'pdf_download'))
TotalThread = 50
urls = getrawurl()
Num = len(urls)
Gap = int(float(Num)/TotalThread)
progress = tqdm(total = Num, ascii = True)
mutex = threading.Lock()

ThreadList = [threading.Thread(target=GetPdf,args = (i,i+Gap,Num,progress,)) for i in range(0,Num,Gap)]

for i in ThreadList:
    i.setDaemon(True)
    i.start()
for t in ThreadList:
    t.join()
print('done')