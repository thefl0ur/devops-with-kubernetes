package handlers

import (
	"fmt"
	"github.com/labstack/echo/v4"
	"net/http"
)

func (h *Handler) Home(c echo.Context) (err error) {
	counter := h.CounterService
	counter.Increment()
	return c.JSON(http.StatusOK, fmt.Sprintf("Pong %d", counter.GetCount()))
}
