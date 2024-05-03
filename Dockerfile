FROM --platform=linux/x86-64 python:3.12

ENV PYTHONPATH=.
ADD app/ .
RUN cd /app
RUN python -m pip install -r requirements.txt

WORKDIR /app
ADD . /app

RUN useradd appuser && chown -R appuser /app
USER appuser

ENTRYPOINT ["python", "main.py"]
