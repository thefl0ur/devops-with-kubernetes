package services

import (
	"context"
	"fmt"
	"os"
	"strconv"

	"github.com/jackc/pgx/v5"
)

type WriterService struct {
	db   *pgx.Conn
	path string
}

func NewWriterService(path string, dbConnection *pgx.Conn) *WriterService {
	w := &WriterService{}
	w.db = dbConnection
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
