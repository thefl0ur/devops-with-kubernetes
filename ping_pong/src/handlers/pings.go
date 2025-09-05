package handlers

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func (h *PingsHandler) Index(c echo.Context) (err error) {
	return c.JSON(http.StatusOK, h.CounterService.GetCount())
}
