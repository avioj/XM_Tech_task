## Orders service Deploy:

1. Install [docker compose](https://docs.docker.com/compose/install/) (tested on version 1.29.2)
2. Make sure that 5000 and 8000 ports are not used
3. Execute `docker-compose up` 
4. Short description of previous command: this command ups both test and backend services, <br />but you could choose which to start by mentioning them)
5. If you use Mac with M1 processor please add ` export DOCKER_DEFAULT_PLATFORM=linux/amd64; ` prefix to docker-compose commands <br />So it would be `export DOCKER_DEFAULT_PLATFORM=linux/amd64; docker-compose up` 
## Orders service Usage:
1. [Tap to see test results once service in deployed](http://127.0.0.1:8000)
2. To communicate with REST api use http://127.0.0.1:8000

## Known bugs: 
1. Something is wrong with quantity field after merging new status into DB (as you can see in test results)
