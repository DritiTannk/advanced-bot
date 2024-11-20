import json
from datetime import datetime

from django.views import View
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# from .models import BotResponse
# from .utils import predict_entities, text_to_speech

class HomeView(View):
    template_name = 'home.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {"curr_time": datetime.now().strftime("%H:%M")}
                      )


# @csrf_exempt
# def send_message(request): # User Question and Answer to front end connection point
#     if request.method == 'POST':
#         sender = request.POST['sender']
#         content = request.POST['content']
#
#         prediction = predict_entities(content)
#
#         b_instance = BotResponse.objects.create(sender=sender,
#                                                 user_msg=content,
#                                                 response=prediction
#                                                 )
#         text_to_speech(prediction, b_instance)
#
#
#         return HttpResponse(json.dumps({'content': json.dumps(prediction),
#                                         'audio_path': b_instance.polly_file.url,
#                                         'status': 200
#                                         }),
#                             content_type='application/json'
#                             )
