FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000
USER nobody:nogroup
ENTRYPOINT ["python"]
CMD ["app.py"]
