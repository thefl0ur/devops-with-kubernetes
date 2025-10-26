package services

import (
	"context"

	"github.com/jackc/pgx/v5"
)

type CounterService struct {
	counter int64
	db      *pgx.Conn
}

func NewCounterService(dbConnection *pgx.Conn) *CounterService {
	c := &CounterService{}

	c.db = dbConnection
	err := c.db.QueryRow(context.Background(), "SELECT value from counter").Scan(&c.counter)
	if err != nil {
		c.counter = 0
	}

	return c
}

func (c *CounterService) Increment() {
	c.counter += 1
}

func (c *CounterService) GetCount() int64 {
	return c.counter
}
