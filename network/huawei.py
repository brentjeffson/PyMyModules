import requests
import xml.etree.ElementTree as xml

TRAFFIC_API = 'api/monitoring/traffic-statistics'
STATUS_API = 'api/monitoring/status'

class InvalidSessionIDError(Exception):
    '''Raised when SessionID being used is invalid
        Args:
            msg (str): Human readable string describing the exception

        Attributes:
            msg (str): Human readable string describing the exception
    '''
    pass
    # def __init__(self, msg):
    
    #     self.msg


class Response():
    pass

class HuaweiApi():
    
    def __init__(self, session_id=None, base_url='http://192.168.8.1/'):
        '''API used to get information from huawei pocket wifi.'''
        self._session_id = session_id
        self.base_url = base_url
        self.session = requests.Session()
        session_id = HuaweiApi._get_session_id()
        if session_id is not None: 
            self.session_id = session_id
    
    def get_traffic(self):
        return self._get_info(TRAFFIC_API)

    def get_status(self):
        return self._get_info(STATUS_API)

    def _get_info(self, api, headers={}):
        '''Get response from the api
            Args:
                api (str): API to get response from.

            Raises:
                InvalidSessionIDError: Invalid/Unusable Session ID was provided

            Returns:
                response (Response): Contains meta of requested API
        '''
        response = Response()
        
        try:
            resp = self.session.get(self.base_url + api, headers=headers)
            
            if resp.ok: 
                root = xml.fromstring(resp.text)

                for child in root:
                    setattr(response, child.tag, child.text)
                return response
        except Exception as e:
            print(e)
            raise

    def _get_session_id():
        try:
            resp = requests.get('http://192.168.8.1/html/home.html')
            if 'set-cookie' in resp.headers:
                return resp.headers['set-cookie']
        except Exception as e:
            print(e)
            return None
        return None

    def __str__(self):
        return self.session.cookies
        
    @property
    def session_id(self):
        return None

    @session_id.setter
    def session_id(self, id):
        '''Sets the instance `session id` to a new `id`'''
        self.session.headers.update({'cookie': id})

    