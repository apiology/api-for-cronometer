import http.client as http_client
import logging
import os

import mechanize
import requests

from ._headers import headers

url = 'https://cronometer.com/login'

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


def login() -> requests.Session:
    """Login to the server."""
    br = mechanize.Browser()
    br.open("https://cronometer.com/login/")
    br.select_form(nr=0)
    br.form['username'] = os.environ['CRONOMETER_USERNAME']
    br.form['password'] = os.environ['CRONOMETER_PASSWORD']
    # https://api.jquery.com/serialize/
    # serialize form elements like jquery .serialize() would

    http_client.HTTPConnection.debuglevel = 1

    mechanize_url, urlencoded_get_data, mechanize_headers = br.form.click_request_data()

    # # grab cookies from mechanize
    mechanize_cookiejar = br._ua_handlers['_cookies'].cookiejar
    print("mechanize_cookiejar: {}".format(mechanize_cookiejar))
    # # convert to requests cookies
    requests_cookiejar = requests.utils.cookiejar_from_dict(
        requests.utils.dict_from_cookiejar(mechanize_cookiejar))
    print("requests_cookiejar: {}".format(requests_cookiejar))
    # set cookies in requests
    requests_session = requests.Session()
    requests_session.cookies = requests_cookiejar
    # # set headers in requests
    # requests_session.headers = mechanize_headers

    print("Serialized form data: {}".format(urlencoded_get_data))
    login_headers = headers.copy()
    print("mechanize headers: {}".format(mechanize_headers))
    # use requests to get response

    # Set Content-Type = application/x-www-form-urlencoded
    login_headers['Content-Type'] = 'application/x-www-form-urlencoded'

    response = requests_session.post(url, headers=login_headers, data=urlencoded_get_data)

    if 'redirect' in response.json():
        print("Successfully logged in")
        return requests_session
    else:
        print(f"Response: {response}")
        print(f"Response cookies: {response.cookies}")
        print(f"Response data: {response.text}")
        raise Exception("Login failed")
