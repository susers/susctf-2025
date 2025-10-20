FROM surnet/alpine-python-wkhtmltopdf:3.13.5-0.12.6-small

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .
COPY --chmod=755 run.sh .

CMD ["/app/run.sh"]

