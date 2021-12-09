import json
import requests


def request_to_api(url , file_path, angle_of_rotation, n):
	files = {'upload_file': open(file_path,'rb')}
	data = {
		"n":n,
		"angle_of_rotation" : angle_of_rotation
	}

	try:
		response_decoded_json = requests.post(url, 
						data=data,
						files=files)
		res = response_decoded_json.json()
		path = res['path']
		
		return path
	except Exception as e:
		return e
	
	
if __name__ == "__main__":
	file_path = 'test_files/dummypdf.pdf'
	n =3
	angle_of_rotation = 90

	url = "http://127.0.0.1:5000/"

	path = request_to_api(url , file_path, angle_of_rotation, n)
	print(path)