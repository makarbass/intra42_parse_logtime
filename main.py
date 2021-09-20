import requests
from bs4 import BeautifulSoup
import getpass

login = input("Введите логин: ").strip()
password = getpass.getpass("Введите пароль: ")
print('Ожидайте...')
url_login = 'https://signin.intra.42.fr/users/sign_in/'
url_main = 'https://profile.intra.42.fr/users/'+login+'/locations_stats'

client = requests.session()
html = client.get(url_login)
soup = BeautifulSoup(html.text, 'lxml')
token = soup.find('input', dict(name='authenticity_token'))['value']

data = {
	'utf8': '✓',
	'authenticity_token': token,
	'user[login]': login,
	'user[password]': password,
	'commit': 'Sign+in',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)  Safari/537.36',
    'Referer': url_main,
    'Connection': 'keep-alive',
}
r = client.post(url_login, data=data, headers=headers)
content = client.get(url_main).json()

f = open('stats.txt', 'a+')
for i in content:
	date = i.split('-')
	time = (content[i].split('.'))
	f.write('Дата: '+date[2]+'.'+date[1]+'.'+date[0]+', количество времени: '+time[0]+'\n')
f.close()
print("Файл stats.txt обновлен")