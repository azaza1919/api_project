from mistralai.client import Mistral

def mail_promt(text, api_key):
    if not text:
        return 'empty'
        
    client = Mistral(api_key=api_key)
    
    prompt = f'напиши краткое содержание(1-2 предложения) письма:\n\n{text}'
    
    response = client.chat.complete(
        model= 'mistral-tiny',
        messages=[{
            'role': 'user', 
            'content': prompt
        }]
    )
    
    return response.choices[0].message.content