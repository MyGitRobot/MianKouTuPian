''' Encoding: UTF-8'''

# If you want to modify this file and publish it, please update the information below.

'''
Source: https://miankoutupian.com/
Author: MrCrawL
Created Time: 2024-02-09
Modified Time: 2024-02-11
Modified by: MrCrawL
'''

from requests import get, post
from re import findall
from hashlib import md5
from time import sleep
from os import makedirs


def miankou(word,num):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    page = 0  # page to download
    data = {  # post data
        'product_id': '53',
        'version_code': '1213',
        'loose': 'false',
        'page': f'{page}',
        'page_size': '30',
        'search_word': word,  # search word
        'scene_type': '13',
        'sort_type': '-1',
        'is_large_scale': '-1',
    }
    o_string = f'is_large_scale={data["is_large_scale"]}&loose={data["loose"]}&page={data["page"]}&page_size={data["page_size"]}&product_id={data["product_id"]}&scene_type={data["scene_type"]}&search_word={word}&sort_type={data["sort_type"]}&version_code={data["version_code"]}&key=d9fd3ec394'  # string to generate sign
    sign = md5(o_string.encode()).hexdigest().upper()  # actually, sign is useless
    data['sign'] = sign  # update sign into data
    url = 'https://wallpaper.soutushenqi.com/api/v1/avoid_cut/list'
    check_download = input('Download all pictures? [y:yes,n:no]:').lower()  # ask whether download pictures
    if check_download=='y':
        makedirs(f'Miankoutupian-{word}',exist_ok=True)  # create a file folder
        print(f'Download soon into Miankoutupian-{word} file folder')
    with open(f'Miankoutupian-{word}.txt', 'w', encoding='utf-8') as f: f.write('')  # initialize pic info txt
    title_list = ['example']
    times_list = [0]
    try:
        while page<int(num):
            res = post(url, headers=headers, data=data).content.decode('utf-8')  # get resource from url
            if len(findall('"data": \[],',res))!=0: break  # if page is excess, stop the loop
            output_title = findall(r'"detailInfo": "([^"]*?)"',res)  # get pic title
            output_url = findall(r'"largeUrl": "([^"]*?)"', res)  # get large pic url
            output_url_thumb = findall(r'"thumbUrl": "([^"]*?)"', res)  # get thumb pic url
            for i in range(len(output_url)):
                with open(f'Miankoutupian-{word}.txt','a',encoding='utf-8') as f:
                    f.write(f'Title:{output_title[i]}\nLargeUrl:{output_url[i]}\nThumbUrl:{output_url_thumb[i]}\n\n')  # update pic info into txt
                if check_download=='y':
                    title = output_title[i].replace("\\","")  # replace illegal file name
                    title = title.replace("|","")
                    title = title.replace("/","")
                    title = title.replace(":","")
                    title = title.replace("*","")
                    title = title.replace("?","")
                    title = title.replace("<","")
                    title = title.replace('"',"")
                    title = title.replace(">","")
                    title = title.strip()[0:50]  # delete blanks, and limit the length
                    if title in title_list:  # avoid the same file name
                        times_list[title_list.index(title)]+=1
                        title = f'{title}({times_list[title_list.index(title)]})'
                    else:
                        title_list.append(title)
                        times_list.append(0)
                    with open(f'Miankoutupian-{word}/{title}.png', 'wb') as p:  # save pictures
                        pic = get(output_url[i], headers=headers)
                        p.write(pic.content)
                    print(f'{title}.png downloaded')
            page+=1
            data['page'] = f'{page}'  # update page into data
            sleep(0.1)
        input('All pictures downloaded!')
    except ValueError:
        input('Retry! Remember the page should be positive integer!')
    except Exception as e:
        input(f'Error:{e}\nRetry please!')


if __name__ == '__main__':
    print('Happy Loong Year!!!')
    miankou(input('Input search word:'),input('Input desired page:'))