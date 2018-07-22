import re
import os
import sys
import time
import requests
import random
import datetime
import pandas as pd
import urllib.parse
from tqdm import tqdm
from urllib import parse
from shutil import rmtree

def cur_file_dir():
    path = os.path.dirname(os.path.realpath(sys.argv[0]))
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

def get_raw_url():
    urls = []
    with open(cur_file_dir()+'\\'+'PDF_Urls.txt','r') as f:
        raw=f.readlines()
        for url in raw:
            url = url.replace('\n','')
            urls.append(url)
    return urls   

def get_File(urls,progress,seconds,flag,num_retries=2):
    lst = []
    for i in urls:
        # proto, rest = urllib.parse.splittype(i)
        # res, rest = urllib.parse.splithost(rest)
        url = parse.unquote(i)
        # 'Connection':'keep-alive',
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',}
            # headers['Referer']=i
            # if res:
            #     headers['Host']='www.'+res                
            response = requests.get(url,headers =headers,stream =True)
            if 100<= response.status_code<=300 and response.text != '':
                if 'Content-Disposition' in response.headers.keys():
                    u = response.headers['Content-Disposition']
                    file_name = re.findall(r'(?i)(?<=filename=)"?(.*?.pdf)"?',u)[0]
                elif re.search('.*?.pdf$',url):
                    name = url.split('/')[-3:]
                    file_name = name[0]+'_'+name[1]+'_'+name[2]
                else:
                    name = url.split('/')[-2:]
                    file_name = re.sub(r'(?|\|:)','_',name[0])+'_'+re.sub(r'(?|\|:)','_',name[1])+'.pdf'
                with open(file_name, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):  
                        f.write(chunk)
                        f.flush()
                    # f.write(response.content)
                item = [url,file_name[:-4],'Downloaded successfully']
                lst.append(item)
                time.sleep(seconds)
            elif 400<= response.status_code<500:
                item = [url,'----','This URL can not be downloaded:'+str(response.status_code)+'-'+response.reason]
                lst.append(item)
                flag +=1
            elif 500<= response.status_code<600:
                if num_retries>0:
                    return get_File(url,progress,flag,num_retries-1)
                else:
                    item = [url,'----','This URL can not be downloaded:'+str(response.status_code)+'-:'+response.reason]
                    lst.append(item)
                    flag +=1
        except Exception as e:
            item = [url,'----','Can not open this URL:'+str(e)]
            lst.append(item)
            flag +=1
        finally:
            progress.update(1)
    return [lst,flag]

def Create_Excel(lst,Num,seconds,flag):           
    a = pd.DataFrame(data=lst,columns = ['Url','File_Name','Comment'])
    a.to_csv(cur_file_dir()+'\\'+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+'_'+'PDF_Download.csv')
    if flag != 0:
        s = int(Num) -int(flag)
        print('%d PDF have been downloaded successfully.%d PDF fail to download,please see the csv'%(s,int(flag)))
    else:
        print('All PDF have been downloaded successfully,please see the csv')





if __name__ =='__main__':
    print('Start Downloading..')    
    if not os.path.exists(cur_file_dir()+'\\'+'pdf_download'):        
        os.mkdir(cur_file_dir()+'\\'+'pdf_download')
        os.chdir(os.path.join(cur_file_dir(),'pdf_download'))
    else:
        rmtree(cur_file_dir()+'\\'+'pdf_download')
        os.mkdir(cur_file_dir()+'\\'+'pdf_download')
        os.chdir(os.path.join(cur_file_dir(),'pdf_download'))
    urls = get_raw_url()
    Num = len(urls)
    progress = tqdm(total = Num, ascii = True)
    seconds = random.randint(2,4)
    flag = 0
    a = get_File(urls,progress,seconds,flag,num_retries=2)
    lst = a[0]
    flag =a[1]
    Create_Excel(lst,Num,seconds,flag)