public class GreeterClient
{
     private readonly HttpClient _httpClient;
     public GreeterClient(HttpClient httpClient)
     {
          _httpClient = httpClient;
     }

     public async Task<string> GetGreeting()
     {
          using var response = await _httpClient.GetAsync("/");
          response.EnsureSuccessStatusCode();
          return await response.Content.ReadAsStringAsync();
     }
}