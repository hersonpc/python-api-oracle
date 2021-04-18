build:
	docker build -t hersonpc/python-api-oracle .

bash:
	docker run -it --rm --name python-oracle hersonpc/python-api-oracle bash