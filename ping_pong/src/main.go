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

func main() {
	counter := services.CounterService{}
	h := &handlers.Handler{CounterService: &counter}
	e := echo.New()

	e.GET("/pingpong", h.Home)

	if err := e.Start(fmt.Sprintf(":%d", GetPort())); err != nil && !errors.Is(err, http.ErrServerClosed) {
		slog.Error("failed to start server", "error", err)
	}
}
