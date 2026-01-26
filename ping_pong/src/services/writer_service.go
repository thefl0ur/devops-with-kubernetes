package services

import (
	"context"
	"fmt"
	"os"
	"strconv"

	"github.com/jackc/pgx/v5/pgxpool"
)

type WriterService struct {
	db   *pgxpool.Pool
	path string
}

func NewWriterService(path string, dbPool *pgxpool.Pool) *WriterService {
	w := &WriterService{}
	w.db = dbPool
	w.path = path
	return w
}

func (w *WriterService) Write(counter int64) {
	os.WriteFile(w.path, []byte(strconv.FormatInt(counter, 10)), 0644)
	_, err := w.db.Exec(context.Background(), "INSERT INTO counter (value) VALUES ($1);", counter)
	if err != nil {
		fmt.Fprintf(os.Stderr, "QueryRow failed: %v\n", err)
	}
}
