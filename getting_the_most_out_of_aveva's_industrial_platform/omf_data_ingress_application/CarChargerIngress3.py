from ADHOMFClient import *
from ChargerDataClient import ChargerDataClient, ChargerData
from collections import deque
from concurrent.futures import ProcessPoolExecutor
import json
import logging
from multiprocessing import Process
import os
import threading


# Logging Settings
level = logging.INFO
log_file_name = 'logfile.txt'

# Data Sending Settings
send_period = 30        # maximum time to wait before sending the next OMF data message
max_events = 17000      # maximum number of events to send per OMF data message
max_queue_len = 100000
max_processes = min(os.cpu_count(), 4)
max_threads_per_process = 5


def getAppsettings():
    """Open and parse the appsettings.json file"""

    # Try to open the configuration file
    try:
        with open(
            'appsettings.json',
            'r',
        ) as f:
            appsettings = json.load(f)
    except Exception as error:
        logging.ERROR(f'Error: {str(error)}')
        logging.ERROR(f'Could not open/read appsettings.json')
        exit()

    return appsettings


def send(omf_client: ADHOMFClient, queue: deque):
    payload = {}
    for _ in range(max_events):
        if len(queue) == 0:
            continue

        event: ChargerData = queue.pop()
        if event.Id not in payload:
            payload[event.Id] = [
                {'Timestamp': event.Timestamp, 'Value': event.Value}]
        else:
            payload[event.Id].append(
                {'Timestamp': event.Timestamp, 'Value': event.Value})

    payload = [{'containerid': id, 'values': values}
               for id, values in payload.items()]

    response = omf_client.retryWithBackoff(
        omf_client.omfRequest, 10, OMFMessageType.Data, OMFMessageAction.Create, payload)
    omf_client.verifySuccessfulResponse(response, 'Error sending data')


def threadManager(appsettings, thread_partition):
    omf_client = ADHOMFClient(
        appsettings.get('Resource'),
        appsettings.get('ApiVersion'),
        appsettings.get('TenantId'),
        appsettings.get('NamespaceId'),
        appsettings.get('Clients')[0].get('ClientId'),
        appsettings.get('Clients')[0].get('ClientSecret'),
        logging_enabled=True
    )

    charger_data_client = ChargerDataClient()

    queue = deque(maxlen=max_queue_len)
    timer = time.time()
    while True:
        for stream in thread_partition:
            queue.extendleft(charger_data_client.getData(stream.get('id')))

            while len(queue) >= max_events or time.time() - timer > send_period:
                send(omf_client, queue)
                timer = time.time()

            time.sleep(1)


def processManager(appsettings, process_partition):
    # *************************************************************************
    # Split streams again into different threads to further improve performance
    # *************************************************************************
    thread_partitions = []
    for i in range(0, len(process_partition), int(len(process_partition)/max_threads_per_process)):
        thread_partitions.append(
            process_partition[i:i + int(len(process_partition)/max_threads_per_process)])

    threads = []
    for thread_partition in thread_partitions:
        thread = threading.Thread(target=threadManager, args=(
            appsettings, thread_partition))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def main():
    appsettings = getAppsettings()

    # Create clients
    omf_client = ADHOMFClient(
        appsettings.get('Resource'),
        appsettings.get('ApiVersion'),
        appsettings.get('TenantId'),
        appsettings.get('NamespaceId'),
        appsettings.get('Clients')[0].get('ClientId'),
        appsettings.get('Clients')[0].get('ClientSecret'),
        logging_enabled=True
    )

    charger_data_client = ChargerDataClient()

    # Get or create types in data hub
    response = omf_client.omfRequest(
        OMFMessageType.Type, OMFMessageAction.Create, charger_data_client.getTypes())
    omf_client.verifySuccessfulResponse(response, 'Error creating types')

    # Get or create streams from data source in data hub
    streams = charger_data_client.getStreams()
    response = omf_client.omfRequest(
        OMFMessageType.Container, OMFMessageAction.Create, streams)
    omf_client.verifySuccessfulResponse(response, 'Error creating containers')

    # Split streams into different partitions to improve performance
    process_partitions = []
    for i in range(0, len(streams), int(len(streams)/max_processes)):
        process_partitions.append(
            streams[i:i + int(len(streams)/max_processes)])

    processes = []
    for process_partition in process_partitions:
        process = Process(target=processManager, args=(
            appsettings, process_partition))
        processes.append(process)
        process.start()

    while all([process.is_alive() for process in processes]):
        if input('Type "exit" to quit application: ').casefold() == 'exit':
            break

    for process in processes:
        process.terminate()


if __name__ == "__main__":

    # Set up the logger
    logging.basicConfig(filename=log_file_name, encoding='utf-8', level=level, datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(module)16s,line: %(lineno)4d %(levelname)8s | %(message)s')

    main()
