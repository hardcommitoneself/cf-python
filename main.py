import os
from subprocess import Popen, run , PIPE, STDOUT
import shutil
import random
import string
import time
from traceback import print_tb
import requests

links = []

# def authenticate_account(email_account,key_account):
# 	# wrangler config is deprecated
# 	p = Popen(['wrangler', 'login'], shell=True , stdout=PIPE, stdin=PIPE, stderr=STDOUT)
# 	p.communicate()[0]


def deauthenticate_account():
	p = Popen(['wrangler', 'logout'], shell=True , stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	p.communicate(input=b'Y\n')[0]


def publish_script():
	global links
	p = Popen(['CLOUDFLARE_ACCOUNT_ID=881c45a878f8aa734e28528df2c5bd25', 'CLOUDFLARE_API_TOKEN=YeUKdQvcCnB27YloWSPiXT8EOZCkLeqrcdScCNBV', 'wrangler', 'publish', 'index.js'], shell=True , stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	(output, err) = p.communicate()
	print(f'{output}')
	if "https://" in output.decode():
		links.append("https://" + output.decode().split("https://")[1][:-2])

def test_run():
	p = Popen(['CLOUDFLARE_ACCOUNT_ID=881c45a878f8aa734e28528df2c5bd25', 'CLOUDFLARE_API_TOKEN=YeUKdQvcCnB27YloWSPiXT8EOZCkLeqrcdScCNBV', 'wrangler', 'publish', 'index.js'], shell=True , stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	(output, errors) = p.communicate()
	print(f'{output}')


def random_string_alpha(length):
	choices = string.ascii_lowercase
	return "".join(random.choices(choices, k=length))


def random_string_numbers(length):
	choices = string.digits
	return "".join(random.choices(choices, k=length))


def random_string_full(length):
	choices = string.ascii_lowercase + string.digits
	return "".join(random.choices(choices, k=length))


def main():
	test_run()

	return

	global links
	with open("license.txt","r+") as license:
		key = license.read().splitlines()[0]
		res = requests.get(f'https://owlshop.one/verify_key/{key}')
		if not res or res.json()["status"] != 'ok':
			print("invalid license")
			time.sleep(5)
			exit()
	accounts = []
	with open("accounts.txt","r+") as acc:
		accounts_data = acc.read().splitlines()
		for account in accounts_data:
			accounts.append(account)
	count = int(input("how many links you want from each account : "))
	is_custom = input("You Want To Use custom.txt File ? (Y/N): ")
	workerNames = []
	if is_custom.lower() == "y":
		with open("custom.txt", "r") as f:
			workerNames = f.read().splitlines()
	else:
		for i in range(int(count)):
			workerNames.append(random_string_alpha(random.randint(5,10)) + "-" + random_string_numbers(random.randint(5,10)))
	if count>len(workerNames):
		count = len(workerNames)
	for account in accounts:
		# authenticate_account(email_account=account.split(":")[0],key_account=account.split(":")[1])
		links = []
		for i in range(count):
			workerName = workerNames[i]
			os.mkdir(workerName)
			#os.mkdir(f'{workerName}/node_modules')
			print(f'[+]Made Repo: {workerName}')
			os.system(f'copy package.json {workerName}')
			os.system(f'copy package-lock.json {workerName}')
			#os.system(f'xcopy node_modules "{workerName}node_modules" /s /e /h')
			shutil.copytree('node_modules', f'{workerName}/node_modules')
			os.system(f'copy index.js {workerName}')

			with open(f"{workerName}/wrangler.toml", "w") as f:
				f.write(f"""name = "{workerName}"
			workers_dev = true
			compatibility_date = "" """)

			with open("index.html", errors='ignore') as f:
				html = f.read()

			with open(f"{workerName}/index.js", "w") as f:
				f.write("""const html = `""" + html + """`
			async function handleRequest(request) {
			return new Response(html, {
			headers: {
				"content-type": "text/html;charset=UTF-8",
			},
			})
			}

			addEventListener("fetch", event => {
			return event.respondWith(handleRequest(event.request))
			})
			""")
			os.chdir(workerName)
			publish_script()
			os.chdir('../')
			# os.system(f'rmdir /Q /S {workerName}')
			print('[+]Done')
			print("_"*30)
		
		for link in links:
			print(f'{link}')

if __name__ == "__main__":
	main()

