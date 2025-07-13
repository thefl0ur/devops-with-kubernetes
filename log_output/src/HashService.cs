public class HashService : BackgroundService

{
    private readonly Guid _guid = Guid.NewGuid();
    private readonly TimeSpan _timeout =  new(0, 0, 5);
    private string _last_entry = "";

    public string LastEntry
    {
        get => _last_entry;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            _last_entry = $"{DateTime.Now}: {_guid}";
            await Task.Delay(_timeout, stoppingToken);
        }
    }
}