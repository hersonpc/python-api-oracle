build:
	docker build -t hersonpc/python-api-oracle .

prod:
	docker build --no-cache -t hersonpc/python-api-oracle .

bash:
	docker run -it --rm --name python-oracle -p 8001:8000 hersonpc/python-api-oracle bash

up:
	echo Running containers
	docker-compose up -d

down:
	echo Stopping containers in execution
	docker-compose down

console:
	echo Accessing bash in running container
	clear
	docker exec -it api_core bash

logs:
	echo Accessing logs of running container
	docker-compose logs -f --tail=30

test:
	curl -X 'GET' \
		'http://localhost:8008/unidades_internacao' \
		-H 'accept: application/json'

env:
	cp .env.example .env	