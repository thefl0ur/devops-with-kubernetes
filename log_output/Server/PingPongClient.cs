public class PingPongClient
{
     private readonly HttpClient _httpClient;
     public PingPongClient(HttpClient httpClient)
     {
          _httpClient = httpClient;
     }

     public async Task<string> GetPings()
     {
          using var response = await _httpClient.GetAsync("pings");
          response.EnsureSuccessStatusCode();
          return await response.Content.ReadAsStringAsync();
     }
}