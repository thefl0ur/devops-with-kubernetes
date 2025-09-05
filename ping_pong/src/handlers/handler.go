package handlers

import (
	"ping-pong/services"
)

type (
	PingpongHandler struct {
		CounterService *services.CounterService
		WriterService  *services.WriterService
	}
)

type (
	PingsHandler struct {
		CounterService *services.CounterService
	}
)
