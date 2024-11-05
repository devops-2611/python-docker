FROM mysql:latest
ENV MYSQL_ROOT_PASSWORD=admin
ENV MYSQL_DATABASE=attendance_db
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=admin

# SQL script to create the students table
COPY init.sql /docker-entrypoint-initdb.d/
