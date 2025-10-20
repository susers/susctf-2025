FROM golang:1.24-alpine AS builder

WORKDIR /src
COPY src/ .
RUN go build

FROM alpine:3.22
WORKDIR /app
COPY --from=builder /src/am-i-admin .
COPY src/run.sh .

CMD ["/app/run.sh"]

