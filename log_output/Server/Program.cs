var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

string filePath = "/tmp/share.md";

app.MapGet("/", () => Results.Ok(File.ReadAllText(filePath)));

app.Run();
