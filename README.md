# HoppoRoo

The web application that runs on the Raspberry Pi has been written in Python with Django
web framework. This application allows the teacher to create, access and store quizzes and quiz
data. It also allows the teacher to view the real time score of the classroom. From the home page 
the teacher can do everything necessary as well as start/create a quiz.

To run sandbox/dev instance locally:
```
$ git clone https://github.com/jpoirier55/HoppoRoo
$ cd HoppoRoo
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver <dest ip add>:<dest port>
``` 
Go to http://dest_ip:dest_port to see running sandbox instance.

Currently I am hosting an AWS cloud server with the app running here (Limited functionality due to permissions and rpi directories):
## http://hopporoo.jakepoirierdev.com
