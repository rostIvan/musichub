#!/usr/bin/env bash

export $(cat .env | xargs) && export PG_HOST=$(make dbip)

PGPASSWORD=$PG_PASSWORD psql -h $PG_HOST -U $PG_USER -d postgres -c "DROP DATABASE $PG_DB"
PGPASSWORD=$PG_PASSWORD psql -h $PG_HOST -U $PG_USER -d postgres -c "CREATE DATABASE $PG_DB"
