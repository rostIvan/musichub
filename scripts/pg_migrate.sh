#!/usr/bin/env bash

export $(cat .env | xargs) && export PG_HOST=$(make dbip) && ./manage.py migrate --settings=musichub.settings.local
