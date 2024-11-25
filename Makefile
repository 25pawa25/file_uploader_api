# Wake up docker containers
up:
	docker-compose -f docker-compose.yml up -d

# Shut down docker containers
down:
	docker-compose -f docker-compose.yml down

# Start tests in container
test-user-check:
	docker-compose -f docker-compose.yml exec -e DEBUG=True test_auth sh -c "cd .. && pytest -vv -s tests/test_GRPCAsyncServerUserExisting.py"


# Show logs of each container
logs:
	docker-compose -f docker-compose.yml logs

# Restart all containers
restart: down up

# Build and up docker containers
build:
	docker-compose -f docker-compose.yml build --force-rm

# Build and up docker containers
rebuild:  build up
