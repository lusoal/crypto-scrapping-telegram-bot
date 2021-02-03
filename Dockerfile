FROM joyzoursky/python-chromedriver:3.8-selenium

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /usr/workspace

WORKDIR /usr/workspace

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]