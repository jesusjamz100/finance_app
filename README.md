# Finance app (Beta)

Income and expenses, balance in various accounts and monthly control

## Requirements
* FLask == 2.2.2
* Flask-Login == 0.6.2
* Flask-Mail == 0.9.1
* Flask-SQLAlchemy == 3.0.0
* itsdangerous == 2.1.2
* SQLAlchemy == 1.4.41
* SQLAlchemy-Utils == 0.38.3
* Werkzeug == 2.2.2

## Resources
* Bootstrap 5
* Chart.js

### Initialize windows

#### Create virtual environment
```bash
pip install virtualenv
virtualenv venv
.\venv\Scripts\activate
```
#### Install requirements and set enviroment variables
```bash
pip install -r requirements.txt
$Env:APP_MAIL_USERNAME = "your email"
$Env:APP_MAIL_PASSWORD = "your password"
```
