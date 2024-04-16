# -*- coding: utf-8 -*-

"""
Source: https://miankoutupian.com/
Program: MianKouTuPian Downloader
Author: MrCrawL
Created Time: 2024-02-09
Last Modified: 2024-04-16
Modified by: MrCrawL
PS. 2024-04-16: Improved code format, or... refactor code
"""
# If you want to modify this file and publish it, please update the information above.

from requests import get, post
from re import findall
from hashlib import md5
from time import sleep
from os import makedirs
import logging

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}


# def miankou(word,num):
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
#     page = 0  # page to download
#     data = {  # post data
#         'product_id': '53',
#         'version_code': '1213',
#         'loose': 'false',
#         'page': f'{page}',
#         'page_size': '30',
#         'search_word': word,  # search word
#         'scene_type': '13',
#         'sort_type': '-1',
#         'is_large_scale': '-1',
#     }
#     o_string = f'is_large_scale={data["is_large_scale"]}&loose={data["loose"]}&page={data["page"]}&page_size={data["page_size"]}&product_id={data["product_id"]}&scene_type={data["scene_type"]}&search_word={word}&sort_type={data["sort_type"]}&version_code={data["version_code"]}&key=d9fd3ec394'  # string to generate sign
#     sign = md5(o_string.encode()).hexdigest().upper()  # actually, sign is useless
#     data['sign'] = sign  # update sign into data
#     url = 'https://wallpaper.soutushenqi.com/api/v1/avoid_cut/list'
#     check_download = input('Download all pictures? [y:yes,n:no]:').lower()  # ask whether download pictures
#     if check_download=='y':
#         makedirs(f'Miankoutupian-{word}',exist_ok=True)  # create a file folder
#         print(f'Download soon into Miankoutupian-{word} file folder')
#     with open(f'Miankoutupian-{word}.txt', 'w', encoding='utf-8') as f: f.write('')  # initialize pic info txt
#     title_list = ['example']
#     times_list = [0]
#     try:
#         while page<int(num):
#             res = post(url, headers=headers, data=data).content.decode('utf-8')  # get resource from url
#             if len(findall('"data": \[],',res))!=0: break  # if page is excess, stop the loop
#             output_title = findall(r'"detailInfo": "([^"]*?)"',res)  # get pic title
#             output_url = findall(r'"largeUrl": "([^"]*?)"', res)  # get large pic url
#             output_url_thumb = findall(r'"thumbUrl": "([^"]*?)"', res)  # get thumb pic url
#             for i in range(len(output_url)):
#                 with open(f'Miankoutupian-{word}.txt','a',encoding='utf-8') as f:
#                     f.write(f'Title:{output_title[i]}\nLargeUrl:{output_url[i]}\nThumbUrl:{output_url_thumb[i]}\n\n')  # update pic info into txt
#                 if check_download=='y':
#                     title = output_title[i].replace("\\","")  # replace illegal file name
#                     title = title.replace("|","")
#                     title = title.replace("/","")
#                     title = title.replace(":","")
#                     title = title.replace("*","")
#                     title = title.replace("?","")
#                     title = title.replace("<","")
#                     title = title.replace('"',"")
#                     title = title.replace(">","")
#                     title = title.strip()[0:50]  # delete blanks, and limit the length
#                     if title in title_list:  # avoid the same file name
#                         times_list[title_list.index(title)]+=1
#                         title = f'{title}({times_list[title_list.index(title)]})'
#                     else:
#                         title_list.append(title)
#                         times_list.append(0)
#                     with open(f'Miankoutupian-{word}/{title}.png', 'wb') as p:  # save pictures
#                         pic = get(output_url[i], headers=headers)
#                         p.write(pic.content)
#                     print(f'{title}.png downloaded')
#             page+=1
#             data['page'] = f'{page}'  # update page into data
#             sleep(0.1)
#         input('All pictures downloaded!')
#     except ValueError:
#         input('Retry! Remember the page should be positive integer!')
#     except Exception as e:
#         input(f'Error:{e}\nRetry please!')


class MianKou:

    def __init__(self, search_words:str, download_pages:int):
        """
        Download picture info or png through miankoutupian.com
        :param search_words: search words through miankoutupian.com
        :param download_pages: total pages to download/save
        """
        self.words = search_words
        self.num = download_pages
        self.page = 0  # current page to download
        self.url = 'https://wallpaper.soutushenqi.com/api/v1/avoid_cut/list'
        self.data = {
            'product_id': '53',
            'version_code': '1213',
            'loose': 'false',
            'page': self.page,
            'page_size': '30',
            'search_word': self.words,
            'scene_type': '13',
            'sort_type': '-1',
            'is_large_scale': '-1',
        }
        self.check_download = None

    def _get_sign(self):
        o_string = (f'is_large_scale={self.data["is_large_scale"]}&loose={self.data["loose"]}&page={self.data["page"]}'
                    f'&page_size={self.data["page_size"]}&product_id={self.data["product_id"]}'
                    f'&scene_type={self.data["scene_type"]}&search_word={self.words}&sort_type={self.data["sort_type"]}'
                    f'&version_code={self.data["version_code"]}&key=d9fd3ec394')  # string to generate sign
        sign = md5(o_string.encode()).hexdigest().upper()  # actually, sign is useless
        self.data['sign'] = sign  # update sign into data

    def _check_download(self):
        self.check_download = input('Download all pictures? [y/n]:').lower()  # ask whether download pictures
        with open(f'Miankoutupian-{self.words}.txt', 'w', encoding='utf-8') as f: f.write('')  # initialize pic info txt
        if self.check_download == 'y' or self.check_download == '':
            self.check_download = True
            makedirs(f'Miankoutupian-{self.words}', exist_ok=True)  # create a file folder
            print(f'[Info] Download soon into Miankoutupian-{self.words} file folder')

    def _download_info(self):
        while self.page < self.num:
            res = post(self.url, headers=headers, data=self.data).content.decode('utf-8')  # get resource from url
            if len(findall('"data": \[],', res)) != 0: break  # if page is excess, stop the loop
            output_title = findall(r'"detailInfo": "([^"]*?)"', res)  # get pic title
            self.output_url = findall(r'"largeUrl": "([^"]*?)"', res)  # get large pic url
            output_url_thumb = findall(r'"thumbUrl": "([^"]*?)"', res)  # get thumb pic url
            for i in range(len(self.output_url)):
                with open(f'Miankoutupian-{self.words}.txt', 'a', encoding='utf-8') as f:
                    f.write(f'Title:{output_title[i]}\nLargeUrl:{self.output_url[i]}\n'
                            f'ThumbUrl:{output_url_thumb[i]}\n\n')  # update pic info into txt
                if self.check_download:
                    self._download_picture(output_title, i)
            self.page += 1
            self.data['page'] = self.page  # update page into data
            sleep(0.1)

    def _download_picture(self, output_title:list, index:int):
        title_list = ['example']
        times_list = [0]
        title = output_title[index].replace("\\", "")  # replace illegal file name
        tmp_ls = ['|', '/', ':', '*', '?', '<', '"', '>']
        for ele in tmp_ls: title = title.replace(ele, '')  # clear illegal characters
        title = title.strip()[0:50]  # delete blanks, and limit the length
        if title in title_list:  # avoid the same file name
            times_list[title_list.index(title)] += 1
            title = f'{title}({times_list[title_list.index(title)]})'
        else:
            title_list.append(title)
            times_list.append(0)
        with open(f'Miankoutupian-{self.words}/{title}.png', 'wb') as p:  # save pictures
            pic = get(self.output_url[index], headers=headers)
            p.write(pic.content)
        print(f'[Info] {title}.png downloaded')

    def download(self):
        self._check_download()
        self._get_sign()
        self._download_info()
        input('[Info] All pictures downloaded! Press <Enter> to exit...')


def error_logging(error:Exception):
    print(f'[Error] {error} recorded.')
    logging.basicConfig(filename='error.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.ERROR,
                        encoding='utf-8')
    logging.error(f"Error occurred: {error}", exc_info=True)


def check_digit(pages:str):
    if pages.isdigit():
        return int(pages)
    else:
        return False


def download_process(words:str, pages:str):
    page = check_digit(pages)
    if page:
        miankou = MianKou(words, page)
        miankou.download()
    else:
        page = input('>>> Please input correct pages: ')
        download_process(words, page)


def main():
    print('Happy Loong Year!!!')
    # miankou(input('Input search word:'), input('Input desired page:'))
    words = input('>>> Input search words: ')
    pages = input('>>> Input download pages: ')
    download_process(words, pages)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        error_logging(e)
