using System.Threading;

Guid guid = Guid.NewGuid();
TimeSpan timeout = new TimeSpan(0, 0, 5);

while (true) {
    Console.WriteLine($"{DateTime.Now}: {guid}");
    Thread.Sleep(timeout);
}

