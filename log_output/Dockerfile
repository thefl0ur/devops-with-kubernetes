FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build

WORKDIR /app

COPY ./src .

RUN dotnet publish -c Release --runtime linux-x64 -o publish/ --self-contained false


FROM mcr.microsoft.com/dotnet/runtime:9.0 AS deploy

COPY --from=build /app/publish/ .

CMD ["dotnet", "log_output.dll"]
