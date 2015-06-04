base:
  '*':
    - requirements.essential
    - ssh
  'writerr-vagrant.qubitlogic.net':
    - writerr.requirements
    - writerr.nginx
    - writerr.share
    - writerr.venv
    - writerr.uwsgi
    - writerr.postgresql

