import requests
import json
import os
import time
import datetime
import zipfile
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
session = requests.Session()
iw_url = config['infowatch']['url']
iw_user = config['infowatch']['username']
iw_pass = config['infowatch']['password']
query_id = config['infowatch']['query_id'] # ID запроса на получение событий
rv_url = config['rvision']['url']
rv_api = config['rvision']['key']

headers = {
	'Host': iw_url,
	'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="98"',
	'X-Requested-With': 'XMLHttpRequest',
	'Sec-Ch-Ua-Mobile': '?0',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
	'Sec-Ch-Ua-Platform': '"Windows"',
	'Sec-Fetch-Site': 'same-origin',
	'Sec-Fetch-Mode': 'cors',
	'Sec-Fetch-Dest': 'empty',
	'Referer': f"https://{iw_url}/",
	'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
	'Connection': 'close',
	}

def get_cookie():
	'''Получение cookie'''
	url = f"https://{iw_url}/api/checkVersion"
	payload={}
	response = session.get(url,verify=False, headers=headers, data=payload)

def get_salt():
	'''Получение токена'''
	url = f"https://{iw_url}/api/salt"
	payload={}
	response = session.get(url,verify=False, headers=headers, data=payload)
	return response.headers['X-CSRF-Token']

def auth(token):
	'''Аутентификация'''
	global headers
	url = f"https://{iw_url}/api/login"
	payload = '{\"username\":\"' + iw_user + '\",\"password\":\"' + iw_pass + '\"}'
	headers.update({'X-Csrf-Token':token})
	response = session.get(url,verify=False, headers=headers, data=payload)
	return 0

def execute_query(token, query_id=query_id):
	'''Запрос на выполнение преднастроенной выборки событий'''

	url = f"https://{iw_url}/api/query/{query_id}/execute"
	payload = ""
	response = session.post(url, verify=False, headers=headers, data=payload)
	return 0

def get_messages_by_query(token, query_id=query_id):
	'''Запрос на получение событий из выборки'''
	# тут можно настроить сколько событий забирать, для этого поменяйте значения start и limit в url
	url = f"https://{iw_url}/api/object?start=0&limit=10000&merge_with[]=objectContentFilenames&&sort%5BOBJECT_ID%5D=asc&filter%5BQUERY_ID%5D=" + str(query_id)
	response = session.get(url, verify=False, headers=headers)
	return json.loads(response.text)["data"]

def send_event(payload):
	'''Отправка события в R-Vision'''	
	url = f"https://{rv_url}/api/v2/incidents"
	session = requests.Session()
	session.trust_env = False
	resp = session.post(url,verify = False, data=payload)
	return resp.text


def copy_event(event):
	'''Обработка событий категории копирование'''

	''' Добавьте сюда необходимые операции для обработки событий категории копирование '''

	id = event['OBJECT_ID'] 
	payload = {
		'token': rv_api,
		'company': 'Филиал 1',
		'category': 'Копирование чувствительной информации',
		'infowatch_id':id,
	}
	return send_event(payload)

def crawler_event(event):
	'''Обработка событий категории хранение'''

	''' Добавьте сюда необходимые операции для обработки событий категории хранение '''

	id = event['OBJECT_ID'] 
	payload = {
		'token': rv_api,
		'company': 'Филиал 1',
		'category': 'Хранение чувствительной информации в неположенном месте',
		'infowatch_id':id,
	}
	return send_event(payload)

def transfer_event(event):
	'''Обработка событий категории передача'''

	''' Добавьте сюда необходимые операции для обработки событий категории передача '''

	id = event['OBJECT_ID'] 
	payload = {
		'token': rv_api,
		'company': 'Филиал 1',
		'category': 'Передача чувствительной информации',
		'infowatch_id':id,
	}
	return send_event(payload)

def get_report(obj_id, query_id, token):
	'''Запрос на формирование отчета'''

	url = f"https://{iw_url}/api/object/report"
	payload = "{\r\n    \"QUERY_ID\":" + str(query_id) + ",\r\n    \"DISPLAY_NAME\": \"Report\",\r\n    \"FILTER\": {},\r\n    \"SORT\": {\r\n        \"OBJECT_ID\": \"asc\"\r\n    },\r\n    \"IS_ONE_REPORT\": 0,\r\n    \"FORMAT\": \"full\",\r\n    \"TYPE\": {\r\n        \"one_report\": \"docx\",\r\n        \"several_report\": \"docx\"\r\n    },\r\n    \"IS_SEVERAL_REPORT\": 1,\r\n    \"LOAD_ATTACHMENT\": 0,\r\n    \"KEEP_HIERARCHY\": 0,\r\n    \"SEVERAL_LOAD_REPORT\": 1,\r\n    \"LOAD_SNIPPET\": 1,\r\n    \"LOAD_EML\": 0,\r\n    \"LOAD_DEBUG_OBJECT\": 0,\r\n    \"SCOPE\": \r\n" + str(obj_id) + "\r\n    \r\n}"
	response = session.post(url, headers=headers, verify = False, data=payload)
	return json.loads(response.text)["data"]["REPORT_ID"]

def take_ready_report(report_id,token):
	'''Запрос на получение отчета'''

	url = f"https://{iw_url}/api/object/reportFile?report_id={report_id}"
	response = session.get(url, headers=headers, verify = False,data=payload)
	with open('Отчет по инциденту.zip','wb') as file:
		file.write(response.content)
		file.close()
	with zipfile.ZipFile('Отчет по инциденту.zip', 'r') as zip_ref:
		zip_ref.extractall('./extracted')
	return 0

def get_last_id():
	'''Получение id последнего обработанного события'''

	list = []
	file = read_last_id()
	for line in file:
		try:
			list.append(int(line.split('\n')[0]))
		except:
			pass
	return list

def write_last_id(id):
	'''Запись последнего id события'''

	with open(os.path.dirname(os.path.abspath(__file__)) + '/last_created_id.txt', "a") as f:
		f.write(id)

def read_last_id():
	'''Чтение последнего id события'''

	file =  open(os.path.dirname(os.path.abspath(__file__)) + '/last_created_id.txt', "r")
	return file

def get_json(event):
	'''Формирование JSON-файла события'''

	filename = f"{event['OBJECT_ID']}.json"
	with open(filename, 'w') as outfile:
		json.dump(event, outfile)
	return 0

def processing_events(events,token):
	'''Функция обработки событий'''

	for event in events:
		id = event['OBJECT_ID']
		if int(id) not in get_last_id():
			try:
				rep_id = get_report(id, query_id, token) # id выгружаемого отчета
			except:
				write_to_log(f"Ошибка при запросе отчета. Инцидент: {id}")
			try:
				if event['RULE_GROUP_TYPE'] == "Transfer":
					transfer_event(event)	
				elif event['RULE_GROUP_TYPE'] == "Copy":
					copy_event(event)	
				elif event['RULE_GROUP_TYPE'] == "Placement":
					crawler_event(event)
				else:
					write_to_log(f"Незвестный тип инцидента {id} --> {event['RULE_GROUP_TYPE']}")
				os.system(f"mkdir {id}")
				os.system(f"mkdir '{id}/1. Обнаруженные материалы'")
				write_last_id(str(id) + '\n')
			except Exception as e:
				write_to_log(f"Инцидент {id} не обработан, ошибка: {e}")	
			try:
				get_json(event)
				os.system(f"cp {id}.json '{id}/1. Обнаруженные материалы/Отчет по инциденту {id}.json'")
			except:
				write_to_log(f"Ошибка при получении отчета. Инцидент: {id}")
			try:
				take_ready_report(rep_id,token)
				os.system(f"mv './extracted/ID_/ID_{id}.docx' '{id}/1. Обнаруженные материалы/Отчет по инциденту {id}.docx'")
			except Exception as e:
				write_to_log(f"Ошибка {e} при обращении за готовым отчетом. Инцидент: {id}")
		else:
			pass
	return 0

def write_to_log(err):
	'''Логирование'''

	print(str(err))
	file = open("log.txt",'a')
	file.write(str(datetime.datetime.now()) + " " +  str(err) + '\n')
	return 0

def main():
	'''Основная функция'''

	while True:
		try:
			get_cookie()
			token = get_salt()
			auth(token)
		except Exception as err:
			write_to_log(f"Ошибка авторизации: {err}")
		try:
			execute_query(token,query_id)
			time.sleep(10)
		except Exception as err:
			write_to_log(f"InfoWatch недоступен: {err}")
		try:
			events = get_messages_by_query(token,query_id)
		except Exception as err:
			write_to_log(f"Нет событий: {err}")
		try:
			processing_events(events,token)
			time.sleep(100)
		except Exception as err:
			write_to_log(f"Ошибка обработки событий: {err}")
main()