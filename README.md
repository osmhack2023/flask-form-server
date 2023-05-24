# Form Server 

- Supports captcha
- Supports file upload

## Api Usage

### For Captcha verification
```js
// POST /api/submit
{
    "token": "captcha token",
}
// Response
{
    "success": true,
    "message": ""
}
{
    "success": false,
    "message": "Captcha verification failed, try again!"
}
```

### For Form Submission
```js
// POST /api/formsubmit
{
    ... key value pairs of form data
    "file": {file}
}
// Response
{
    "success": true,
    "message": ""
}

{
    "success": false,
    "message": {error message}
}
```

## Hosting Locally

```bash
$ git clone https://github.com/osmhack2023/flask-form-server.git
$ cd flask-form-server
```

Fill/Export the environment variables


### With Poetry
```bash
$ poetry install
$ poetry run python main.py
OR
$ poetry run gunicorn main:app
```

### With Pip
```bash
$ pip install -r requirements.txt
$ python main.py
OR
$ python -m gunicorn main:app
```

