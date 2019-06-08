import wikipedia

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client-secret.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "wikibot-bijmvc"

from pymongo import MongoClient

client=MongoClient("mongodb+srv://name:name@cluster0-tdlcz.mongodb.net/test?retryWrites=true&w=majority")
db= client.get_database('student_db')
records=db.student_records

def get_news(parameters):
    print(parameters)
    topic=parameters.get('topic')
    new_student={
         'user_query': topic
         
        }
    records.insert_one(new_student)
    return wikipedia.summary(topic,sentences=4)

def get_idea(parameters):
    print(parameters)
    topic=parameters.get('topic')
    print(wikipedia.page(topic))
    n=wikipedia.page(topic)
    return n.images[0]

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result



def fetch_reply(msg, session_id):
    response = detect_intent_from_text(msg, session_id)
    print(response.parameters)
    print(response.intent.display_name)
    if response.intent.display_name == 'get_summary':
        news = get_news(dict(response.parameters))
        news_str = 'Here is your summ:'
        return news
    elif response.intent.display_name == 'get_image':

        new=get_idea(dict(response.parameters))
        return new

    else:
        return response.fulfillment_text

#      fields {
# key: "topic"
#  value {
#    string_value: "sports"
#
