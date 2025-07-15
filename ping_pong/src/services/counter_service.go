package services

type CounterService struct {
	counter int64
}

func NewCounterService() *CounterService {
	return &CounterService{}
}

func (c *CounterService) Increment() {
	c.counter += 1
}

func (c *CounterService) GetCount() int64 {
	return c.counter
}
