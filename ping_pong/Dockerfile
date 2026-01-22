FROM golang:1.24.5-alpine AS build

WORKDIR /app

COPY src/go.mod src/go.sum ./

RUN go mod download

COPY src/ . 

RUN ["go", "build"]

FROM golang:1.24.5-alpine AS server

ARG PORT=8002

ENV PORT=${PORT}

ENV SHARED_FILE_PATH='/tmp/ping'

EXPOSE ${PORT}

WORKDIR /app

COPY --from=build /app/ping-pong .

CMD ["./ping-pong"]

