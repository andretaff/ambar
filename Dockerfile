FROM python:alpine3.7
COPY . /source
WORKDIR /source
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./source/ambar.py