var builder = WebApplication.CreateBuilder(args);
string url = "http://ping-pong-service:3456";
builder.Services.AddHttpClient<PingPongClient>(client =>
{
    client.BaseAddress = new Uri(url);
});

var app = builder.Build();

string filePath = "/tmp/share.md";

app.MapGet("/", async (PingPongClient pingPongClient) => {
    string pingpongCount = await pingPongClient.GetPings();
    string result =
        File.ReadAllText(filePath) +
        System.Environment.NewLine +
        $"Ping / Pongs: {pingpongCount}";

    return Results.Text(result);
});

app.Run();
