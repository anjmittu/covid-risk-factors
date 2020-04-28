FROM python:3

WORKDIR /usr/lib

RUN apt update && \
apt install -y default-jre default-jdk

RUN wget http://mallet.cs.umass.edu/dist/mallet-2.0.8.tar.gz && \
tar -zxvf mallet-2.0.8.tar.gz && \
  rm mallet-2.0.8.tar.gz

RUN echo 'alias mallet="/usr/lib/mallet-2.0.8/bin/mallet"' >> /root/.bashrc

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app

RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash"]