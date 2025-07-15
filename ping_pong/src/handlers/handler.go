package handlers

import (
	"ping-pong/services"
)

type (
	Handler struct {
		CounterService *services.CounterService
	}
)
