apt-get install rsync -y
/etc/init.d/ssh start
/etc/init.d/redis-server start
/etc/init.d/mysql start
python /data/ops/baiwei/manage.py makemigrations
python /data/ops/baiwei/manage.py migrate
python /data/ops/baiwei/manage.py runserver 0.0.0.0:8000
