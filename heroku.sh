#!/bin/bash
gunicorn app:app --daemon
python database/worker.py
