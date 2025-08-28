var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

string filePath = "/tmp/share.md";
string? pingPath = System.Environment.GetEnvironmentVariable("PING_SHARED_FILE");

app.MapGet("/", () => {
    string result =
        File.ReadAllText(filePath) +
        System.Environment.NewLine +
        $"Ping / Pongs: {(pingPath != null ? File.ReadAllText(pingPath) : "0")}";

    return Results.Text(result);
});

app.Run();
