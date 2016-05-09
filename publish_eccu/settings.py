import os

assert 'AKAMAI_USER' in os.environ, "AKAMAI_USER must be set"
assert 'AKAMAI_PASSWORD' in os.environ, "AKAMAI_PASSWORD must be set"
assert 'AKAMAI_HOST' in os.environ, "AKAMAI_HOST must be set"
assert 'AKAMAI_NOTIFY' in os.environ, "AKAMAI_NOTIFY must be set"

AKAMAI_USER = os.environ.get('AKAMAI_USER')
AKAMAI_PASSWORD = os.environ.get('AKAMAI_PASSWORD')
AKAMAI_NOTIFY = os.environ.get('AKAMAI_NOTIFY')
AKAMAI_ENDPOINT = 'https://control.akamai.com/webservices/services/PublishECCU'

# Downloaded from https://control.akamai.com/webservices/services/PublishECCU?wsdl
WSDL_PATH = 'file://%s' % os.path.join(os.path.dirname(__file__), 'PublishECCU.wsdl')
try:
    from settings_local import *
except ImportError:
    pass
