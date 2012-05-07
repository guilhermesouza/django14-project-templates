SETTINGS_DEV='{{ project_name }}.settings.development'
SETTINGS_TESTS='{{ project_name }}.settings.tests'

clean:
        @echo "Cleaning up build and *.pyc..."
        @find . -name '*.pyc' -delete
        @rm -rf build

runserver:
        @python manage.py runserver 0.0.0.0:8000 --settings=${SETTINGS_DEV}

syncdb:
        @python manage.py syncdb --settings=${SETTINGS_DEV}

migrate:
        @python manage.py migrate --settings=${SETTINGS_DEV}

reindex:
        @python manage.py rebuild_index --settings=${SETTINGS_DEV}

test:
        @python manage.py test $(app) --settings=${SETTINGS_TESTS}

test-coverage:
        @python manage.py test_coverage $(app) --settings=${SETTINGS_TESTS}

shell:
        @python manage.py shell --settings=${SETTINGS_DEV}

pep8:
        @pep8 {{ project_name }}/$(app) --exclude=migrations/,manage.py --statistics

compass:
        @compass watch
