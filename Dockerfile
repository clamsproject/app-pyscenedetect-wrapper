FROM clamsproject/clams-python-opencv4

COPY ./ ./app
WORKDIR ./app

RUN pip install --upgrade pip
RUN pip install --upgrade -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]