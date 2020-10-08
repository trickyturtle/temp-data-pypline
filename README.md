# temp-data-pypline
A temperature data pipeline written in python using postgres in a docker container

To create the postgres docker container use:
`docker run -p 5432:5432 --name DATABASE_NAME -e POSTGRES_PASSWORD=postgres postgres`

To monitor, I also spun up a pgadmin docker container like so:
1. `docker run -p 5555:80 --name pgadmin -e PGADMIN_DEFAULT_EMAIL="YOUR_EMAIL@HOTMAIL.COM" -e PGADMIN_DEFAULT_PASSWORD="password" dpage/pgadmin4`

2. Sign into pgadmin using the credentials I set and connect it to the postgres docker container
