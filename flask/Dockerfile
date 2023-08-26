FROM python:3.9.2-alpine

# upgrade pip
RUN pip install --upgrade pip

# get curl for healthchecks
RUN apk add curl
# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs -o rustup.sh
# RUN chmod +x ./rustup.sh
# RUN ./rustup.sh -y
# ENV PATH="${PATH}:${HOME}/.cargo/bin"

# permissions and nonroot user for tightened security
RUN adduser -D nonroot
RUN mkdir /home/app/ && chown -R nonroot:nonroot /home/app
RUN mkdir -p /var/log/flask-app && touch /var/log/flask-app/flask-app.err.log && touch /var/log/flask-app/flask-app.out.log
RUN chown -R nonroot:nonroot /var/log/flask-app
WORKDIR /home/app
USER nonroot

# python setup
COPY --chown=nonroot:nonroot ./requirements.txt /home/app/requirements.txt
RUN pip install -r requirements.txt
RUN export FLASK_APP=app.py

# copy all the files to the container
COPY --chown=nonroot:nonroot . .

# define the port number the container should expose
EXPOSE 5000

# used to detect whether Python's running in Docker
ENV IS_IN_DOCKER=True

CMD ["python", "app.py"]