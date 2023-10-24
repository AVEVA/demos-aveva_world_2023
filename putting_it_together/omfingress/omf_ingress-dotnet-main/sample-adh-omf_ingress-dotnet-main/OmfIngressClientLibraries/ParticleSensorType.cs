using System;
using System.Threading.Tasks;
using OSIsoft.Omf;
using OSIsoft.Omf.DefinitionAttributes;
using Polly.Caching;

namespace OmfIngressClientLibraries
{

    [OmfType(Id = "ParticleSensorType", ClassificationType = ClassificationType.Dynamic)]
    public class ParticleSensorType
    {
        [OmfProperty(IsIndex = true)]
        public DateTime Timestamp { get; set; }
        [OmfProperty(Name = "Count0.3", Id = "Count0.3", Uom = "count")]
        public double Count03 { get; set; }
        [OmfProperty(Name = "Count0.5", Id = "Count0.5", Uom = "count")]
        public double Count05 { get; set; }
        [OmfProperty(Name = "Count1.0", Id = "Count1.0", Uom = "count")]
        public double Count10 { get; set; }
        [OmfProperty(Name = "Count2.5", Id = "Count2.5", Uom = "count")]
        public double Count25 { get; set; }
        [OmfProperty(Name = "Count5.0", Id = "Count5.0", Uom = "count")]
        public double Count50 { get; set; }
        [OmfProperty(Name = "Count10.0", Id = "Count10.0", Uom = "count")]
        public double Count100 { get; set; }
        [OmfProperty(Name = "PM1.0S", Id = "PM1.0S", Uom = "count")]
        public double PM10S { get; set; }
        [OmfProperty(Name = "PM1.0E", Id = "PM1.0E", Uom = "count")]
        public double PM10E { get; set; }
        [OmfProperty(Name = "PM2.5S", Id = "PM2.5S", Uom = "count")]
        public double PM25S { get; set; }
        [OmfProperty(Name = "PM2.5E", Id = "PM2.5E", Uom = "count")]
        public double PM25E { get; set; }
        [OmfProperty(Name = "PM10.0E", Id = "PM10.0E", Uom = "count")]
        public double PM100E { get; set; }
        [OmfProperty(Name = "PM10.0S", Id = "PM10.0S", Uom = "count")]
        public double PM100S { get; set; }


        internal static Random Rand = new Random();
        public static ParticleSensorType ReturnRandom()
        {
            return new()
            {
                Timestamp = DateTime.UtcNow,
                Count03 = GetNumber(),
                Count05 = GetNumber(),
                Count10 = GetNumber(),
                Count25 = GetNumber(),
                Count50 = GetNumber(),
                Count100 = GetNumber(),
                PM10S = GetNumber(),
                PM10E = GetNumber(),
                PM25S = GetNumber(),
                PM25E = GetNumber(),
                PM100S = GetNumber(),
                PM100E = GetNumber()
            };
        }

        public void AddRandom()
        {
            int bounds = 1;
            Timestamp = DateTime.UtcNow;
            Count03 += Rand.NextInt64(-bounds, bounds +1);
            Count05 += Rand.NextInt64(-bounds, bounds +1);
            Count10 += Rand.NextInt64(-bounds, bounds +1);
            Count25 += Rand.NextInt64(-bounds, bounds +1);
            Count50 += Rand.NextInt64(-bounds, bounds +1);
            Count100 += Rand.NextInt64(-bounds, bounds +1);
            PM10S += Rand.NextInt64(-bounds, bounds +1);
            PM10E += Rand.NextInt64(-bounds, bounds +1);
            PM25S += Rand.NextInt64(-bounds, bounds +1);
            PM25E += Rand.NextInt64(-bounds, bounds +1);
            PM100S += Rand.NextInt64(-bounds, bounds +1);
            PM100E += Rand.NextInt64(-bounds, bounds +1);

            if (Count03 < 0) Count03 = 0;
            if (Count05 < 0) Count05 = 0;
            if (Count10 < 0) Count10 = 0;
            if (Count25 < 0) Count25 = 0;
            if (Count50 < 0) Count50 = 0;
            if (Count100 < 0) Count100 = 0;
            if (PM10S < 0) PM10S = 0;
            if (PM10E < 0) PM10E = 0;
            if (PM25S < 0) PM25S = 0;
            if (PM25E < 0) PM25E = 0;
            if (PM100S < 0) PM100S = 0;
            if (PM100E < 0) PM100E = 0;
        }
        public ParticleSensorType AddRandomNew()
        {
            int bounds = 1;
            Timestamp = DateTime.UtcNow;
            ParticleSensorType newO = new ParticleSensorType()
            {
                Timestamp = DateTime.UtcNow,
                Count03 = Count03 + Rand.NextInt64(-bounds, bounds + 1),
                Count05 = Count05 + Rand.NextInt64(-bounds, bounds + 1),
                Count10 = Count10 + Rand.NextInt64(-bounds, bounds + 1),
                Count25 = Count25 + Rand.NextInt64(-bounds, bounds + 1),
                Count50 = Count50 + Rand.NextInt64(-bounds, bounds + 1),
                Count100 = Count100 + Rand.NextInt64(-bounds, bounds + 1),
                PM10S = PM10S + Rand.NextInt64(-bounds, bounds + 1),
                PM10E = PM10E + Rand.NextInt64(-bounds, bounds + 1),
                PM25S = PM25S + Rand.NextInt64(-bounds, bounds + 1),
                PM25E = PM25E + Rand.NextInt64(-bounds, bounds + 1),
                PM100S = PM100S + Rand.NextInt64(-bounds, bounds + 1),
                PM100E = PM100E + Rand.NextInt64(-bounds, bounds + 1)
            };

            if (newO.Count03< 0) newO.Count03 = 0;
            if (newO.Count05 < 0) newO.Count05 = 0;
            if (newO.Count10 < 0) newO.Count10 = 0;
            if (newO.Count25 < 0) newO.Count25 = 0;
            if (newO.Count50 < 0) newO.Count50 = 0;
            if (newO.Count100 < 0) newO.Count100 = 0;
            if (newO.PM10S < 0) newO.PM10S = 0;
            if (newO.PM10E < 0) newO.PM10E = 0;
            if (newO.PM25S < 0) newO.PM25S = 0;
            if (newO.PM25E < 0) newO.PM25E = 0;
            if (newO.PM100S < 0) newO.PM100S = 0;
            if (newO.PM100E < 0) newO.PM100E = 0;
            return newO;
        }

    public static double GetNumber()
        {
            return Rand.Next(100);
        }
    }
}
