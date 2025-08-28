package main

import (
	"errors"
	"log/slog"
	"net/http"

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

func LoadInitialValue() int64 {
	sharedFilePath := os.Getenv("SHARED_FILE_PATH")
	data, err := os.ReadFile(sharedFilePath)
	if err != nil {
		return 0
	}

	value, err := strconv.ParseInt(string(data), 10, 0)
	if err != nil {
		return 0
	}

	return value
}

func main() {
	counter := services.NewCounterService(LoadInitialValue())
	writer := services.NewWriterService(os.Getenv("SHARED_FILE_PATH"))

	h := &handlers.Handler{
		CounterService: counter,
		WriterService:  writer,
	}
	e := echo.New()

	e.GET("/pingpong", h.Home)

	if err := e.Start(fmt.Sprintf(":%d", GetPort())); err != nil && !errors.Is(err, http.ErrServerClosed) {
		slog.Error("failed to start server", "error", err)
	}
}
