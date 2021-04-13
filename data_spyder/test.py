import asyncio
import requests_async as requests
import re
from bs4 import BeautifulSoup
import os

async def get_data_list(url,es):
    urls = []
    print("start get ", url)
    i = 0
    while True:
        i+=1
        if i > 10 :
            print("url maybe not correct:",url)
            break
        try:
            rep = await requests.get(url)
            if rep.status_code == 200:
                break 
            elif rep.status_code == 404:
                print("url not found ", url)
                break
            else:
                await asyncio.sleep(1)
        except:
            await asyncio.sleep(1)
            continue
    # matchs = re.findall(f"{site}\.\d4\.trop\.zip", rep.text)
    # print(rep.text)
    soup = BeautifulSoup(rep.text, 'html.parser')
    for file in soup.find_all(text=re.compile(r"LOLARDR_.*DAT")):
        urls.append(url + file)
    print("end get ", url)
    return urls

async def download_file(url,es, semaphore):
    async with semaphore:
        print("start download ", url)
        file = url.split("/")[-1]
        dir_ = "I:/data/rdr/co/"
        path = dir_
        file = dir_ + f"{file}"
        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.exists(file):
            print("end download file exist", url)
            return 
        i = 0
        while True:
            i+=1
            if i > 10 :
                print("url maybe not correct:",url)
                break
            try:
                rep = await requests.get(url)
                if rep.status_code == 200:
                    break 
                elif rep.status_code == 400:
                    print("url not found ", url)
                    break 
                else:
                    await asyncio.sleep(1)
                if i > 10 :
                    print("url maybe not correct:",url)
                    break
            except:
                await asyncio.sleep(1)
                continue
        with open(file, "wb") as code:
            code.write(rep.content)
        print("end download ", url)


async def crawl_page(es,s1):
    es = ""
    async with s1:
        base_url = "http://imbrium.mit.edu/DATA/LOLA_RDR/LRO_CO"
        url = base_url + es + "/"
        print("start crawl ", url)
        urls = await asyncio.create_task(get_data_list(url,es))
        tasks = []
        semaphore = asyncio.Semaphore(25)
        for url_ in urls:
            tasks.append(asyncio.create_task(download_file(url_,es, semaphore)))
        await asyncio.gather(*tasks)
        print("end crawl ", url)

async def main():
    # sites = pd.read_csv("./data/sites.csv")
    # sites = open("./data/ztd/sites.csv")
    # print(sites.head())
    s1 = asyncio.Semaphore(5)
    tasks = []
    for es in range(1): # # #
        tasks.append(asyncio.create_task(crawl_page(str(es),s1)))
        # break
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    s1 = asyncio.Semaphore(5)
    asyncio.run(main())