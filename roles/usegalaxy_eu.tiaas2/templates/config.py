GALAXY_SECRET = "{{ tiaas_galaxy_idsecret }}"
TIAAS_OWNER = '{{ tiaas_info.owner }}'
TIAAS_EMAIL = '{{ tiaas_info.owner_email }}'
TIAAS_OWNER_SITE = '{{ tiaas_info.owner_site }}'
TIAAS_DOMAIN = '{{ tiaas_info.domain }}'

TIAAS_SEND_EMAIL_TO = '{{ tiaas_info.owner_email }}'
TIAAS_SEND_EMAIL_FROM = "tiaas+noreply@example.org"

TIAAS_GDPR_RETAIN_EXTRA = {{ retain_extra_time }}  # months (int)

DEBUG = {{ tiaas_debug | default('False') }}

DATABASES = {
    {% if tiaas_tiaas_use_sqlite %}
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '{{ tiaas_dir }}/db.sqlite3',
    },
    {% else %}
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ tiaas_tiaas_db_name }}',
        'USER': '{{ tiaas_tiaas_db_user }}',
        'PASSWORD': '{{ tiaas_tiaas_db_pass }}',
        'HOST': '{{ tiaas_tiaas_db_host }}',
        'PORT': '{{ tiaas_tiaas_db_port }}',
    },
    {% endif %}
    'galaxy': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ tiaas_galaxy_db_name }}',
        'USER': '{{ tiaas_galaxy_db_user }}',
        'PASSWORD': '{{ tiaas_galaxy_db_pass }}',
        'HOST': '{{ tiaas_galaxy_db_host }}',
        'PORT': '{{ tiaas_galaxy_db_port }}',
    }
}

ALLOWED_HOSTS = ['*']
SECRET_KEY = '{{ tiaas_secret_key }}'
STATIC_ROOT = '{{ tiaas_static_dir }}'


{{ tiaas_other_config }}
