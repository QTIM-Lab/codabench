docker compose up -d
docker compose down

docker compose logs -f django
docker compose logs -f minio
docker compose logs -f compute_worker
docker compose logs -f site_worker
docker compose logs -f flower
docker compose logs -f rabbit
docker compose logs -f caddy

/var/log/rabbitmq/

docker compose exec django bash
docker compose exec minio bash
docker compose exec compute_worker bash
docker compose exec site_worker bash
docker compose exec flower bash
docker compose exec rabbit bash


docker compose restart django
docker compose restart compute_worker
docker compose restart minio
docker compose restart site_worker
docker compose exec django ./manage.py collectstatic
docker attach codabench-django-1
docker attach codabench-site_worker-1

docker compose exec django flake8 src/

# Begin in codabench root directory
cd codabench

# See data we are going to purge
ls var

# Purge data
# sudo rm -r var/postgres/*
# sudo rm -r var/minio/*
# sudo rm -r var/rabbit/*

# Restart services and recreate database tables
docker compose down
docker compose up -d
docker compose exec django ./manage.py migrate
docker compose exec django ./manage.py makemigrations

# Debugging
## Debugger
pdb works but for workers you need more advanced settings.
Add the following to docker-compose.yml for either worker:
```bash
  #-----------------------------------------------
  #   Celery Service
  #-----------------------------------------------
  site_worker:
  ...
    stdin_open: true
    tty: true
    ports:
      - 6900-7000:6900-7000
    environment:
      - CELERY_RDB_HOST=0.0.0.0
      - PYTHONUNBUFFERED=1
      - COLUMNS=80  # Add this line
  ...
```
* Then you can drop this almost anywhere. Thing is obviously it will work in compute_worker and most tasks assigned to site worker.
* Where it gets interesting is model instances or util funcs\methods used by the workers no matter how deep can be debugged with this.
* Ex: A Competion model instance you want to save with .save(). You can drop the below in that method if you want.
```python
from celery.contrib import rdb
rdb.set_trace()
# You will get instructions to `telnet` inside logs from django, site\compute worker or etc.
```
## Can't connect to workers but site is working and rabbit is working
`.env` sometimes needs `AWS_S3_ENDPOINT_URL` set to your current internal ip:
```bash
# $(ip add show | grep -oP 'inet \K[^/]+' | awk 'NR==2')
AWS_S3_ENDPOINT_URL=http://192.168.7.223:9000
```

# Create Storage Analytics
```bash
docker compose exec django bash
python manage.py shell_plus --plain
from analytics.tasks import create_storage_analytics_snapshot
create_storage_analytics_snapshot()
```

# Make Accounts
docker compose exec django pip install blessings
docker compose exec django bash
python manage.py shell_plus
```python
# User.objects.all_objects()
u = User(username='organizer') # can also use email
u = User(username='bbearce') # can also use email
u = User(username='guest') # can also use email
u = User.objects.get(username='organizer') # can also use email
u = User.objects.get(username='guest') # can also use email
u = User(username='guest2') # can also use email
u.set_password('testtest')
u = User.objects.get(username='emilyktownley') # can also use email
u = User.objects.get(username='ehaneda') # can also use email
u = User.objects.get(username='ehaneda521') # can also use email
u.is_active = True
u.is_staff = True
u.is_superuser = True
u.save()
# u.delete()
```

# DB
## Shell into DB
```bash
docker compose exec -it db bash
psql -U postgres postgres
```
## Then SQL:
```sql
\dt
select
id, username, is_active, is_superuser, is_staff, email
from profiles_user;
where username = 'bbearce';
update profiles_user
set is_active = 'true'
where username = 'guest';
select *
select
id, name, competition_id,
public_data_id, starting_kit_id
from competitions_phase where competition_id = 15;
-- from competitions_phase limit 1;
```

# Tests
```bash
# Not e2e
docker compose exec django py.test -m "not e2e"
docker compose exec django py.test src/apps/competitions/tests/test_v2_unpacker.py::V2UnpackerTests::test_phase_unpacking
# Selenium
./run_selenium_tests.sh
docker compose -f docker-compose.yml -f docker-compose.selenium.yml up -d
docker compose -f docker-compose.yml -f docker-compose.selenium.yml down
docker compose -f docker-compose.yml -f docker-compose.selenium.yml exec django py.test src/tests/functional/ -m e2e
docker compose -f docker compose.yml -f docker compose.selenium.yml exec django py.test src/tests/functional/test_submissions.py::TestSubmissions::test_v2_submission_end_to_end

```


# Navigating a competition 
```python

competition.solutions
competition.files

competition.phases

p = competition.phases.order_by('index').first()

competition.phases.order_by('index').first().tasks

competition.phases.order_by('index').first().tasks.all()[0]

competition.phases.order_by('index').first().tasks.all()[0].solutions.all()[0]

competition.phases.order_by('index').first().tasks.all()[0].get_chahub_data(include_solutions=True)['solutions']
# ---------- #

input_data = instance.task.input_data
ingestion_program = instance.task.ingestion_program
scoring_program = instance.task.scoring_program
reference_data = instance.task.reference_data

input_data.id


qs = instance.task.starting_kit # part of phases not tasks

qs = instance.task.solutions.all()
```

# Certbot
sudo apt update
sudo apt install snapd

sudo apt-get remove certbot
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot certonly --standalone
sudo certbot renew

sudo cp /etc/letsencrypt/live/qtim-challenges.southcentralus.cloudapp.azure.com/fullchain.pem certs/caddy/
sudo cp /etc/letsencrypt/live/qtim-challenges.southcentralus.cloudapp.azure.com/privkey.pem certs/caddy/

## Minio
> We need to secure minio when in https mode and otherwise it needs to be http.

Summary:
* Use same ssl certs from letsencrypt (certbot) but change fullchain.pem -> public.crt and privkey.pem -> private.key. I copied from ./certs/caddy (for django/caddy) to ./certs/minio/certs.
* You need to change the command for minio to "server /export --certs-dir /root/.minio/certs" and not just "server /export"
* Mount  in certs: 
  - Add "- ./certs/minio:/root/.minio" under the minio service's "volumes" section
* Certs must be in /${HOME}/.minio and for dockers ends up being /root/.minio

```bash
sudo ls -la certs/minio/certs
```

## Copy Certs
```bash
sudo cp /home/azureuser/codabench/certs/caddy/fullchain.pem /home/azureuser/codabench/certs/minio/certs/public.crt
sudo cp /home/azureuser/codabench/certs/caddy/privkey.pem /home/azureuser/codabench/certs/minio/certs/private.key
```

## Inspect cert
sudo openssl x509 -noout -in /home/azureuser/codabench/certs/minio/certs/public.crt -dates

```bash
 #-----------------------------------------------
  # Minio local storage helper
  #-----------------------------------------------
  minio:
    image: minio/minio:RELEASE.2020-10-03T02-19-42Z
    command: server /export --certs-dir /root/.minio/certs
    volumes:
      - ./var/minio:/export
      - ./certs/minio:/root/.minio
    restart: unless-stopped
    ports:
      - $MINIO_PORT:9000
    env_file: .env
    healthcheck:
      test: ["CMD", "nc", "-z", "minio", "9000"]
      interval: 5s
      retries: 5
```

```bash
docker compose up minio -d
```


# Email
```python
from competitions.emails import send_participation_requested_emails
user = User.objects.filter(username='organizer')[0]
competition = Competition.objects.filter(id=1)[0]
competition_participant = CompetitionParticipant.objects.filter(competition=competition, user=user)[0]

send_participation_requested_emails(competition_participant)
```


# Docker Submissions

```bash
docker compose exec django bash
python manage.py shell
```

```python
from competitions.tasks import build_user_docker_image
build_user_docker_image.apply_async(args=("11",))
```
