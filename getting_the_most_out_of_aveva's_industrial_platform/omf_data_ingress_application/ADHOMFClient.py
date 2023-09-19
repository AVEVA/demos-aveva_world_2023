from __future__ import annotations

from OMFClient import *
from Authentication import Authentication


class ADHOMFClient(OMFClient):
    """Handles communication with PI OMF Endpoint."""

    def __init__(self, resource: str, api_version: str, tenant_id: str, namespace_id: str, client_id: str = None,
                 client_secret: str = None, omf_version: str = '1.2', logging_enabled: bool = False):
        self.__resource = resource
        self.__api_version = api_version
        self.__tenant_id = tenant_id
        self.__namespace_id = namespace_id
        self.__omf_version = omf_version
        self.__logging_enabled = logging_enabled
        self.__full_path = f'{resource}/api/{api_version}/Tenants/{tenant_id}/Namespaces/{namespace_id}'

        if (client_id is not None):
            self.__auth_object = Authentication(
                tenant_id, resource, client_id, client_secret)
            self.__auth_object.getToken()
        else:
            self.__auth_object = None

        super().__init__(self.FullPath, omf_version, True, logging_enabled)

    @property
    def Resource(self) -> str:
        """
        Gets the base url
        :return:
        """
        return self.__resource

    @property
    def ApiVersion(self) -> str:
        """
        Returns just the base api versioning information
        :return:
        """
        return self.__api_version

    @property
    def TenantId(self) -> str:
        """
        Returns the tenant ID
        :return:
        """
        return self.__tenant_id

    @property
    def NamespaceId(self) -> str:
        """
        Returns the namespace ID
        :return:
        """
        return self.__namespace_id

    @property
    def OmfVersion(self) -> str:
        """
        Returns the omf version
        :return:
        """
        return self.__omf_version

    @property
    def FullPath(self) -> bool:
        return self.__full_path

    @property
    def LoggingEnabled(self) -> bool:
        return self.__logging_enabled

    @LoggingEnabled.setter
    def LoggingEnabled(self, value: bool):
        self.__logging_enabled = value

    def _getToken(self) -> str:
        """
        Gets the bearer token
        :return:
        """
        return self.__auth_object.getToken()

    def getHeaders(self, message_type: OMFMessageType, action: OMFMessageAction):
        headers = super().getHeaders(message_type, action)
        headers['authorization'] = f'Bearer {self._getToken()}'
        return headers