# Due to the weird behavior of either /bin/sh or docker while loading env_vars, I chose to explicitly feed the ip:port combo.
python manage.py migrate && gunicorn "todolist.wsgi:application" -b 0.0.0.0:8000 -w 2 --log-level "info"
# Technically, gunicorn will never exit on its own. So if we get the error code 69 without stopping the container,
# then we know something was wrong With the migration. or gunicorn for that matter.
exit 69