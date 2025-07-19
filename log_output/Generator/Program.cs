using System.Threading;

Guid guid = Guid.NewGuid();
TimeSpan timeout = new TimeSpan(0, 0, 5);
string filePath = "/tmp/share.md";
Directory.CreateDirectory(Path.GetDirectoryName(filePath));

while (true) {
    File.WriteAllText(filePath, $"{DateTime.Now}: {guid}");
    Thread.Sleep(timeout);
}
