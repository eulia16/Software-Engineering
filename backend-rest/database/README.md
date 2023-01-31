# Database
The SQL in this `server-backup.sql` is meant to be run by PSQL - it will not work as 
standard SQL syntax. 

`flask-user.sql` establishes the user to be used by the Flask endpoints.  It needs to be run 
before `server-backup.sql`.  You will get errors otherwise.

Be sure to update `backup-server.sql` when the schema changes.

## When Updating
Right-click the DB to be backed up, select `Backup`, choose the file name and
location, then change the format to `Plain`.  This is very important because
otherwise it will spit out a bunch of gibberish. 

## To Build Locally
In pgAdmin 4:
- Select the DB to update, or create a new one and name it `RobotRadarAlpha`
- Open up `PSQL Tool` from the `Tools` menu
- Copy and paste the contents of the `.sql` files into the shell
  - `flask-user.sql` needs to be run before `server-backup.sql`

## Docker Guide 
1. Run `docker build -t robot-radar-db .`
(NOTE: the ending period is very important do not forget)
2. Run: `docker run -p 36000:5432 -d robot-radar-db`

### To use Postgres:
1. Run `docker exec -it <container-name> bash`
2. Run `psql -U postgres`

Be sure to restart the container so that the database service
starts after initialization.

You can make sure the tables were created by switching to the `RobotRadarAlpha`
database (run `\connect RobotRadarAlpha`) and running `\dt` while in the PSQL shell.

To view columns, use `\d+ <table name>`.

Use `\qt` to exit PSQL and then `exit` to exit bash.

To get the Docker container's IP:
`docker container inspect -f '{{ .NetworkSettings.IPAddress }}' <container name>`

### Removing Docker Images from remote
SSH in first.
#### Remove Container
For each container:
1. Run `docker ps`, get the id or the container name
2. Run `docker stop <container id or name>`
3. Run `docker rm <container id or name>`

#### Remove Image
1. Run `docker image rm robot-radar-db`
2. Run `docker image rm flask-app-backend`

### Deployment
Create the images locally following this readme and the backend-rest readme, then:
1. Run `docker save --output robot-radar-db.tar robot-radar-db`.  This outputs the
Postgres DB into a `.tar` to be loaded onto remote.
2. Run `docker save --output flask-app-backend.tar flask-app-backend`.  Same deal
but for the Flask app.
3. SSH into remote and create a directory called `robotradar`
   - If the `.tar` files already exist in this directory, cd in and delete them with `rm robot-radar-db.tar` and `rm flask-app-backend.tar`
4. Return to terminal, enter `scp robot-radar-db.tar <user>@remote<REMOTE IP>:/home/<user>/robotradar`
and follow the prompts.  Wait for the upload to finish.
5. Enter `scp flask-app-backend.tar <user>@remote<REMOTE IP>:/home/<user>/robotradar`
and follow the prompts.  Wait for the upload to finish.
6. Return to SSH terminal, enter `docker load --input robot-radar-db.tar`
7. Enter `docker load --input flask-app-backend.tar`
8. Run `docker run -dp 36000:5432 robot-radar-db`, then `docker ps` and get the container ID or name
9. Wait a bit then run `docker start <container id or name>` to restart the DB
10. Follow the instructions in the `To use Postgres` section to verify the tables 
were created correctly.
11. Run `docker run -p 9823:5000 -d flask-app-backend`
12. Hit `http://remote<REMOTE IP>:9823/logs?password=<password>&remote=True` in either Postman or your
browser.  If it works, everything built correctly!