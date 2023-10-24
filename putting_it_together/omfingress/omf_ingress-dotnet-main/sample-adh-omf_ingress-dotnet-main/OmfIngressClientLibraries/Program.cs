using System;
using System.IO;
using System.Security;
using System.Threading;
using System.Threading.Tasks;
using System.Timers;
using Microsoft.Extensions.Configuration;
using OSIsoft.Data.Http;
using OSIsoft.Identity;
using OSIsoft.OmfIngress;
using OSIsoft.OmfIngress.Models;
using Timer = System.Timers.Timer;

namespace OmfIngressClientLibraries
{
    public static class Program
    {
        internal static double ReadInterval = 1000;
        internal static double SendInterval = 10000;

        private static Device _omfDevice;
        private static IConfiguration _config;
        private static Timer _timerCollectData;
        private static Timer _timerSendData;

        public static string Resource { get; set; }
        public static string TenantId { get; set; }
        public static string NamespaceId { get; set; }
        public static string ClientId { get; set; }
        public static string ClientSecret { get; set; }
        public static string ConnectionName { get; set; }
        public static string StreamId { get; set; }
        public static string DeviceClientId { get; set; }
        public static string DeviceClientSecret { get; set; }


        public static void Main()
        {
            SetupConfiguration();
            SendTypeandContainerAsync().GetAwaiter().GetResult();
            StartCollectionAndSending();

            while (true)
            {
                Thread.Sleep(8000);
                Console.WriteLine(Device.LastCollectTime + "   " + Device.LastSendTime);
            }
        }

        private static void StartCollectionAndSending()
        {
            _timerCollectData = new (ReadInterval);
            _timerCollectData.Elapsed += new (CollectData);
            _timerCollectData.Enabled = true;


            _timerSendData = new (SendInterval);
            _timerSendData.Elapsed += new (SendData);
            _timerSendData.Enabled = true;


            Console.CancelKeyPress += delegate
            {
                _timerCollectData.Dispose();
                _timerSendData.Dispose();
                Environment.Exit(0);
            };
        }

        /// <summary>
        /// Reads in configuration
        /// </summary>
        public static void SetupConfiguration()
        {
            IConfigurationBuilder builder = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json");
            _config = builder.Build();

            // ==== Client constants ====
            TenantId = _config["TenantId"];
            NamespaceId = _config["NamespaceId"];
            Resource = _config["Resource"];
            ClientId = _config["ClientId"];
            ClientSecret = _config["ClientSecret"];
            ConnectionName = _config["ConnectionName"];
            DeviceClientId = _config["DeviceClientId"];
            ReadInterval = Convert.ToDouble(_config["ReadInterval"]);
            SendInterval = Convert.ToDouble(_config["SendInterval"]);
            GetDeviceClientSecret();

            _omfDevice = new Device(Resource, TenantId, NamespaceId, DeviceClientId, DeviceClientSecret);
        }

        /// <summary>
        /// Gets the device secret and saves it securely.  
        /// </summary>
        private static void GetDeviceClientSecret()
        {
            //TODO make this step more secure...
            DeviceClientSecret = _config["DeviceClientSecret"];            
        }

        /// <summary>
        /// Kicks off the type and container creations
        /// </summary>
        /// <returns></returns>
        public static async Task SendTypeandContainerAsync()
        {
            // Create the Type and Stream
            await _omfDevice.CreateDataPointTypeAsync().ConfigureAwait(false);
            await _omfDevice.CreateStreamAsync(Sensors.GetSensor()).ConfigureAwait(false);
        }

        /// <summary>
        /// Collects data to send
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public static void CollectData(object sender, ElapsedEventArgs e)
        {
            try
            {
                _omfDevice.ColectData();
            }
            catch(Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }
        }

        /// <summary>
        /// Sends the queued up data
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public static void SendData(object sender, ElapsedEventArgs e)
        {
            try
            {
                _omfDevice.SendValuesAsync();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }
        }
    }
}
