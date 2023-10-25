def image_to_text_example(api_url: str) -> [str, str, str]:
    python_code = f"""
    import requests
    
    API_URL = "{api_url}"
    
    def query(filename):
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, data=data)
        return response.json()
    
    output = query("cats.jpg")
    print(output)
       """

    curl_code = f"""
       curl  {api_url} \\
            -X POST \\
            --data-binary '@cats.jpg'
       """

    js_code = f"""
        async function query(filename) {{
            const data = fs.readFileSync(filename);
            const response = await fetch(
                "{api_url}",
                {{
                    method: "POST",
                    body: data,
                }}
            );
            const result = await response.json();
            return result;
        }}

        query("cats.jpg").then((response) => {{
            console.log(JSON.stringify(response));
        }});
       """

    return python_code, js_code, curl_code


def asr_example(api_url: str) -> [str, str, str]:
    python_code = f"""
    import requests

    API_URL = "{api_url}"
    def query(filename):
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, data=data)
        return response.json()
    
    output = query("sample1.flac")
    print(output)
       """

    curl_code = f"""
       curl  {api_url}  \\
        -X POST \\
        --data-binary '@sample1.flac'
       """

    js_code = f"""
        async function query(filename) {{
            const data = fs.readFileSync(filename);
            const response = await fetch(
                "{api_url}",
               {{
                    method: "POST",
                    body: data,
                }}
            );
            const result = await response.json();
            return result;
        }}
        
        query("sample1.flac").then((response) => {{
            console.log(JSON.stringify(response));
        }});
       """

    return python_code, js_code, curl_code


def text_speech_example(api_url: str) -> [str, str, str]:
    python_code = f"""
    import requests
    
    API_URL = "{api_url}"
    
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    output = query({{
        "inputs": "The answer to the universe is 42",
    }})
    print(output)
       """

    curl_code = f"""
       curl {api_url} \\
        -X POST \\
        -d '{"inputs": "The answer to the universe is 42"}' \\
        -H 'Content-Type: application/json'
       """

    js_code = f"""
       async function query(data)  {{
            const response = await fetch(
                 "{api_url}",
                {{
                    method: "POST",
                    body: JSON.stringify(data),
                }}
            );
            const result = await response.json();
            return result;
        }}
        
        query({"inputs": "The answer to the universe is 42"}).then((response) =>  {{
            console.log(JSON.stringify(response));
        }});
       """

    return python_code, js_code, curl_code
