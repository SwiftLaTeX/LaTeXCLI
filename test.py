import requests
jsond = {
    'main': "main.tex",
    'resources': [
        {
            'name':'main.tex',
            'url':'https://www3.nd.edu/~powers/ame.20231/sample.tex',
            'use_cache':'yes'
        },
        {
            'name':'sample.figure.eps',
            'url':'https://www3.nd.edu/~powers/ame.20231/sample.figure.eps',
            'use_cache':'yes'
        }
    ],
    'mode': 'simple'
}
r = requests.post('http://127.0.0.1:5000/compiler', json=jsond)
print(r.text)