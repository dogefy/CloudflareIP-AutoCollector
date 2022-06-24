from bs4 import BeautifulSoup
import requests

url = 'https://github.com/ip-scanner/cloudflare'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

result = ''


def get_keywords():
    with open('keys.txt', encoding='utf-8') as f:
        keywords = f.read().split('\n')
    while 1:
        try:
            keywords.remove('')
        except ValueError:
            break
    return keywords


def get_tags():
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
    result_tags = soup.find_all(class_='js-navigation-open Link--primary')
    return result_tags


if __name__ == '__main__':
    keys = get_keywords()
    tags = get_tags()
    count = 0
    for i in tags:
        for j in keys:
            if i['title'].find(j) != -1:
                print(i['title'])
                i['title'] = ''
                count = count + 1
                url_raw = 'https://raw.githubusercontent.com' + i['href'].replace('/blob', '')
                IPs = requests.get(url=url_raw, headers=headers)
                result = result + IPs.content.decode('utf-8')

    with open('ip_result.txt', 'w') as f:
        f.write(result)

    print("Finish! {count} files in total.".format(count=count))
