# OMF Ingress .NET Samples

**Version:** 1.2.4

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/ADH/aveva.sample-adh-omf_ingress-dotnet?branchName=main)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=2620&branchName=main)

## Scope of Sample

This sample is intended to show how to build out the OMF Ingress connection in ADH programmatically using the DotNet NuGet library. The starting point of this sample assumes your OMF Ingress is not configured. It does show sending OMF data, but that is to show that the programmatic OMF configuration works. A typical OMF app would assume that the OMF ingress is already configured (as this is a one time configuration action). To learn about OMF application development and see samples of typcial OMF applications please go to our [OMF Repository](https://github.com/osisoft/OSI-Samples-OMF).

## Building a Client with the Ingress Client Libraries

The sample described in this section makes use of the AVEVA Ingress Client Libraries. When working in .NET, it is recommended that you use these libraries. The libraries are available as NuGet packages. The packages used are:

- OSIsoft.Omf
- OSIsoft.OmfIngress
- OSIsoft.Identity.AuthenticationHandler

The libraries offer a framework of classes that make client development easier.

## Configure constants for connecting and authentication

The sample is configured using the file [appsettings.placeholder.json](OmfIngressClientLibraries/appsettings.placeholder.json). Before editing, rename this file to `appsettings.json`. This repository's `.gitignore` rules should prevent the file from ever being checked in to any fork or branch, to ensure credentials are not compromised.

The OMF Ingress Service is secured by obtaining tokens from the Identity Server. Such clients provide a client application identifier and an associated secret (or key) that are authenticated against the server. The sample includes an `appsettings.json` configuration file to hold configuration strings, including the authentication strings. You must replace the placeholders with the authentication-related values you received from AVEVA. The application requires two Client Credential Clients, one to manage OMF Ingress connections and one to send data from a mock device. For information on how to obtain these client IDs and secrets, see the [Client Credential Client Documentation](https://ocs-docs.osisoft.com/Content_Portal/Documentation/Identity/Identity_ClientCredentialClient.html).

```json
{
  "TenantId": "PLACEHOLDER_REPLACE_WITH_TENANT_ID",
  "NamespaceId": "PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID",
  "Resource": "https://uswe.datahub.connect.aveva.com", //This is the base address, NOT the OMF endpoint.
  "ClientId": "PLACEHOLDER_REPLACE_WITH_CLIENT_IDENTIFIER", //This is the client to connect to the OMF Ingress Services.
  "ClientSecret": "PLACEHOLDER_REPLACE_WITH_CLIENT_SECRET",
  "DeviceClientId": "PLACEHOLDER_REPLACE_WITH_DEVICE_CLIENT_ID", //This is the client that will be used to send OMF data. Make sure a connection hasn't been made for this client yet.
  "DeviceClientSecret": "PLACEHOLDER_REPLACE_WITH_DEVICE_CLIENT_SECRET",
  "ConnectionName": "PLACEHOLDER_REPLACE_WITH_CONNECTION_NAME",
  "StreamId": "PLACEHOLDER_REPLACE_WITH_STREAM_ID"
}
```

The authentication values are provided to the `OSIsoft.Identity.AuthenticationHandler`. The AuthenticationHandler is a DelegatingHandler that is attached to an HttpClient pipeline.

## Other Configuration

The aforementioned `appsettings.json` file has placeholders for the names of the connection, as well as a client Id to map a device to the connection. You must fill in those values as well.

## Set up OmfIngressService

The example works through one interface:

- IOmfIngressService for for configuring OMF Connections and sending OMF Messages

The following code block illustrates how to configure the OmfIngressService to use throughout the sample:

```C#
AuthenticationHandler authenticationHandler = new AuthenticationHandler(address, clientId, clientSecret);

OmfIngressService baseOmfIngressService = new OmfIngressService(new Uri(address), HttpCompressionMethod.None, authenticationHandler);
IOmfIngressService omfIngressService = baseOmfIngressService.GetOmfIngressService(tenantId, namespaceId);
```

Note that the instance of the IOmfIngressService is scoped to a tenant and namespace. If you wish to work in a different tenant or namespace, you would need another instance scoped to that tenant and namespace.

## Clients

Devices sending OMF messages each need a clientId and clientSecret. The clientId is used route messages to the proper connection(s). ClientIds may be mapped to at most one connection per namespace. For more details on Clients see the [Client Credential Client Documentation](https://ocs-docs.osisoft.com/Content_Portal/Documentation/Identity/Identity_ClientCredentialClient.html).

## OMF Connections

 An OMF Connection is the connection that handles reading and handling OMF messages. We create the Connection by instantiating a new OmfConnectionCreate object:

```C#
OmfConnectionCreate omfConnectionCreate = new OmfConnectionCreate()
{
    Name = "REPLACE_WITH_CONNECTION_NAME",
    Description = "This is a sample Connection",
    ClientIds = new List<string>() { mappedClientId }
};
```

Then use the Ingress client to start the creation of the Client:

```C#
OmfConnection omfConnection = await omfIngressService.BeginCreateOmfConnectionAsync(omfConnectionCreate).ConfigureAwait(false);
```

After initiating creation, we can query for the connection and check the status until it is Active:

```C#
using (CancellationTokenSource cancel = new CancellationTokenSource(_timeout))
{
    while (!cancel.IsCancellationRequested && !omfConnection.State.Equals("Active"))
    {
        omfConnection = await _omfIngressService.GetOmfConnectionAsync(omfConnection.Id).ConfigureAwait(false);
        Task.Delay(1000).Wait();
    }

    if (cancel.IsCancellationRequested)
    {
        throw new Exception("Omf Connection creation timeout");
    }
}
```

A cancellation token is used to ensure that the action never excedes the value _timeout.

## Send OMF Messages

OMF messages sent to ADH are translated into objects native to the Sequential Data Store. In this example, we send an OMF Type message which creates an SDS type in the data store, an OMF Container message which creates an SDS stream, and then send OMF Data messages, which use the containerId in the message body to route the data to the SDS stream. Refer to the data store documentation for how to view the types/streams/data in SDS. For each type of message, we first construct the message body using the OMF library:

```C#
OmfTypeMessage typeMessage = OmfMessageCreator.CreateTypeMessage(typeof(DataPointType));

OmfContainerMessage containerMessage = OmfMessageCreator.CreateContainerMessage(streamId, typeof(DataPointType));

DataPointType dataPoint = new DataPointType() { Timestamp = DateTime.UtcNow, Value = rand.NextDouble() };
OmfDataMessage dataMessage = OmfMessageCreator.CreateDataMessage(streamId, dataPoint);
```

Then the devices uses its own ingress client, which uses the device clientId and clientSecret to authenticate the requests. The device clientId is used to route the message to the Connection that the clientId is mapped to.

```C#
var serializedMessage = OmfMessageSerializer.Serialize(omfMessage);
await deviceOmfIngressService.SendOMFMessageAsync(serializedMessage);
```

## Cleanup: Deleting OMF Connections

In order to prevent unused resources from being left behind, this sample performs some cleanup before exiting.

Deleting Containers and Types can be achieved by constructing the same OMF messages, but instead specifying the Delete action:

```C#
OmfTypeMessage typeMessage = OmfMessageCreator.CreateTypeMessage(typeof(DataPointType));
typeMessage.ActionType = ActionType.Delete;

OmfContainerMessage containerMessage = OmfMessageCreator.CreateContainerMessage(streamId, typeof(DataPointType));
containerMessage.ActionType = ActionType.Delete;
```

Then serialize the message and send as shown in the prior section.

Deleting an OMF Connection can be achieved using the Ingress client and passing the corresponding object Id:

```C#
await _omfIngressService.BeginDeleteOmfConnectionAsync(omfConnection.Id).ConfigureAwait(false);
```

After beginning the deletion, we can continuously check the list of OMF Connections until it no longer contains our omfConnection:

```C#
using (CancellationTokenSource cancel = new CancellationTokenSource(_timeout))
{
    bool deleted = false;
    while (!deleted)
    {
        OmfConnections omfConnections = await _omfIngressService.GetOmfConnectionsAsync().ConfigureAwait(false);
        bool found = false;
        foreach (OmfConnection connection in omfConnections.Results)
        {
            if (string.Equals(connection.Id, omfConnection.Id, StringComparison.InvariantCultureIgnoreCase))
            {
                deleted = connection.State.Equals("Deleted");
                found = true;
            }
        }

        if (!found)
        {
            deleted = true;
        }

        Task.Delay(1000).Wait();
    }

    if (cancel.IsCancellationRequested)
    {
        throw new Exception("Omf Connection deletion timeout");
    }
}
```

A cancellation token is used to ensure that the action never excedes the value _timeout.

## Steps to run this sample

Replace the placeholders in the `appsettings.json` file with your TenantId, NamespaceId, ClientId, ClientSecret, DeviceClientId, DeviceClientSecret, ConnectionName and the StreamId.

### Requirements

- .NET 6.0 or later
- Reliable internet connection

### Using Visual Studio

- Load the .csproj
- Rebuild project
- Run it

### Command Line

- Make sure you have the install location of dotnet added to your path
- Run the following command from the location of this project:

```shell
dotnet restore
dotnet run
```

- To run the tests, first make sure to change the current folder to the folder with OmfIngressClientLibrariesTests.csproj

```shell
dotnet restore
dotnet test
```

---

For the main ADH page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main AVEVA samples page [ReadMe](https://github.com/osisoft/OSI-Samples)
