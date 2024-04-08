# FamPay Takehome

---
> Unfortunately due to an unforeseen event, I was unable to pick up the task during the weekend so completed it in one sitting so missed the part on making smaller commits.
---



## Features implemented

All requirements including Bonus Points in the [Assignment Notion Doc](https://fampay.notion.site/Backend-Assignment-FamPay-32aa100dbd8a4479878f174ad8f9d990) are implemented.

## Deploy and Test locally

### Build & Deploy the services

```shell
cd deployment
docker compose build
docker compose up
```

### Create admin username and password

Open up a new shell inside `deployment` and type the following command

```shell
docker compose exec server sh -c "export DJANGO_SUPERUSER_PASSWORD=admin-password && python3 manage.py createsuperuser --noinput --username admin --email admin@famapp.in"
```

### Login to Admin & set API Keys

- Go to [localhost:8000/admin](http://localhost:8000/admin)
- Enter username as `admin` and password as `admin-password`
- Go to [localhost:8000/admin/core/ytdatav3credentials/add](http://localhost:8000/admin/core/ytdatav3credentials/add/)
- Enter the `Encrypted text` (this is the API Key to query YouTube Data V3)
- Enter the GCP Project id and Project name and save

### Wait for data to be populated

- Go to [localhost:8000/admin/core/ytmetadata](http://localhost:8000/admin/core/ytmetadata/) and keep refreshing until data is populated. This should typically take around a minutes time.

### Test the API

- Go to http://localhost:8000/api/v1/search?q=official
