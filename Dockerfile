FROM python:alpine3.19

COPY echo-server.py /echo-server.py

CMD ["python3", "-u","/echo-server.py"]

EXPOSE 4001/udp
EXPOSE 4002/udp
EXPOSE 4003/udp
EXPOSE 5001/tcp
EXPOSE 5002/tcp
EXPOSE 5003/tcp
