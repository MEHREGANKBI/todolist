FROM python:3.10.13-alpine3.19

# Make a directory for the whole project.
RUN mkdir -p /home/todolist

# Copy the requirements to the container and install the dependencies.
COPY ./requirements.txt /home/todolist/
RUN pip install --no-cache-dir -r /home/todolist/requirements.txt

# Copy the source code and sqlite
COPY src/ /home/todolist/src/
COPY persistence/ /home/todolist/persistence/

# change directory to where the manage.py file is. 
WORKDIR /home/todolist/src/

# Entry point of the container
CMD ["gunicorn", "todolist.wsgi:application", "-b" , "0.0.0.0:8000"]
