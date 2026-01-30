var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => {
    var greetMessage = Environment.GetEnvironmentVariable("greet_message") ?? "Hello from Greeter!";
    return greetMessage;
});

app.Run();