FROM golang:1.24.5-alpine AS build

WORKDIR /app

COPY src/ .

RUN ["go", "build"]

FROM golang:1.24.5-alpine AS server

ARG PORT=8002

ENV PORT=${PORT}

EXPOSE ${PORT}

WORKDIR /app

COPY --from=build /app/ping-pong .

CMD ["./ping-pong"]

