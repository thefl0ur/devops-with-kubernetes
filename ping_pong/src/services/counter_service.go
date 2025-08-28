package services

type CounterService struct {
	counter int64
}

func NewCounterService(initital int64) *CounterService {
	c := &CounterService{}
	c.counter = initital
	return c
}

func (c *CounterService) Increment() {
	c.counter += 1
}

func (c *CounterService) GetCount() int64 {
	return c.counter
}
