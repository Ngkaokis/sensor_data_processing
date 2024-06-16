cp .env.example .env
docker-compose build
docker-compose up -d db
sleep 10 # Wait pg to init
make upgrade-db
