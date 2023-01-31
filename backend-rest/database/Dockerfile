FROM postgres

# Copy source
WORKDIR /database

# Change this password for your own needs
ENV POSTGRES_PASSWORD=mM&kRb42GZEEqC
ENV POSTGRES_DB RobotRadarAlpha

#run the PSQL for db creation
COPY flask-user.sql /docker-entrypoint-initdb.d/
#run the PSQL for flaskuser
COPY server-backup.sql /docker-entrypoint-initdb.d/



