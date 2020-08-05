# Base install

$ apt-get update
$ apt install python3-venv python3-pip libpython3-dev python3-docutils python3-sphinx
$ apt install libz-dev libjpeg-dev libssl-dev libxml2-dev libreadline-dev wv libxslt1-dev libffi-dev
$ apt install git rsync certbot poppler-utils vim screen build-essential libpcre3-dev mlocate
$ apt install sendmail
$ apt install certbot
$ certbot certonly --standalone
$ certbot renew --dry-run
$ sh -c 'printf "#!/bin/sh\n/opt/lra/bin/supervisorctl  stop nginx\n" > /etc/letsencrypt/renewal-hooks/pre/nginx.sh'
$ sh -c 'printf "#!/bin/sh\n/opt/lra/bin/supervisorctl  start nginx\n" > /etc/letsencrypt/renewal-hooks/post/nginx.sh'
$ sudo adduser www
$ cd /opt/
$ mkdir buildout-cache
$ cd buildout-cache/
$ mkdir extends
$ mkdir downloads
$ mkdir eggs
$ cd ..
$ chown -R www:www buildout-cache/
$ git clone git@github.com:a25kk/lra.git
$ cd lra/
$ git checkout update/5.2 (TODO: Switch when ready)
$ mv secret.cfg.tmp secret.cfg
$ vim secret.cfg (Use existing credentials!)
$ vim local.cfg (add existing setup)
$ openssl dhparam -out ./etc/dhparam.pem 2048
$ bootstrap.sh -c deployment.cfg
$ rsync -aPz -e "ssh -p 22222"  root@d9.ade25.de:/opt/sites/lra/buildout.lra/var/blobstorage/* ./var/blobstorage/
 
# TODO: SQL Setup
 