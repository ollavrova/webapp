MANAGE=django-admin.py
ROOT_DIR=`pwd`

test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=webapp.settings $(MANAGE) test app

run:
	. $(ROOT_DIR)/venv/bin/activate; PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=webapp.settings $(MANAGE) runserver

migrate:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=webapp.settings $(MANAGE) migrate --noinput


install:
	virtualenv --no-site-packages venv
	. $(ROOT_DIR)/venv/bin/activate; pip install -r $(ROOT_DIR)/requirements.txt
	. $(ROOT_DIR)/venv/bin/activate; make syncdb
