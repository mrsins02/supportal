FROM postgres:16

RUN echo "listen_addresses='*'" >> /var/lib/postgresql/data/postgresql.conf
RUN echo "# TYPE  DATABASE        USER            ADDRESS                 METHOD\
\
# Allow access from other servers\
host    all             all             0.0.0.0/0               md5\
\
# For IPv6:\
host    all             all             ::/0                    md5\
\
# Local connections (localhost)\
local   all             all                                     trust\
host    all             all             127.0.0.1/32            trust\
host    all             all             ::1/128                 trust" > /var/lib/postgresql/data/pg_hba.conf