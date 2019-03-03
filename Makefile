.PHONY: start env

start: # start dev environment
	./env/bin/activate

env: # start docker env
	docker-compose up -d