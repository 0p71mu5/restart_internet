import requests
import re
import ctypes


s=requests.Session()
# url='http://jiofi.local.html'
url='http://192.168.225.1'
try:
	request=s.post(url+'/cgi-bin/en-jio/login_Query.html', allow_redirects=True, timeout=5)
	token = re.compile(r'","text":"(.*?)"}').findall(request.text)
# 	print(' Login Token - '+token[0])

	payload = {'RequestVerifyToken':token[0], 'act':'administrator', 'pwd':'administrator'}
	request=s.post(url+'/cgi-bin/en-jio/login_check.html', data=payload, allow_redirects=True, timeout=5)

	request=s.get(url+'/cgi-bin/en-jio/mSoftUpdate_Reboot.html', timeout=5)
	token = re.compile(r'name="RequestVerifyToken" value="(.*?)">').findall(request.text)
# 	print(' Reboot Token - '+token[0])

	payload = {'RequestVerifyToken': token[0], 'autoapn':'0', 'apnname':'jionet', 'iptype':'ipv4'}
	request=s.get(url+'/cgi-bin/en-jio/reboot.html', params=payload, timeout=5)

	if 'true' in request.text:
		ctypes.windll.user32.MessageBoxW(0, "JioFi Restart Successful", "JioFi Restart Script", 0)

# except (ValueError,IndexError,TypeError):
except (IndexError):
	print('Index Error Occured')