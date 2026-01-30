string filePath = System.Environment.GetEnvironmentVariable("file_path");
string url = System.Environment.GetEnvironmentVariable("ping_pong_url");
string greeterUrl = System.Environment.GetEnvironmentVariable("greeter_url");
string configuratedFile = System.Environment.GetEnvironmentVariable("configurated_file");
string envParamKey = "MESSAGE";

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHttpClient<PingPongClient>(client =>
{
    client.BaseAddress = new Uri(url);
});

if (!string.IsNullOrEmpty(greeterUrl))
{
    builder.Services.AddHttpClient<GreeterClient>(client =>
    {
        client.BaseAddress = new Uri(greeterUrl);
    });
}

var app = builder.Build();


app.MapGet("/", async (PingPongClient pingPongClient, GreeterClient greeterClient) => {
    string pingPongCount = await pingPongClient.GetPings();
    string greeting = "";

    if (greeterClient != null)
    {
        try
        {
            greeting = await greeterClient.GetGreeting();
        }
        catch (Exception ex)
        {
            greeting = $"Error getting greeting: {ex.Message}";
        }
    }

    string result =
        $"file content: {File.ReadAllText(configuratedFile)}" +
        System.Environment.NewLine +
        $"env variable: MESSAGE={System.Environment.GetEnvironmentVariable(envParamKey)}" +
        System.Environment.NewLine +
        File.ReadAllText(filePath) +
        System.Environment.NewLine +
        $"Ping / Pongs: {pingPongCount}" +
        System.Environment.NewLine +
        $"Greeting: {greeting}";

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
