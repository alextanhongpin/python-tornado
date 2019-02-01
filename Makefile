venv:
	# virtualenv -p python3 venv
	# source venv/bin/activate
	# deactivate

install:
	pip3 install -r requirements.txt

freeze:
	pip3 freeze > requirements.txt

start:
	python3 main.py
