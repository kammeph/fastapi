#-----------------------------------------------------------
# Clean up
#----------------------------------------------------------------
docker-compose -f docker-compose.dev.yml down
docker image rm -f fastapi || true

#----------------------------------------------------------------
# Start
#----------------------------------------------------------------
docker-compose -f docker-compose.dev.yml up