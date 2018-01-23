# LuponCRM

## Requirements

- python3
- virtualenv
- git
- PostgreSQL
- some kind of OS with root access

## Installation

```bash
sudo useradd lupon
su lupon
```

```Bash
virtualenv -p python3 venv
cd venv
scource bin/activate
```

```Bash
git clone https://github.com/RolfZurbrugg/lupon.git
cd lupon
pip install --editable .
# OR
pip install -r requirements.txt
```

## Flask-Script

```shell
# Initialize Database and create default user
python manage.py init
# Start appliaction in development mode
python manage.py runserver
```

## Configuration

```shell
cp config-example.py config.py
```

Disable debug Toolbar and/or redirect interception
```python
DEBUG_TB_INTERCEPT_REDIRECTS = False
DEBUG_TB_ENABLED = False
```

If https is used, please set preferred URL SCHEME which affects all url_for() calls
```python
PREFERRED_URL_SCHEME = 'https'
```

```python
# DATABASE MySQL (deprecated but maybe still working) => you will need to install "pip install mysqlclient"
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/database'

# DATABASE Postgresql
SQLALCHEMY_DATABASE_URI = 'postgresql://lupon:lupon@localhost/lupon'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
```

```python
# Security
SECRET_KEY = 'real_secret_key'
# TOCKEN
SECURITY_PASSWORD_SALT = 'my_precious_two'
# GOOGLE API KEY
# https://developers.google.com/maps/documentation/javascript/get-api-key?hl=de
GOOGLE_API_KEY = 'this-is-my-google-api-key'
```

```python
# Mail
MAIL_FROM_EMAIL = "no@addre.ss" # For use in application emails
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'MAIL_USERNAME'
MAIL_PASSWORD = 'MAIL_PASSWORD'
```

### Database

Create unprivileged user
```bash
sudo useradd lupon
```

### PostgreSQL Installation

#### Archlinux
Create Database and Database User

```bash
pacuar -S postgresql
## ARCHLinux spesific??
initdb --locale $LANG -E UTF8 -D '/var/lib/postgres/data'
#Enable Service
systemctl enable postresql
systemctl start postresql
# Create DB Role and Database
sudo -u postgres -i
# add user to psql
createuser --interactive lupon
# create database lupon
createdb lupon
# drop database lupon
dropdb lupon
```

#### CentOS 7
```
yum install postgesql-server
postgresql-setup
systemctl enable postresql
systemctl start postresql
```

bug fix: update connection permissions 

```bash
su postgres
cd /var/lib/pgsql/data
vi pg_hba.conf
```
@ https://www.depesz.com/2007/10/04/ident/
Edit /var/lib/pgsql/data/pg_hba.conf and change peer/ident to trust
```conf
# "local" is for Unix domain socket connections only
local   all             all                                     trust
local   all             lupon                                   trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
# Allow replication connections from localhost, by a user with the
# replication privilege.
#local   replication     postgres                                peer
#host    replication     postgres        127.0.0.1/32            ident
#host    replication     postgres        ::1/128                 ident

```

Verify DB Connection:
```bash
psql -U lupon -d lupon -h 127.0.0.1 -W
```

## Nginx 
```bash
sudo yum install nginx
sudo yum install certbot-nginx

sudo firewall-cmd --permanenet --add-service=http
sudo firewall-cmd --permanenet --add-service=https

sudo firewall-cmd --reload
```
```conf
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  84.72.0.143 www lupon.ch www.lupon.ch dev.lupon.ch;
        # Redirect to HTTPS
        return       301 https://dev.lupon.ch;
    }

   server {
        listen       443 ssl http2 default_server;
        listen       [::]:443 ssl http2 default_server;
        server_name  84.72.0.143 dev dev.lupon.ch;
        root         /usr/share/nginx/html;

        ssl_certificate /etc/letsencrypt/live/dev.lupon.ch/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/dev.lupon.ch/privkey.pem;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;
        ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";
        ssl_ecdh_curve secp384r1;
        ssl_session_cache shared:SSL:10m;
        ssl_session_tickets off;
        ssl_stapling on;
        ssl_stapling_verify on;
        ssl_dhparam /etc/ssl/certs/dhparam.pem;
        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
                proxy_pass http://127.0.0.1:5000;
                proxy_buffering                       off;
                proxy_set_header Host                 $http_host;
                proxy_set_header X-Real-IP            $remote_addr;
                proxy_set_header X-Forwarded-For      $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto    $scheme;
        }
   }
}

```



### Let's Encrypt

1. Create Standalonecertificate as per default nginx will not answer on https port without certificate
```bash
sudo certbot certonly -d dev.lupon.ch
```
2. Create Diffihelman key
```bash
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
```
3. Update certbot renew configuration (authenticator and installer)


```bash
cat /etc/letsencrypt/renewal/dev.lupon.ch.conf
...
# renew_before_expiry = 30 days
version = 0.19.0
archive_dir = /etc/letsencrypt/archive/dev.lupon.ch
cert = /etc/letsencrypt/live/dev.lupon.ch/cert.pem
privkey = /etc/letsencrypt/live/dev.lupon.ch/privkey.pem
chain = /etc/letsencrypt/live/dev.lupon.ch/chain.pem
fullchain = /etc/letsencrypt/live/dev.lupon.ch/fullchain.pem

# Options used in the renewal process
[renewalparams]
authenticator = nginx
installer = nginx
account = ...
...
```

4. Test Certificate Renewal
```bash
sudo certbot renew --dry-run
```

5. Add a cronjob for autorenewal

```bash
sudo crontab -e -u root
...
15 4 * * 1 /usr/bin/certbot renew >> /var/log/renew-certs.log
18 4 * * 1 /usr/bin/systemctl reload nginx
...
```

## Docker

yum install docker
systemctl enable docker
systemctl start docker

docker build -t lupon .
docker run -it --rm --name flaskapp -v "$PWD":/usr/src/app -w /usr/src/app -e LANG=C.UTF-8 -e FLASK_APP=lupon -p 5000:5000 lupon

## Dependencies

* Flask
* Flask-Babel
* Flask-Mail
* Flask-Cache
* Flask-WTF
* Flask-Login
* requests
* ...
## Database
* Psycopg2
* Flask-SQLAlchemy
* ...


## Documentation References

### Plugins
* Flask: http://flask.pocoo.org/docs/0.12/
* Flask-SQLAlchemy: http://flask-sqlalchemy.pocoo.org/2.3/
* WTForms: https://wtforms.readthedocs.io/en/latest/index.html
* Flask-WTF: https://flask-wtf.readthedocs.io/en/stable/index.html
* Flask-Babel: https://pythonhosted.org/Flask-Babel/
* SQLAlchemy: http://docs.sqlalchemy.org/en/latest/orm/index.html
* Twitter Bootstrap: https://getbootstrap.com/docs/4.0/getting-started/introduction/
* Jinja2 (Templateing): http://jinja.pocoo.org/docs/2.9/templates/#
* Flask-Login: http://flask-login.readthedocs.io/en/latest/

### HowTos & Tutorials
* Example Flask Project(Template): https://github.com/xen/flask-project-template
* Flask Example Projekct: https://github.com/imwilsonxu/fbone
* Flask by Example: https://realpython.com/blog/python/flask-by-example-part-1-project-setup/
* Flask Mega Tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
* GoogleMaps API: https://developers.google.com/maps/documentation/javascript/tutorial
* Explore Flask: http://exploreflask.com/en/latest/index.html
* Email vonfirmation: https://realpython.com/blog/python/handling-email-confirmation-in-flask/
* http://blog.luisrei.com/articles/flaskrest.html

### Snippets
* Flask-WTF Tricks: https://goonan.io/flask-wtf-tricks/

## Product Backlog
Florian
* Send eMail on user registration
* Administrator Interface
* Customer management

Rolf
* Offer creation page
    * AJAX
* Search functionaliy
    * Tasks
    * Customers
