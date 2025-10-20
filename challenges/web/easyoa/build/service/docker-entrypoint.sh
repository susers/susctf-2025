#!/bin/bash

rm -f /docker-entrypoint.sh

mysqld_safe &

mysql_ready() {
	mysqladmin ping --socket=/run/mysqld/mysqld.sock --user=root --password=root >/dev/null 2>&1
}

while ! mysql_ready; do
	echo "waiting for mysql ..."
	sleep 3
done

# Check the environment variables for the flag and assign to INSERT_FLAG
if [ "$GZCTF_FLAG" ]; then
	INSERT_FLAG="$GZCTF_FLAG"
else
	INSERT_FLAG="susctf{testflag}"
fi

echo $INSERT_FLAG >/flag

source /etc/apache2/envvars

echo "Running..." &

tail -F /var/log/apache2/* &

exec apache2 -D FOREGROUND
#!/bin/bash

rm -f /docker-entrypoint.sh

mysqld_safe &

mysql_ready() {
	mysqladmin ping --socket=/run/mysqld/mysqld.sock --user=root --password=root >/dev/null 2>&1
}

while ! mysql_ready; do
	echo "waiting for mysql ..."
	sleep 3
done

# Check the environment variables for the flag and assign to INSERT_FLAG
if [ "$GZCTF_FLAG" ]; then
	INSERT_FLAG="$GZCTF_FLAG"
else
	INSERT_FLAG="susctf{testflag}"
fi

echo $INSERT_FLAG | tee /flag

source /etc/apache2/envvars

echo "Running..." &

tail -F /var/log/apache2/* &

exec apache2 -D FOREGROUND
