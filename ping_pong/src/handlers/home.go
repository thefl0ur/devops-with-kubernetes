package handlers

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/labstack/echo/v4"
)

func (h *Handler) Home(c echo.Context) (err error) {
	counter := h.CounterService
	counter.Increment()
	count := counter.GetCount()

	writer := h.WriterService
	writer.Write(strconv.FormatInt(count, 10))
	return c.JSON(http.StatusOK, fmt.Sprintf("Pong %d", count))
}
