string filePath = "/tmp/share.md";
string url = "http://ping-pong-service:3456";
string configuratedFile = "/opt/information.txt";
string envParamKey = "MESSAGE";

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHttpClient<PingPongClient>(client =>
{
    client.BaseAddress = new Uri(url);
});

var app = builder.Build();


app.MapGet("/", async (PingPongClient pingPongClient) => {
    string pingpongCount = await pingPongClient.GetPings();
    string result =
        $"file content: {File.ReadAllText(configuratedFile)}" +
        System.Environment.NewLine +
        $"env variable: MESSAGE={System.Environment.GetEnvironmentVariable(envParamKey)}" +
        System.Environment.NewLine +
        File.ReadAllText(filePath) +
        System.Environment.NewLine +
        $"Ping / Pongs: {pingpongCount}";

    return Results.Text(result);
});

app.Run();
