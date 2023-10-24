using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace OmfIngressClientLibraries
{
    public static class Sensors
    {
        internal static Random Rand = new Random();
        internal static ParticleSensorType lastData = ParticleSensorType.ReturnRandom();

        public static ParticleSensorType GetData()
        {
            lastData = lastData.AddRandomNew();
            return lastData;
        }

        public static string GetSensor()
        {
            return "USA.SLTC.1.125.PM";
        }
    }
}
