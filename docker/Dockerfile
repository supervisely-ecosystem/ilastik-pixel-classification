FROM supervisely/base-py-sdk:6.73.418

RUN apt-get install unzip
RUN wget https://github.com/supervisely-ecosystem/ilastik-pixel-classification/releases/download/v1.0.0/ilastik-1.4.0b14-Linux.zip -O /ilastik-1.4.0b14-Linux.zip
RUN mkdir /ilastik-build
RUN unzip /ilastik-1.4.0b14-Linux.zip -d /ilastik-build

RUN pip install supervisely==6.73.486

LABEL python_sdk_version="6.73.486"
