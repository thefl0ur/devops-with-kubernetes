package handlers

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func (h *HomeHandler) Index(c echo.Context) (err error) {
	return c.JSON(http.StatusOK, "Alive")
}