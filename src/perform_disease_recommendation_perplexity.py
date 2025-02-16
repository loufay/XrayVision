import requests

def perform_disease_recommendation_perplexity(message):

    api_key = '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'
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "max_tokens": 600,
        "temperature": 0.2,
        "top_p": 0.9,
        "search_domain_filter": None,
        "return_images": False,
        "return_related_questions": False,
        # "search_recency_filter": "<string>",
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1,
        "response_format": None
    }
    headers = {
        "Authorization": "Bearer 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",
        # "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.json()['choices'][0]['message']['content'])

    return response.json()['choices'][0]['message']['content']


