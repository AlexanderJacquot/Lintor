FROM --platform=linux/x86-64 python:3.12

ENV PYTHONPATH=.

WORKDIR /app
ADD ./app /app

RUN python -m pip install -r requirements.txt

RUN useradd appuser && chown -R appuser /app
USER appuser

ENTRYPOINT ["python", "main.py"]
