# temp-data-pypline
A temperature data pipeline written in python using postgres in a docker container.
This was pretty interesting, I'd never built something like this before.

To create the postgres docker container use:
`docker run -p 5432:5432 --name DATABASE_NAME -e POSTGRES_PASSWORD=postgres postgres`

To monitor, I also spun up a pgadmin docker container like so:
1. `docker run -p 5555:80 --name pgadmin -e PGADMIN_DEFAULT_EMAIL="YOUR_EMAIL@HOTMAIL.COM" -e PGADMIN_DEFAULT_PASSWORD="password" dpage/pgadmin4`

2. Sign into pgadmin using the credentials set in the previous step and connect 
it to the postgres docker container

Once you have your postgres docker container running, you will need to add your credentials
to the data_processor.py file (and the unit_test.py file if you want to run them).

To run the pipeline, just run data_pipeline.py. You can also change its NUM_ENTRIES
and NUM_PROCESSES variables to experiment with performance. 

Notes:
1. The logger is not configured, so it isn't as useful as it could be. I typically 
wait to configure it until I know how it will be used in the larger system.

2. I obviously wouldn't normally use the same db for the unit tests and the data
(and I would probably store it in a config file), but I did here just so it's easier 
to play with. You could easily set them up as different dbs. Likewise the `clearTables` 
method would normally be different, I was just trying to improve ease of use for this example.

3. Without multiprocessing, processing and storing 5000 entries takes ~140.95 seconds.

With multiprocessing:

3 processes = ~41.28

4 processes = ~23.4 seconds

6 processes = ~20.05

8 processes = ~15.33