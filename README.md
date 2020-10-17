# Cares

Never miss signing up for [New York Cares](https://www.newyorkcares.org/) projects again. Automates log in, find projects and sign up. Cron job runs weekly on Monday, Wednesday, Thursday and Friday.

## Deploy

```
gcloud app deploy app.yaml
```

```
gcloud app deploy cron.yaml
```

## Check cron job

[App engine console cron job](https://console.cloud.google.com/appengine/taskqueues/cron?project=cares-291215)