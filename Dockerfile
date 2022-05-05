FROM python:3.9-slim
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
ENV TF_ENABLE_ONEDNN_OPTS=1
CMD gunicorn --bind :$PORT --log-level info  --workers 4 --timeout 5000 index:server