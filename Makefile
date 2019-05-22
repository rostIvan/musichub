all: help

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

## ---------------------------------------------------------------------------------------------------------------------
## 		Commands
## ---------------------------------------------------------------------------------------------------------------------

ps:			## Show container names, status, ports
	@docker ps --format="table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"

db:			## Open postgres database
	@docker exec -it pg psql -U django -d musichub

rd:			## Open redis-cli
	@docker exec -it rd redis-cli

dbip:			## Show postgres ip address
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' pg

rdip:			## Show redis ip address
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' rd

.ONESHELL:
dockerbash:		## Open bash in container with entered name
	@echo "Container names: "
	@docker ps --format="{{.Names}}"
	@read -p 'Enter container name: ' container_name
	@docker exec -it $$container_name sh -c "export APP_ENVIRONMENT=DOCKER && bash"
