# SafeServerApp

## **Description**
This is small server application based on pikoframework [Vial](https://goope.ee.pw.edu.pl/bach/vial) written in Python3.5. Basic functionality: authentication, ability to create new user, password recovery based on secret answer

## **Requirments**
* Python 3.6
* uwsgi plugin for Python


## **Running**
In order to run execute:
```
uwsgi --ini drink.ini
```
App will be available at localhost:9090. This method is inefficient, because some main features nead cookie in order to run. Better solution is to run application on web-server (nginx or apache) with reverse proxy and set your own domain in Cookie class.
