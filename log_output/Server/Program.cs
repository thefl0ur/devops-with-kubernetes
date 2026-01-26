string filePath = System.Environment.GetEnvironmentVariable("file_path");
string url = System.Environment.GetEnvironmentVariable("ping_pong_url");
string configuratedFile = System.Environment.GetEnvironmentVariable("configurated_file");
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

app.MapGet("/health", async (PingPongClient pingPongClient) => {
    try
    {
        bool isAlive = await pingPongClient.IsAlive();
        if (isAlive)
        {
            return Results.Ok("OK");
        }
        else
        {
            return Results.StatusCode(503);
        }
    }
    catch (Exception)
    {
        return Results.StatusCode(503);
    }
});

app.Run();
