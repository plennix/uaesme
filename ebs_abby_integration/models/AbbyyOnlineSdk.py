#!/usr/bin/python

# Usage: process.py <input file> <output file> [-l <Language>] [-pdf|-txt|-rtf|-docx|-xml]

import shutil

import xml.dom.minidom
try:
	import requests
except ImportError:
	print("You need the requests library to be installed in order to use this sample.")
	print("Run 'pip install requests' to fix it.")

	exit()


class ProcessingSettings:
	Language = "English"
	OutputFormat = "xml"


class Task:
	Status = "Unknown"
	Id = None
	DownloadUrl = None

	def is_active(self):
		if self.Status == "InProgress" or self.Status == "Queued":
			return True
		else:
			return False


class AbbyyOnlineSdk:
	# Warning! This is for easier out-of-the box usage of the sample only. Change to https:// for production use
	# Change to http://cloud-westus.ocrsdk.com if you created your application in US location
	# serverUrl="";
	# applicationId=""
	# password=""
	Proxies = {}
	def AbbyOnlineSdk(self,serverUrl,applicationId,password):

		self.ServerUrl = serverUrl
		self.ApplicationId = applicationId
		self.Password = password
		return self.ServerUrl,self.ApplicationId,self.Password

		# print(self.ServerUrl)
		# print(self.ApplicationId)
		# print(self.Password)
		# exit()


	# To create an application and obtain a password,
	# register at https://cloud.ocrsdk.com/Account/Register
	# More info on getting your application id and password at
	# https://ocrsdk.com/documentation/faq/#faq3
	# ServerUrl = "http://cloud-eu.ocrsdk.com/"
	# ApplicationId = "081b1b43-5a53-469f-9ef5-de96ec687ae5"
	# Password = "xgghw3ATJglkTWn0nw0upckw"
	# Proxies = {}


	def process_image(self, img, settings,serverUrl,applicationId,password):
		url_params = {
			"language": settings.Language,
			"exportFormat": settings.OutputFormat
		}
		request_url = self.get_request_url("processBusinessCard",serverUrl)
		print(serverUrl)
		print(request_url)
		#exit()

		# with open(file_path, 'rb') as image_file:
		# 	image_data = image_file.read()

		response = requests.post(request_url, data=img, params=url_params,
								 auth=(applicationId, password), proxies=self.Proxies)
		print("ana hon")

		# Any response other than HTTP 200 means error - in this case exception will be thrown
		response.raise_for_status()

		# parse response xml and extract task ID
		task = self.decode_response(response.text)
		return task

	def get_task_status(self, task,server_url):
		if task.Id.find('00000000-0') != -1:
			# GUID_NULL is being passed. This may be caused by a logical error in the calling code
			print("Null task id passed")
			return None

		url_params = {"taskId": task.Id}
		status_url = self.get_request_url("getTaskStatus",server_url)

		response = requests.get(status_url, params=url_params,
								auth=(self.ApplicationId, self.Password), proxies=self.Proxies)
		task = self.decode_response(response.text)
		return task

	def download_result(self, task, output_path):
		get_result_url = task.DownloadUrl
		if get_result_url is None:
			print("No download URL found")
			return

		file_response = requests.get(get_result_url, stream=True, proxies=self.Proxies)
		#print(file_response.raw)
		#exit()
		with open(output_path, 'wb') as output_file:
			shutil.copyfileobj(file_response.raw, output_file)

	def decode_response(self, xml_response):
		""" Decode xml response of the server. Return Task object """
		dom = xml.dom.minidom.parseString(xml_response)
		task_node = dom.getElementsByTagName("task")[0]
		task = Task()
		task.Id = task_node.getAttribute("id")
		task.Status = task_node.getAttribute("status")
		if task.Status == "Completed":
			task.DownloadUrl = task_node.getAttribute("resultUrl")
		return task

	def get_request_url(self, url,serverUrl):

		print(serverUrl.strip('/') + '/' + url.strip('/'))
		#exit()

		return serverUrl.strip('/') + '/' + url.strip('/')
