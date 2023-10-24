using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Security;
using System.Threading.Tasks;
using OSIsoft.Data.Http;
using OSIsoft.Identity;
using OSIsoft.Omf;
using OSIsoft.OmfIngress;

namespace OmfIngressClientLibraries
{
    public class Device
    {
        private readonly IOmfIngressService _deviceOmfIngressService;
        private Dictionary<string, List<ParticleSensorType>> _dataToSend;

        public static string LastCollectTime { get; internal set; }
        public static string LastSendTime { get; internal set; }

        private static Random random = new Random();

        /// <summary>
        /// Initializes the device
        /// </summary>
        /// <param name="address">ADH url</param>
        /// <param name="tenantId">ADH tenantid</param>
        /// <param name="namespaceId">ADH namespace ID</param>
        /// <param name="clientId">ADH clientId</param>
        /// <param name="clientSecret">ADH client secret</param>
        internal Device(string address, string tenantId, string namespaceId, string clientId, string clientSecret)
        {
            // Create the AuthenticationHandler and IngressSerice to use to send data
            AuthenticationHandler deviceAuthenticationHandler = new (new Uri(address), clientId, clientSecret);

            OmfIngressService deviceBaseOmfIngressService = new (new Uri(address), HttpCompressionMethod.None, deviceAuthenticationHandler);
            _deviceOmfIngressService = deviceBaseOmfIngressService.GetOmfIngressService(tenantId, namespaceId);

            _dataToSend = new Dictionary<string, List<ParticleSensorType>>();

            string sensor = Sensors.GetSensor();
            _dataToSend.Add(sensor, new List<ParticleSensorType>());
        }

        /// <summary>
        /// Creates the OMF Data type
        /// </summary>
        /// <returns></returns>
        public async Task CreateDataPointTypeAsync()
        {
            Console.WriteLine($"Creating Type with Id {typeof(ParticleSensorType).Name}");
            Console.WriteLine();

            OmfTypeMessage typeMessage = OmfMessageCreator.CreateTypeMessage(typeof(ParticleSensorType));
            await SendOmfMessageAsync(typeMessage).ConfigureAwait(false);
        }

        /// <summary>
        /// Creates the stream for the sensor.
        /// </summary>
        /// <param name="streamId">Stream to create</param>
        /// <returns></returns>
        public async Task CreateStreamAsync(string streamId)
        {
            // Create container
            Console.WriteLine($"Creating Container with Id {streamId}");
            Console.WriteLine();

            OmfContainerMessage containerMessage = OmfMessageCreator.CreateContainerMessage(streamId, typeof(ParticleSensorType));
            await SendOmfMessageAsync(containerMessage).ConfigureAwait(false);
        }

        /// <summary>
        /// This prepares sending the values in the OMF data message
        /// </summary>
        public async void SendValuesAsync()
        {
            if (AbleToSend())
            {
                OmfDataMessage dataMessage = null;
                lock (_dataToSend)
                {
                    Dictionary<string, IEnumerable<ParticleSensorType>> dataToSend = new Dictionary<string, IEnumerable<ParticleSensorType>>();
                    foreach(var pair in _dataToSend)
                    {
                        dataToSend.Add(pair.Key, pair.Value.AsEnumerable());
                    }

                    dataMessage = OmfMessageCreator.CreateDataMessage(dataToSend);
                   
                    foreach(var sentValues in _dataToSend.Values)
                    {
                        sentValues.Clear();
                    }
                }

                LastSendTime = DateTime.Now.ToString();
                await SendOmfMessageAsync(dataMessage).ConfigureAwait(false);
            }
        }

        /// <summary>
        /// This function determines whether the device is able to actually send the data.  In the real world, this might be a ping or some call to network to make sure it
        /// is in a good state
        /// </summary>
        /// <returns>Whether to attempt to send the data</returns>
        private bool AbleToSend()
        {
            return true;
            /*
             * if (!(_dataToSend.Values.Any(x => x.Count >0)))
                return false;
            return random.Next(100) < 10;
            */
        }

        /// <summary>
        /// This call accesses the sensors attached to this device to get the appropriate data and sensor names(s).
        /// </summary>
        internal void ColectData()
        {
            ParticleSensorType dataPoint = Sensors.GetData();
            string sensor = Sensors.GetSensor();

            lock (_dataToSend)
            {
                _dataToSend[sensor].Add(dataPoint);
                LastCollectTime = DateTime.Now.ToString();
            }
        }

        /// <summary>
        /// This send the omfMessage to the preconfigured endpoint
        /// </summary>
        /// <param name="omfMessage">Message to be sent</param>
        /// <returns></returns>
        private async Task SendOmfMessageAsync(OmfMessage omfMessage)
        {
            SerializedOmfMessage serializedOmfMessage = OmfMessageSerializer.Serialize(omfMessage);
            await _deviceOmfIngressService.SendOmfMessageAsync(serializedOmfMessage).ConfigureAwait(false);
        }
    }
}
