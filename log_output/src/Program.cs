var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSingleton<HashService>();
builder.Services.AddHostedService(x => x.GetRequiredService<HashService>());
var app = builder.Build();

app.MapGet("/", (HashService hashService) => Results.Ok(hashService.LastEntry));

app.Run();
