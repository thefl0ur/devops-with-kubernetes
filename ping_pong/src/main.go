package main

import (
	"context"
	"errors"
	"log/slog"
	"net/http"

	"github.com/jackc/pgx/v5/pgxpool"
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
	pool, err := pgxpool.New(context.Background(), os.Getenv("DB_CONNECTION_STRING"))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to create connection pool: %v\n", err)
		os.Exit(1)
	}
	defer pool.Close()

	counter := services.NewCounterService(pool)
	writer := services.NewWriterService(os.Getenv("SHARED_FILE_PATH"), pool)

	pingpongHandler := &handlers.PingpongHandler{
		CounterService: counter,
		WriterService:  writer,
	}
	pingsHandler := &handlers.PingsHandler{CounterService: counter}

	e := echo.New()

	e.GET("/", pingpongHandler.Index)
	e.GET("/pings", pingsHandler.Index)
	e.GET("/health", func(c echo.Context) error {
		// Test database connection by executing a simple query
		err := pool.Ping(context.Background())
		if err != nil {
			return c.String(http.StatusServiceUnavailable, "Database not connected")
		}
		return c.String(http.StatusOK, "OK")
	})

	if err := e.Start(fmt.Sprintf(":%d", GetPort())); err != nil && !errors.Is(err, http.ErrServerClosed) {
		slog.Error("failed to start server", "error", err)
	}
}
