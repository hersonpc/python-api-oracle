build:
	docker build -t hersonpc/python-api-oracle .

bash:
	docker run -it --rm --name python-oracle -p 8001:8000 hersonpc/python-api-oracle bash

up:
	docker build -t hersonpc/python-api-oracle .
	docker run -it --rm --name python-oracle \
		-p 8008:8000  \
		-e ORACLE_USERNAME='${ORACLE_USERNAME}' \
		-e ORACLE_PASSWORD='${ORACLE_PASSWORD}' \
		-e ORACLE_SERVER='${ORACLE_SERVER}' \
		-e ORACLE_DATABASE='${ORACLE_DATABASE}' \
		hersonpc/python-api-oracle bash

test:
	curl -X 'GET' \
		'http://localhost:8008/unidades_internacao' \
		-H 'accept: application/json'