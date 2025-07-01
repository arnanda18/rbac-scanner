import requests, argparse

GREEN = '\033[32m'
RESET = "\033[0m"
YELLOW = "\033[33m"
RED = "\033[31m"
BLUE = "\033[34m"
CYAN = "\033[36m"

def banner():
    banner = f"""{GREEN}
        .########..########.....###.....######...........######...######.....###....##....##.##....##.########.########.
        .##.....##.##.....##...##.##...##....##.........##....##.##....##...##.##...###...##.###...##.##.......##.....##
        .##.....##.##.....##..##...##..##...............##.......##........##...##..####..##.####..##.##.......##.....##
        .########..########..##.....##.##.......#######..######..##.......##.....##.##.##.##.##.##.##.######...########.
        .##...##...##.....##.#########.##.....................##.##.......#########.##..####.##..####.##.......##...##..
        {GREEN}.##....##..##.....##.##.....##.##....##.........##....##.##....##.##.....##.##...###.##...###.##.......##....##.
        .##.....##.########..##.....##..######...........######...######..##.....##.##....##.##....##.########.##.....##{RESET}

        {BLUE}################################################################################################################

                                                  Created by: {RED}@yasaid
                                                    {BLUE}Version: 1.0
                                                  {BLUE}Github: {RED}@arnanda18
                                                {BLUE}Email: {RED}yasaid@gmail.com{BLUE}
        
        ----------------------------------------------------------------------------------------------------------------

        {RESET}RBAC-Enum is a tool used for penetration testing of Role-Based Access Control (RBAC) to assess whether an API has
        properly implemented access control lists. It is primarily used during the reconnaissance phase to identify access
        control weaknesses or Insecure Direct Object References (IDOR) vulnerabilities in API endpoints.By utilizing a custom
        wordlist, RBAC-Enum scans all possible access scenarios and analyzes response messages from the target system to
        detect potential vulnerabilities. To contribute more for this open source tools and to enhance that see at  
        {YELLOW}https://github.com/arnanda18/rbac-scanner{RESET}

        Usage: python rbacenum.py -u https://example.com -U user -p password -w /path/to/file/wordlist -x POST
        
        Option:
            -h,    --help       To show command help list option and how this command works. 

    """
    print(banner)

def help():
    help=""""
    Usage: python rbacenum.py -u https://example.com -U user -p password -w /path/to/file/wordlist -x POST
        Option:
        -u, --url for login, can different with a -d option or api target, some application maybe have same a url for login and the target they want pentest.
        -U, --user The user of to use log in to the application
        -p, --password The credentials of user
        -w, --wordlist The list of endpoint to the pentest or try to test with RBAC
        -d, --domain The domain target want to pentest
        -x, --request method that want to use send request to the target.

        ----------------------------------------------------------------------------------------------------------------
        ................................................................................................................
    """

    print(help)

def getParams():
    parser = argparse.ArgumentParser(description="Command line tools option")

    parser.add_argument('-u', '--url', required=False, help="The URL of the API endpoint or web application")
    parser.add_argument('-U', '--user', required=False, help="The user of to use log in to the application")
    parser.add_argument('-p', '--password', required=False, help="The credentials of user")
    parser.add_argument('-w', '--wordlist', required=False, help="The list of endpoint to the pentest or try to test with RBAC")
    parser.add_argument('-d', '--api', required=False, help="The domain api/website target want to pentest")
    parser.add_argument('-x', '--request_method', required=True, help="The request method that you will use to send a request to the API server.")

    args = parser.parse_args()
    return args.url, args.user, args.password, args.api, args.request_method, args.wordlist
    
url, user, password, api, request_method, wordlist = getParams()

def auth(url, user, password):
    url = url   
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "username": user,
        "password": password
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            data = data.get("data")
            if data:
                token = data.get("token")
                return token
            else:
                print("Token not found!")
        else:
            print(f"[Auth] - Login failed! {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# banner()
token = f"{auth(url, user, password)}"

# print(token)

def get_request(token, api, w):

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "token": token
    }

    try:
        response = requests.get(api, headers=headers)
        status_code = response.status_code
        if status_code == 200:
            color = GREEN  # Green
        elif status_code == 404:
            color = YELLOW  # Yellow
        elif status_code == 403:
            color = RED  # Red
        else:
            color = CYAN  # Cyan
        try:
            data = response.json()
            data = data.get("message")
            r = f"""{color}[ * ]   {status_code}{RESET} -- {data} on target {CYAN}{w}"""
            print(r)
        except ValueError as e:
            print(f"{color}[ * ]   {status_code}{RESET} -- Url not found on target {CYAN}{w}")           
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def post_request(token, url, w):

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "token": f"{token}"
    }

    payload = {
        "null": "null"
    }

    try:
        response = requests.get(url, json=payload, headers=headers)
        status_code = response.status_code
        if status_code == 200:
            color = GREEN  # Green
        elif status_code == 404:
            color = YELLOW  # Yellow
        elif status_code == 403:
            color = RED  # Red
        else:
            color = CYAN  # Cyan
        try:
            data = response.json()
            data = data.get("message")
            r = f"""{color}[ * ]   {status_code}{RESET} -- {data} on target {CYAN}{w}"""
            print(r)
        except ValueError as e:
            print(f"{color}[ * ]   {color}{status_code}{RESET} -- url not found on target {CYAN}{w}")  
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def scanning(wordlist, method, token, api):
    with open(f"{wordlist}", "r", encoding="utf-8") as file:
        print(f"{BLUE}[ + ] RBAC Scanner has been started ......{RESET}")
        for w in file:
            w = w.strip()
            endpoint = f"{api}{w}"
            if method == 'GET':
                get_request(token, endpoint, w)
            else:
                post_request(token, endpoint, w)

banner()                
scanning(wordlist, request_method, token, api)
# get_request(token, api) // disable for testing
#post_request(token, api)
