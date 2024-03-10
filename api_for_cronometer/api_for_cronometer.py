"""Main module."""

import requests

from ._headers import headers
from .gwt_permutation import gwt_permutation

# Set the URL
URL = 'https://cronometer.com/cronometer/app'

# Define the data to be sent
DATA = '7|0|9|https://cronometer.com/cronometer/|824B7904836FCC05F569A1658372CCCC|' \
    'com.cronometer.shared.rpc.CronometerService|setTarget|java.lang.String/2004016611|' \
    'com.cronometer.shared.targets.models.Target/3515640666|I|acdb03e9d07755322983c2be6e10b2b3|' \
    'java.lang.Double/858496421|1|2|3|4|3|5|6|7|8|6|1|9|22.0|-2|606|0|2895737|'


def update_macro_target(requests_session: requests.Session,
                        macro: str, target: str, max_: str) -> None:
    if macro != 'saturated':
        raise NotImplementedError(f"implement {macro} {target} {max_}")
    request_headers = headers.copy()
    # content-type: text/x-gwt-rpc; charset=UTF-8'
    request_headers['content-type'] = 'text/x-gwt-rpc; charset=UTF-8'
    # https://stackoverflow.com/questions/2609834/gwt-rpc-does-it-do-enough-to-protect-against-csrf
    request_headers['x-gwt-module-base'] = 'https://cronometer.com/cronometer/'
    request_headers['x-gwt-permutation'] = gwt_permutation()

    response = requests_session.post(URL, headers=request_headers, data=DATA)
    print(response.text)
