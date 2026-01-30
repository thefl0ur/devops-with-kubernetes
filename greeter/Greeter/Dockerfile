FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build

WORKDIR /app

COPY Greeter.csproj .

RUN dotnet restore

COPY . .

RUN dotnet publish -c Release --runtime linux-x64 -o publish/ --self-contained false

FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS runtime

ARG PORT=8080

EXPOSE ${PORT}

ENV ASPNETCORE_HTTP_PORTS=${PORT}

WORKDIR /app

COPY --from=build /app/publish/ .

CMD ["dotnet", "Greeter.dll"]