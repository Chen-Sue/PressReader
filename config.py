import json

url_login = "http://ezproxy.lb.polyu.edu.hk/login?url=https://www.pressreader.com/"

add_experimental_option = {
    'detach': True,
    'excludeSwitches': ['enable-automation'],
    'excludeSwitches': ['enable-logging'],
    'useAutomationExtension': False,
    "appState": {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local"
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }  
}

add_option = {'printing.print_preview_sticky_settings': json.dumps(add_experimental_option)}

executable_path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

key_words = 'Evergrande'
