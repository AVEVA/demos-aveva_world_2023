from __future__ import annotations
from enum import Enum
import gzip
import json
import logging
import requests
import time
from typing import Any


class OMFMessageType(Enum):
    """
    enum 0-2
    """
    Type = 'Type'
    Container = 'Container'
    Data = 'Data'


class OMFMessageAction(Enum):
    """
    enum 0-2
    """
    Create = 'Create'
    Update = 'Update'
    Delete = 'Delete'


class OMFClient(object):
    """Handles communication with PI OMF Endpoint."""

    def __init__(self, url: str, omf_version: str = '1.2', verify_ssl: bool = True, logging_enabled: bool = False):
        self.__url = url
        self.__omf_version = omf_version
        self.__verify_ssl = verify_ssl
        self.__logging_enabled = logging_enabled
        self.__omf_endpoint = f'{url}/omf'
        self.__session = requests.Session()

    @property
    def Url(self) -> str:
        """
        Gets the base url
        :return:
        """
        return self.__url

    @property
    def OMFVersion(self) -> str:
        """
        Gets the omf version
        :return:
        """
        return self.__omf_version

    @property
    def VerifySSL(self) -> bool:
        """
        Gets whether SSL should be verified
        :return:
        """
        return self.__verify_ssl

    @property
    def LoggingEnabled(self) -> bool:
        """
        Whether logging is enabled (default False)
        :return:
        """
        return self.LoggingEnabled

    @LoggingEnabled.setter
    def logging_enabled(self, value: bool):
        self.LoggingEnabled = value

    @property
    def OMFEndpoint(self) -> str:
        """
        Gets the omf endpoint
        :return:
        """
        return self.__omf_endpoint

    def verifySuccessfulResponse(self, response, main_message: str, throw_on_bad: bool = True):
        """
        Verifies that a response was successful and optionally throws an exception on a bad response
        :param response: Http response
        :param main_message: Message to print in addition to response information
        :param throw_on_bad: Optional parameter to throw an exception on a bad response
        """

        # response code in 200s if the request was successful!
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            if self.__logging_enabled:
                logging.info(
                    f'request executed in {response.elapsed.microseconds / 1000}ms - status code: {response.status_code}')
                logging.debug(
                    f'{main_message}. Response: {response.status_code} {response.text}.')

            if throw_on_bad:
                raise Exception(
                    f'{main_message}. Response: {response.status_code} {response.text}. ')

    def getHeaders(self, message_type: OMFMessageType, action: OMFMessageAction):
        return {
            'messagetype': message_type.value,
            'action': action.value,
            'messageformat': 'JSON',
            'omfversion': self.OMFVersion,
            'compression': 'gzip',
            'x-requested-with': 'xmlhttprequest'
        }

    def omfRequest(self, message_type: OMFMessageType, action: OMFMessageAction, omf_message_json: dict[str, Any] | list[dict[str, Any]]) -> requests.Response:
        """
        Base OMF request function
        :param message_type: OMF message type
        :param action: OMF action
        :param omf_message_json: OMF message
        :return: Http response
        """

        msg_body = gzip.compress(bytes(json.dumps(omf_message_json), 'utf-8'))
        headers = self.getHeaders(message_type, action)

        return self.request(
            'POST',
            self.OMFEndpoint,
            headers=headers,
            data=msg_body,
            verify=self.VerifySSL,
            timeout=600
        )

    def request(self, method: str, url: str, params=None, data=None, headers=None, additional_headers=None, **kwargs) -> requests.Response:

        if not self.VerifySSL:
            print('You are not verifying the certificate of the end point. This is not advised for any system as there are security issues with doing this.')

            if self.__logging_enabled:
                logging.warning(
                    f'You are not verifying the certificate of the end point. This is not advised for any system as there are security issues with doing this.')

        # Start with the necessary headers for SDS calls, such as authorization and content-type
        if not headers:
            headers = self.getHeaders()

        # Extend this with the additional headers provided that either suppliment or override the default values
        # This allows additional headers to be added to the HTTP call without blocking the base header call
        if additional_headers:
            headers.update(additional_headers)

        if self.__logging_enabled:
            # Announce the url and method
            logging.info(f'executing request - method: {method}, url: {url}')

            # if debug level is desired, dump the payload and the headers (redacting the auth header)
            logging.debug(f'data: {data}')
            for header, value in headers.items():
                if header.lower() != "authorization":
                    logging.debug(f'{header}: {value}')
                else:
                    logging.debug(f'{header}: <redacted>')

        return self.__session.request(method, url, params=params, data=data, headers=headers, **kwargs)

    def retryWithBackoff(self, fn, max_retries, *args, **kwargs):
        success = False
        failures = 0
        while not success:
            response = fn(*args, **kwargs)
            if response.status_code == 504 or response.status_code == 503:
                if (failures >= 0 and failures >= max_retries):
                    logging.error('Server error. No more retries available.')
                    return response
                else:
                    timeout = 3600 if failures >= 12 else 2 ** failures
                    logging.warning('Server error. Retrying...')
                    time.sleep(timeout)
                    failures += 1
            else:
                success = True

        return response
