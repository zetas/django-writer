include:
  - uwsgi

writerr-uwsgi:
  file.managed:
    - name: /etc/uwsgi/apps-available/writerr.ini
    - source: salt://writerr/uwsgi.ini
    - template: jinja
    - user: www-data
    - group: www-data
    - mode: 755
    - require:
      - pip: uwsgi

enable-uwsgi-app:
  file.symlink:
    - name: /etc/uwsgi/apps-enabled/writerr.ini
    - target: /etc/uwsgi/apps-available/writerr.ini
    - force: false
    - require:
      - file: writerr-uwsgi
      - file: /etc/uwsgi/apps-enabled