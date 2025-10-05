from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
import os

def index(request):
    return render(request, 'generator/index.html')

def generate_content(request):
    if request.method == 'POST':
        content_type = request.POST.get('type')
        topic = request.POST.get('topic')
        tone = request.POST.get('tone')
        word_count = request.POST.get('word_count')

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = f"Write a {tone} {content_type} about '{topic}' in around {word_count} words."

        try:
            response = client.responses.create(model="gpt-4.1-mini", input=prompt)
            result = response.output[0].content[0].text
            return JsonResponse({'result': result})
        except Exception as e:
            return JsonResponse({'error': str(e)})
