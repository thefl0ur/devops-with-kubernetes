package services

import (
	"context"

	"github.com/jackc/pgx/v5/pgxpool"
)

type CounterService struct {
	counter int64
	db      *pgxpool.Pool
}

func NewCounterService(dbPool *pgxpool.Pool) *CounterService {
	c := &CounterService{}

	c.db = dbPool
	row := c.db.QueryRow(context.Background(), "SELECT value from counter")
	err := row.Scan(&c.counter)
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
