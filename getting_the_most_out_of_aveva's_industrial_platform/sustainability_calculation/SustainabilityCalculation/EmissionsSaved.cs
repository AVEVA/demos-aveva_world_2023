using SustainabilityCalculation.models;
using Microsoft.Azure.WebJobs;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using System.Threading;

namespace SustainabilityCalculation
{
    public class EmissionsSaved
    {
        private static SdsSecurityHandler securityHandler;
        private static HttpClient httpClient;

        private static readonly string RESOURCE = Environment.GetEnvironmentVariable("ADH_PROD_URL");
        private static readonly string TENANT_ID
            = Environment.GetEnvironmentVariable("ADH_PROD_TENANT_ID");
        private static readonly string NAMESPACE_ID
            = Environment.GetEnvironmentVariable("ADH_PROD_NAMESPACE_ID");
        private static readonly string COMMUNITY_ID
            = Environment.GetEnvironmentVariable("ADH_PROD_COMMUNITY_ID");
        private static readonly string CLIENT_ID
            = Environment.GetEnvironmentVariable("ADH_PROD_CLIENT_ID");
        private static readonly string CLIENT_SECRET
            = Environment.GetEnvironmentVariable("ADH_PROD_CLIENT_SECRET");

        private static readonly string T_FORMAT = "yyyy-MM-ddTHH:mm:00";
        private static readonly double MAX_EVENTS = 250000;
        private static readonly int MAX_CONCURRENT = 10;

        private static readonly double CHARGE_VOLTAGE = 208; // Volts
        private static readonly double WATTSECONDS_TO_MEGAWATTHOURS = 1.0 / (3600.0 * Math.Pow(10, 6));
        private static readonly double MEGATONS_TO_KG = 1000.0;

        private static readonly double AVERAGE_CHARGING_EFFICIENCY = .90; // MPG
        private static readonly double AVERAGE_ICE_CAR_FUEL_ECONOMY = 24.2; // MPG
        private static readonly double AVERAGE_ELECTRIC_CAR_FUEL_ECONOMY = 2.83; // MPkWh
        private static readonly double GALLONS_OF_GAS_TO_KG_CO2 = 8.9; // Kg
        private static readonly double ENERGY_TO_SAVED_EMISSIONS = AVERAGE_CHARGING_EFFICIENCY * AVERAGE_ICE_CAR_FUEL_ECONOMY / AVERAGE_ELECTRIC_CAR_FUEL_ECONOMY * GALLONS_OF_GAS_TO_KG_CO2 * Math.Pow(10, 3); // Kg/MWh

        private static List<TimeIndexedDouble> CalculateEmissionsSaved(
            ref double totalizedSavedEmissions,
            IEnumerable<TimeIndexedDouble> chargerAmps,
            IEnumerable<TimeIndexedDouble> demand,
            IEnumerable<TimeIndexedDouble> totalEmissions
            )
        {
            List<TimeIndexedDouble> calculationResults = new List<TimeIndexedDouble>();
            for (int i = 0; i < chargerAmps.Count() - 1; i++)
            {
                // Reset the totalized value if the timestamp is a start of a day
                if (chargerAmps.ElementAt(i).Timestamp.ToLocalTime().TimeOfDay.Equals(TimeSpan.Zero))
                {
                    totalizedSavedEmissions = 0;
                }
                else
                {
                    double energy = (chargerAmps.ElementAt(i + 1).Value + chargerAmps.ElementAt(i).Value) / 2 *
                        (chargerAmps.ElementAt(i + 1).Timestamp - chargerAmps.ElementAt(i).Timestamp).TotalSeconds *
                        CHARGE_VOLTAGE * WATTSECONDS_TO_MEGAWATTHOURS; // MWh
                    double emissions = energy * totalEmissions.ElementAt(i).Value / demand.ElementAt(i).Value * MEGATONS_TO_KG; // Kg
                    double savedEmissions = energy * ENERGY_TO_SAVED_EMISSIONS; // Kg
                    double netSavedEmissions = savedEmissions - emissions;
                    totalizedSavedEmissions += netSavedEmissions;
                }
                calculationResults.Add(new TimeIndexedDouble
                {
                    Timestamp = chargerAmps.ElementAt(i).Timestamp,
                    Value = totalizedSavedEmissions
                });
            }
            return calculationResults;
        }

        private static async Task RunStreamCalculationAsync(StreamSearchResult stream, DateTime endIndex, SemaphoreSlim semaphore, ILogger log)
        {
            try
            {
                // Get or create the corresponding output stream
                string outputStreamId = $"{string.Join('-', stream.Id.Split('-').Take(6))}-TotalizedDailySavedEmissions";
                SdsStream outputStream = new()
                {
                    Id = outputStreamId,
                    Name = outputStreamId,
                    TypeId = stream.TypeId
                };

                using StringContent content0 = new(JsonConvert.SerializeObject(outputStream));
                HttpResponseMessage response = await httpClient.PutAsync(
                    new Uri($"api/v1/Tenants/{TENANT_ID}/Namespaces/{NAMESPACE_ID}/Streams/{outputStreamId}", UriKind.Relative),
                    content0)
                    .ConfigureAwait(false);
                CheckIfResponseWasSuccessful(response);

                // Retrieve the last totalized value and determine start index
                response = await httpClient.GetAsync(
                            new Uri($"api/v1/Tenants/{TENANT_ID}/Namespaces/{NAMESPACE_ID}/Streams/{outputStreamId}/Data/Last", UriKind.Relative))
                            .ConfigureAwait(false);
                CheckIfResponseWasSuccessful(response);
                TimeIndexedDouble lastValue =
                    JsonConvert.DeserializeObject<TimeIndexedDouble>(await response.Content.ReadAsStringAsync().ConfigureAwait(false));

                double totalizedSavedEmissions = lastValue?.Value ?? 0;
                DateTime startIndex;
                if (lastValue?.Timestamp != null)
                {
                    startIndex = lastValue.Timestamp.AddMinutes(1);
                }
                else
                {
                    using (HttpRequestMessage request = new (HttpMethod.Get, new Uri($"{stream.Self}/Data/First")))
                    {
                        request.Headers.Add("Community-Id", COMMUNITY_ID);
                        response = await httpClient.SendAsync(request).ConfigureAwait(false);
                    }
                    CheckIfResponseWasSuccessful(response);
                    TimeIndexedDouble firstValue =
                        JsonConvert.DeserializeObject<TimeIndexedDouble>(await response.Content.ReadAsStringAsync().ConfigureAwait(false));
                    startIndex = firstValue.Timestamp;
                }

                while (startIndex < endIndex)
                {
                    DateTime sliceStartIndex = startIndex;
                    DateTime sliceEndIndex = new (Math.Min(startIndex.AddMinutes(MAX_EVENTS - 1).Ticks, endIndex.Ticks));
                    int count = (int)((sliceEndIndex - sliceStartIndex) / TimeSpan.FromMinutes(1)) + 1;

                    // Retrieve charger amperage data
                    using (HttpRequestMessage request = new (HttpMethod.Get, new Uri($"{stream.Self}/Data/Interpolated?startIndex={sliceStartIndex.ToString(T_FORMAT)}&endIndex={sliceEndIndex.ToString(T_FORMAT)}&count={count}")))
                    {
                        request.Headers.Add("Community-Id", COMMUNITY_ID);
                        response = await httpClient.SendAsync(request).ConfigureAwait(false);
                    }
                    CheckIfResponseWasSuccessful(response);
                    IEnumerable<TimeIndexedDouble> chargerAmps =
                        JsonConvert.DeserializeObject<IEnumerable<TimeIndexedDouble>>(await response.Content.ReadAsStringAsync().ConfigureAwait(false));

                    // Retrieve electricity supply data
                    response = await httpClient.GetAsync(
                            new Uri($"api/v1/Tenants/{TENANT_ID}/Namespaces/{NAMESPACE_ID}/Streams/CAISO-TotalDemand/Data/Interpolated?startIndex={sliceStartIndex.ToString(T_FORMAT)}&endIndex={sliceEndIndex.ToString(T_FORMAT)}&count={count}", UriKind.Relative))
                            .ConfigureAwait(false);
                    CheckIfResponseWasSuccessful(response);
                    IEnumerable<TimeIndexedDouble> demand =
                        JsonConvert.DeserializeObject<IEnumerable<TimeIndexedDouble>>(await response.Content.ReadAsStringAsync().ConfigureAwait(false));

                    response = await httpClient.GetAsync(
                            new Uri($"api/v1/Tenants/{TENANT_ID}/Namespaces/{NAMESPACE_ID}/Streams/CAISO-TotalCO2/Data/Interpolated?startIndex={sliceStartIndex.ToString(T_FORMAT)}&endIndex={sliceEndIndex.ToString(T_FORMAT)}&count={count}", UriKind.Relative))
                            .ConfigureAwait(false);
                    CheckIfResponseWasSuccessful(response);
                    IEnumerable<TimeIndexedDouble> totalEmissions =
                        JsonConvert.DeserializeObject<IEnumerable<TimeIndexedDouble>>(await response.Content.ReadAsStringAsync().ConfigureAwait(false));

                    // Get calculation results and send them to Data Hub                
                    List<TimeIndexedDouble> calculationResults = CalculateEmissionsSaved(ref totalizedSavedEmissions, chargerAmps, demand, totalEmissions);

                    using StringContent content1 = new(JsonConvert.SerializeObject(calculationResults));
  
                    response = await httpClient.PutAsync(
                        new Uri($"api/v1/Tenants/{TENANT_ID}/Namespaces/{NAMESPACE_ID}/Streams/{outputStreamId}/Data", UriKind.Relative),
                        content1)
                        .ConfigureAwait(false);
                    CheckIfResponseWasSuccessful(response);

                    startIndex = startIndex.AddMinutes(MAX_EVENTS - 1);
                }
            }
            catch (Exception ex)
            {
                log.LogError(ex.Message);
            }
            finally
            {
                semaphore.Release();
            }
        }


        [FunctionName("EmissionsSaved")]
        public async static Task Run([TimerTrigger("0 */5 * * * *"
#if DEBUG
            , RunOnStartup=true
#endif
            )]TimerInfo myTimer, ILogger log)
        {
            try
            {
                log.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");

                // Set up services
                securityHandler = new SdsSecurityHandler(RESOURCE, CLIENT_ID, CLIENT_SECRET);
                httpClient = new(securityHandler) { BaseAddress = new Uri(RESOURCE) };
                httpClient.DefaultRequestHeaders.Add("Request-Timeout", "600");
                httpClient.Timeout = TimeSpan.FromSeconds(600);

                // Get end time for this run
                DateTime endIndex = DateTime.UtcNow.AddMinutes(-5);

                // Read available car charger streams
                HttpResponseMessage response = await httpClient.GetAsync(new Uri($"api/v1-preview/Search/Communities/{COMMUNITY_ID}/Streams?query=*PilotSignalAmps*", UriKind.Relative)).ConfigureAwait(false);
                CheckIfResponseWasSuccessful(response);
                List<StreamSearchResult> streams = JsonConvert.DeserializeObject<List<StreamSearchResult>>(await response.Content.ReadAsStringAsync().ConfigureAwait(false));

                // Run calculation on streams and await results
                SemaphoreSlim semaphore = new(MAX_CONCURRENT, MAX_CONCURRENT);
                List<Task> tasks = new();
                foreach (StreamSearchResult stream in streams)
                {
                    await semaphore.WaitAsync();
                    tasks.Add(RunStreamCalculationAsync(stream, endIndex, semaphore, log));
                }
                await Task.WhenAll(tasks);
            }
            catch (Exception ex)
            {
                log.LogError(ex.Message);
            }
        }

        private class TimeIndexedDouble
        {
            public DateTime Timestamp { get; set; }
            public double Value { get; set; }
        }

        private static void CheckIfResponseWasSuccessful(HttpResponseMessage response)
        {
            // If support is needed please know the Operation-ID header information for support purposes (it is included in the exception below automatically too)
            // string operationId = response.Headers.GetValues("Operation-Id").First();
            if (!response.IsSuccessStatusCode)
            {
                throw new HttpRequestException(response.ToString());
            }
        }
    }
}
