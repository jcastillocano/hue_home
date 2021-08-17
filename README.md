# hue_home

Django app for managing hue lights at home. This is a test for adding extra automation at home without using Philips Hue app (which requires internet access if you want to manage your lights remotely).

## External libraries

This project imports [hueber](https://github.com/mbaltrusitis/hueber) library for managing Hue lights through a Hue Bridge.

For more info please checkout [PyPi - hueber](https://pypi.org/project/hueber/) and [Dev - Hue](https://developers.meethue.com/develop/get-started-2/).

## Config

We need two env vars:

 * *HUE_TOKEN* hue bridge token (check hueber doc)
 * *HUE_HOST* hue bridge IP

## Initialize

### Install dependencies

1. `virtualenv .env -p python3.9`
2. `source .env/bin/activate`
3. `pip install -r requirements.txt`

For linter install `test_requirements.txt` as well (see Linter section below)

### Init db

1. `python manage.py migrate`
2. `python manage.py createsuperuser`

### Run server

1. `python manager.py runserver [optional: <host 0.0.0.0>:<port 8000>]`
2. Open browser at http://localhost:8000/

### Linter

We use [black](https://github.com/psf/black) for formatting python files.

 * Check `black . --check`
 * Format files `black .` 

NOTE: we have github action configured for linting all python files.

## Usage

Every time you load the site it will sync up Hue Bridge with local db. After that you can modify lights one by one, turning them on/off, setting intensity, etc.

## Author

Juan Carlos Castillo Cano <mailto:jccastillocano@gmail.com>
