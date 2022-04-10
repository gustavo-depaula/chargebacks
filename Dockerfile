FROM python:3.10

# install poetry
RUN pip install poetry
WORKDIR /home/chargebacks
RUN poetry install

# build with docker build -t chargebacks_web .
