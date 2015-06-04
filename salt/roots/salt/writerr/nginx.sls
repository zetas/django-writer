include:
  - nginx

writerr-nginx-conf:
  file.managed:
    - name: /etc/nginx/sites-available/writerr.conf
    - source: salt://writerr/nginx.conf
    - template: jinja
    - user: www-data
    - group: www-data
    - mode: 755
    - require:
      - pkg: nginx

# Symlink and thus enable the virtual host
writerr-enable-nginx:
  file.symlink:
    - name: /etc/nginx/sites-enabled/writerr.conf
    - target: /etc/nginx/sites-available/writerr.conf
    - force: false
    - require:
      - file: writerr-nginx-conf