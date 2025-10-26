package handlers

import (
	"fmt"
	"net/http"

	"github.com/labstack/echo/v4"
)

func (h *PingpongHandler) Index(c echo.Context) (err error) {
	counter := h.CounterService
	counter.Increment()
	count := counter.GetCount()

	writer := h.WriterService
	writer.Write(count)
	return c.JSON(http.StatusOK, fmt.Sprintf("Pong %d", count))
}
