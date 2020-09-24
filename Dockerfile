FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
MAINTAINER Florian Schneider "florian.schneider.1992@gmx.de"

COPY . /app/
RUN pip install -r /app/requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
