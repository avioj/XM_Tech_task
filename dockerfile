FROM python:3.8-slim-buster as base
WORKDIR /server

FROM base as build
COPY ./pyproject.toml /server
#COPY ./poetry.lock /server

RUN pip3 install --upgrade pip && pip3 install poetry==1.2.2

FROM build as backend
RUN poetry install --without test

# Do the copy of everything *after* we have installed all the dependencies for better caching.
COPY . /server
WORKDIR /server

ENV FLASK_APP app.py
ENV FLASK_DEBUG 1
ENV JAVA_TOOL_OPTIONS "-XX:MaxRAMPercentage=50"
# the port number should expose
EXPOSE 5000
RUN ["chmod", "+x", "/server/scripts/run_server.sh"]
ENTRYPOINT ["/server/scripts/run_server.sh"]

FROM build as tests
RUN apt-get update -y \
    && apt-get install -y default-jre \
    && apt-get install -y npm \
    && npm config set unsafe-perm true \
    && npm install -g allure-commandline --save-dev \
    && rm -rf /var/lib/apt/lists/*

RUN poetry install --without development
COPY ./tests /server
WORKDIR /server
EXPOSE 8000

RUN ["chmod", "+x", "/server/run_tests_container.sh"]
CMD ["/server/run_tests_container.sh"]