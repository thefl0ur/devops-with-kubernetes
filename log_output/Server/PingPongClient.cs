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

     public async Task<bool> IsAlive()
     {
          try
          {
               using var response = await _httpClient.SendAsync(new HttpRequestMessage(HttpMethod.Get, "pings"));
               return response.IsSuccessStatusCode;
          }
          catch
          {
               return false;
          }
     }
}