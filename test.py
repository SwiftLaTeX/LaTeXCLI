import requests
jsond = {
    'main': "main.tex",
    'session':'JkYAUfNnjx8w80nUYH51vteAbhSNCu8o',
    'resources': [
        {
            'name':'main.tex',
            'url':'https://www3.nd.edu/~powers/ame.20231/sample.tex',
            'modified_time':1300,
        },

    ],
    'mode': 'simple'
}
r = requests.post('http://130.216.216.198/compiler', json=jsond)
print(r.text)