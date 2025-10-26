package main

import (
	"context"
	"errors"
	"log/slog"
	"net/http"

	"github.com/jackc/pgx/v5"
	"github.com/labstack/echo/v4"

	"fmt"
	"os"
	"ping-pong/handlers"
	"ping-pong/services"
	"strconv"
)

const DEFAULT_PORT = 8080

func GetPort() int {
	envPortValue := os.Getenv("PORT")

	if len(envPortValue) == 0 {
		return DEFAULT_PORT
	}

	port, err := strconv.Atoi(envPortValue)
	if err != nil {
		return DEFAULT_PORT
	}

	return port
}

func main() {
	conn, err := pgx.Connect(context.Background(), os.Getenv("DB_CONNECTION_STRING"))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close(context.Background())

	counter := services.NewCounterService(conn)
	writer := services.NewWriterService(os.Getenv("SHARED_FILE_PATH"), conn)

	pingpongHandler := &handlers.PingpongHandler{
		CounterService: counter,
		WriterService:  writer,
	}
	pingsHandler := &handlers.PingsHandler{CounterService: counter}
	e := echo.New()

	e.GET("/pingpong", pingpongHandler.Index)
	e.GET("/pings", pingsHandler.Index)

	if err := e.Start(fmt.Sprintf(":%d", GetPort())); err != nil && !errors.Is(err, http.ErrServerClosed) {
		slog.Error("failed to start server", "error", err)
	}
}
