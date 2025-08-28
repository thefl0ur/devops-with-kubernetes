package services

import "os"

type WriterService struct {
	Path string
}

func NewWriterService(path string) *WriterService {
	return &WriterService{Path: path}
}

func (w *WriterService) Write(line string) {
	os.WriteFile(w.Path, []byte(line), 0644)
}
