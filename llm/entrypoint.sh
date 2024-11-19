#!/bin/bash

# DB migrationを実行する
python api.migrate_cloud_db.py

# uvicornのサーバーを立ち上げる
uvicorn api.main:app --host 0.0.0.0