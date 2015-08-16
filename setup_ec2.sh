sudo su
yum install update
yum groupinstall "Development Tools"
yum install python-devel
#don't install pip from another source

#http://imperialwicket.com/aws-install-postgresql-on-amazon-linux-quick-and-dirty/
sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs
sudo service postgresql initdb
sudo vim /var/lib/pgsql9/data/pg_hba.conf
sudo vim /var/lib/pgsql9/data/postgresql.conf
sudo service postgresql start
psql -U postgres

pip install psycopg2

#add password to pgpass
chmod 0600 ~/.pgpass