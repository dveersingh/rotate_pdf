import os
import uuid

from flask import Flask, jsonify, request
#from werkzeug.utils import secure_filename
import PyPDF2
  
# creating a Flask app
app = Flask(__name__)

UPLOAD_FOLDER = 'upload/'  # upload folder
RESULT_FOLDER = 'rotated/' # otput folder

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER']  = RESULT_FOLDER

def rotate_pdf(file, angle_of_rotation , n ):
	output_path = "some error 404"
	try:
		filename = app.config['UPLOAD_FOLDER']+file
		pdf_in = open(filename, 'rb') # read pdf file
		pdf_reader = PyPDF2.PdfFileReader(pdf_in)
		pdf_writer = PyPDF2.PdfFileWriter()

		for pagenum in range(pdf_reader.numPages):
			page = pdf_reader.getPage(pagenum)
			if pagenum < n:
			# this conditon will rotate 0 to n-1 pages that is  1 to n.
				page.rotateClockwise(angle_of_rotation)
			pdf_writer.addPage(page)
			
		output_path = app.config['RESULT_FOLDER'] +file
		#defining output folder that is 'rotated/'
		pdf_out = open(output_path, 'wb')
		pdf_writer.write(pdf_out)
		pdf_out.close()
		pdf_in.close()
		#rotated pdf saved
	except Exception as e:
		print(e)
		pass
		
	return output_path

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	try:
		angle_of_rotation = int(request.form.get('angle_of_rotation'))
		n = int(request.form.get('n'))
		#fetthing json data
		file = request.files['upload_file']
		#fetchingh file
		filename = str(uuid.uuid4())+".pdf"
		#unique id for every upload
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#saving file to upload folder
		rotate_file = rotate_pdf(filename, angle_of_rotation,n)
		#calling function to rotate
		
		return jsonify({'path':rotate_file })
	except Exception as e:
		return jsonify({"path": "error in upload file function: "+e})
	 

if __name__ == '__main__':
  
	app.run(debug = True, port = 5000)