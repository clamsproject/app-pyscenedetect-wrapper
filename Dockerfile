FROM jjanzic/docker-python3-opencv

COPY ./ ./app
WORKDIR ./app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]