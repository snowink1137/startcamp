import requests


# MY_CHAT_ID = '684937471'
# BOT_TOKEN = '754774178:AAFSpv4g3FAC5Yw1jExcBKcJHH6Kac6z5Pk'
# msg = 'Happy Hacking'
# url = 'https://api.hphk.io/telegram/bot{}/sendMessage?chat_id={}&text={}'.format(BOT_TOKEN, MY_CHAT_ID, msg)

# response = requests.get(url)
# print(response.json())

def send_message(CHAT_ID, msg, BOT_TOKEN='754774178:AAFSpv4g3FAC5Yw1jExcBKcJHH6Kac6z5Pk'):
    url = 'https://api.hphk.io/telegram/bot{}/sendMessage?chat_id={}&text={}'.format(BOT_TOKEN, CHAT_ID, msg)
    response = requests.get(url)
    
    
