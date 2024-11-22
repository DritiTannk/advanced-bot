import json
import uuid
from datetime import datetime

from django.views import View
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, UserChatHistory
from .utils import query_vdb, favourites_extraction, detect_fav_intent


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        token = str(uuid.uuid4())
        request.session['user_token'] = token

        return render(request, self.template_name,
                      {'user_token': token,
                       "curr_time": datetime.now().strftime("%H:%M")
                       })


def check_chat_exists(user_obj, user_quest):
    """
    This method checks whether past same chat exists or not.
    """
    past_chat = (UserChatHistory.objects.filter(user=user_obj, user_msg=user_quest)
                 .order_by('-created_at').first())

    return past_chat

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        user_name = request.POST.get('sender')
        user_token = request.POST.get('user_token')
        user_message = request.POST.get('content')

        # user fetch or creation
        user, _ = User.objects.get_or_create(user_name=user_name, session_id=user_token)

        # search existing records.
        past_chat = check_chat_exists(user, user_message)

        if not past_chat:
            user_chat = UserChatHistory.objects.create(user=user, user_msg=user_message)

            vec_res = query_vdb(user_message.strip().lower())

            if vec_res and vec_res["matches"]:
                intent_metadata = vec_res["matches"][0]["metadata"]
                intent = intent_metadata["intent"]
                bot_msg = intent_metadata["response"]

                # Handle intents
                if intent == "greet" or intent == "care":
                    user_chat.bot_resp = bot_msg
                    user_chat.save()

                    return HttpResponse(json.dumps({'content': bot_msg,
                                                    'status': 200
                                                    }),
                                        content_type='application/json'
                                        )

                elif intent == "introduce":
                    name = user.user_name
                    bot_resp = bot_msg.format(name=name)

                    user_chat.bot_resp = bot_msg
                    user_chat.save()

                    return HttpResponse(json.dumps({'content': bot_resp,
                                                    'status': 200
                                         }),
                                        content_type='application/json'
                                        )

                elif intent == "favourites":
                    user_fav_intent = detect_fav_intent(user_message)  # Identify the question intent
                    fav_ext_val = favourites_extraction(user_message)

                    # Save user's choices data as metadaata
                    if user.meta_data:
                        if user_fav_intent in user.meta_data:
                            if len(user.meta_data[user_fav_intent]) != 0:
                                user.meta_data[user_fav_intent].extend(fav_ext_val[user_fav_intent])
                            else:
                                user.meta_data[user_fav_intent] = fav_ext_val[user_fav_intent]
                    else:
                        user.meta_data = fav_ext_val

                    user.save()

                    user_fav_item = user.meta_data[user_fav_intent]
                    bot_resp = bot_msg.format(item=",".join(user_fav_item))
                    user_chat.bot_resp = bot_resp
                    user_chat.save()

                    return HttpResponse(json.dumps({'content': bot_resp,
                                                    'status': 200}),
                                        content_type='application/json'
                                        )

                elif intent == "dislikes":
                    user_quest_intent = detect_fav_intent(user_message)
                    dislike_ext_val = favourites_extraction(user_message)

                    if user and user.meta_data:
                        if user_quest_intent and user.meta_data.get(user_quest_intent):
                            user_prefer = user.meta_data.get(user_quest_intent)

                            if all(item in user_prefer for item in dislike_ext_val[user_quest_intent]):
                                return HttpResponse(json.dumps({'content': f"No, You like {','.join(user_prefer)}",
                                                                'status': 200}),
                                    content_type='application/json'
                                )
                            else:
                                bot_resp = bot_msg.format(item=",".join(dislike_ext_val[user_quest_intent]))
                                user_chat.bot_resp = bot_resp
                                user_chat.save()
                                return HttpResponse(json.dumps({'content': bot_resp,
                                                                'status': 200}),
                                                    content_type='application/json'
                                                    )

                elif intent == "ask_favorite":
                    query_intent = detect_fav_intent(user_message)

                    if user.meta_data:
                        if query_intent in user.meta_data and len(user.meta_data[query_intent]) != 0:
                            bot_resp = bot_msg.format(item=",".join(user.meta_data[query_intent]),
                                                      intent=query_intent)
                            user_chat.bot_resp = bot_resp
                            user_chat.save()

                            return HttpResponse(json.dumps({'content': bot_resp,
                                                            'status': 200}),
                                                content_type='application/json'
                                                )
                        else:
                            bot_resp = f"Dear {user.user_name}, you have not given me any your favourite {query_intent} details"
                            user_chat.bot_resp = bot_resp
                            user_chat.save()
                            return HttpResponse(
                                json.dumps({
                                               'content': bot_resp,
                                               'status': 200}),
                                content_type='application/json'
                            )
                    else:
                        bot_resp = f"Dear {user.user_name}, I don't know you very much. tell me about yourself more !!"
                        user_chat.bot_resp = bot_resp
                        user_chat.save()

                        return HttpResponse(
                            json.dumps({'content': bot_resp,
                                        'status': 200}),
                            content_type='application/json'
                            )

                else:
                    bot_resp = "Sorry, I am unable to understand your question. Plz try again"
                    user_chat.bot_resp = bot_resp
                    user_chat.save()
                    return HttpResponse({'content': bot_resp,
                                                'status': 200 },
                                        content_type='application/json'
                                        )
            else:
                bot_resp = "Please check your message !!"
                user_chat.bot_resp = bot_resp
                user_chat.save()
                return HttpResponse({'content': bot_resp,
                                            'status': 200},
                                    content_type='application/json'
                                    )
        else:
            query_intent = detect_fav_intent(user_message)

            bot_resp = past_chat.bot_resp
            user_new_chat = UserChatHistory.objects.create(user=user, user_msg=user_message, bot_resp=bot_resp)

            return HttpResponse(json.dumps({'content': bot_resp,'status': 200 }),
                                content_type='application/json'
                                )




