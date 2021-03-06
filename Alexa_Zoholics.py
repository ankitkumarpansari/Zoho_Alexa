from __future__ import print_function
import urllib2
import json
from re import sub
from decimal import Decimal

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']


    # Dispatch to your skill's intent handlers
    if intent_name == "ZohoIntent":
        return zoho_get_data(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "SF_Intent":
        return get_SF_response(intent,session)
    elif intent_name == "Audience_Intent":
        return get_Audience_response(intent, session)
    elif intent_name == "Accountant_Intent":
        return zoho_lead_accountant(intent, session)
    elif intent_name == "Austin_Intent":
        return zoho_lead_austin(intent, session)
    elif intent_name == "Lead_Intent":
        return zoho_lead_count(intent, session)
    elif intent_name == "Top_Accounts_Intent":
        return zoho_top_accounts(intent, session)
    elif intent_name == "Rep_Intent":
        return zoho_sales_rep(intent, session)
    elif intent_name == "Lost_Deals_Intent":
        return zoho_lost_deals(intent, session)
    elif intent_name == "Deals_Pipeline_Intent":
        return zoho_deals_pipeline(intent, session)
    elif intent_name == "Closed_Leads_Intent":
        return zoho_closed_deals(intent, session)
    elif intent_name == "Best_Sales_Intent":
        return zoho_best_sales_rep(intent, session)
    elif intent_name == "Worst_Sales_Intent":
        return zoho_worst_sales_rep(intent, session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to  Zoho. A leading provider of Cloud"\
                    " Applications for Small and Medium businesses. How"\
                    "can I help you today?"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = None
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Zoho. " \
                    " Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, should_end_session))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# -------------------Who is the admin of my CRM ?------------------

def zoho_get_data(intent, session):
    Auth = '8b1c24432b8cd3274df434039e98f162'
    url = 'https://crm.zoho.com/crm/private/json/Users/getUsers?authtoken=' + Auth + '&scope=crmapi&type=AllUsers'
    response = urllib2.urlopen(url).read()
    r_decoded = json.loads(response)
    name = r_decoded['users']['user']['content']
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    speech_output = 'The administrator of your CRM is ' + name
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------How many of my leads accountants ?--------------

def zoho_lead_accountant(intent, session):
    url = 'https://creator.zoho.com/api/json/alexa/view/Leads_Accountants/zc_ownername=tejaszoholics16&scope=creatorapi&authtoken=477ebc164fe043f942f0cac15398729f&raw=true'
    response = urllib2.urlopen(url).read()
    r_decoded = json.loads(response)
    number =  str(len(r_decoded["CRM_Leads"]))
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    speech_output = 'You have ' + number + 'number of leads who are accountants.'
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# ------------Salesforce or Zoho --------------

def get_SF_response(intent, session):

    session_attributes = {}
    card_title = "Salesforce or Zoho"
    speech_output = "Are you kidding me? Ofcourse. Zoho is better."
    reprompt_text = None
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# ------------Welcome the audience ---------------

def get_Audience_response(intent, session):

    session_attributes = {}
    card_title = "Welcome the audience"
    speech_output = "Hello Everyone! I hope you had an amazing time in Zoholics Sales and Marketing !"
    reprompt_text = None
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# -----------------Leads from Austin--------------------

def zoho_lead_austin(intent, session):
    url = 'https://creator.zoho.com/api/json/alexa/view/Leads_Austin/zc_ownername=tejaszoholics16&scope=creatorapi&authtoken=477ebc164fe043f942f0cac15398729f&raw=true'
    response = urllib2.urlopen(url).read()
    r_decoded = json.loads(response)
    number =  str(len(r_decoded["CRM_Leads"]))
    final = ""
    for lead in r_decoded["CRM_Leads"]:
        final += lead['First_Name'] + " " + lead['Last_Name'] + " " + "who is a " + lead['Title'] + ". "
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    speech_output = "There are " + number + " leads who are from Austin, Texas. They are " + final
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# -------------to count the number of leads in CRM_Leads_Report---------------------

def zoho_lead_count(intent, session):
    url = 'https://creator.zoho.com/api/json/alexa/view/CRM_Leads_Report/zc_ownername=tejaszoholics16&scope=creatorapi&authtoken=477ebc164fe043f942f0cac15398729f&raw=true'
    response = urllib2.urlopen(url).read()
    r_decoded = json.loads(response)
    number =  str(len(r_decoded["CRM_Leads"]))
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    speech_output = 'You have ' + number + ' leads in your CRM. '
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------top five customers in Zoho CRM -----------------------

def zoho_top_accounts(intent,session):
    url = 'https://creator.zoho.com/api/json/alexa/view/Total_Business_Per_Account_Report/zc_ownername=tejaszoholics16&scope=creatorapi&authtoken=477ebc164fe043f942f0cac15398729f&raw=true'
    response = urllib2.urlopen(url).read()
    r_decoded = json.loads(response)
    output = ""
    for i in range(0,5):
          output += r_decoded["Total_Business_Per_Account"][i]["Company_Name"] + " "\
        "with" + " " + r_decoded["Total_Business_Per_Account"][i]["Amount"] + " " + "of closed deals. "
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    speech_output = "Your top five Accounts are :- " + " " + output
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------------- Sales Performance report -------------------

def zoho_sales_rep(intent,session):
    url = 'https://creator.zoho.com/api/json/alexa/view/Sales_Reps_Report/zc_ownername=tejaszoholics16&scope=creatorapi&authtoken=477ebc164fe043f942f0cac15398729f&raw=true'
    response = urllib2.urlopen(url).read()
    r_decoded = json.loads(response)
    output = ""
    for i in range(len(r_decoded["Sales_Reps"])):
          output += r_decoded["Sales_Reps"][i]["Sales_Rep_Name"].split()[0] + ". "
    if 'Tejas' in output:
        output = "Samir. Ricky and Tezas"
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    speech_output = "Your  sales representatives  are " + output + ". "
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# -------------------Best Sales Reps ----------------

def zoho_best_sales_rep(intent,session):
    url = 'https://creator.zoho.com/api/json/alexa/view/Sales_Reps_Report/zc_ownername=tejaszoholics16&scope=creatorapi&authtoken=477ebc164fe043f942f0cac15398729f&raw=true'
    response = urllib2.urlopen(url).read()
    r_decoded = json.loads(response)
    output = ""
    url = 'https://creator.zoho.com/api/json/alexa/view/Sales_Reps_Report/zc_ownername=tejaszoholics16&scope=creatorapi&authtoken=477ebc164fe043f942f0cac15398729f&raw=true'
    response = urllib2.urlopen(url).read()
    r_decoded = json.loads(response)
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    speech_output = "Your best Sales representative is. Tejaas Gadhia . with " + r_decoded["Sales_Reps"][2]["Total_Closed_Won"] + " of closed deals. You should promote him."
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------------------Worst Sales Reps -------------------


def zoho_worst_sales_rep(intent,session):
    url = 'https://creator.zoho.com/api/json/alexa/view/Sales_Reps_Report/zc_ownername=tejaszoholics16&scope=creatorapi&authtoken=477ebc164fe043f942f0cac15398729f&raw=true'
    response = urllib2.urlopen(url).read()
    r_decoded = json.loads(response)
    output = ""
    url = 'https://creator.zoho.com/api/json/alexa/view/Sales_Reps_Report/zc_ownername=tejaszoholics16&scope=creatorapi&authtoken=477ebc164fe043f942f0cac15398729f&raw=true'
    response = urllib2.urlopen(url).read()
    r_decoded = json.loads(response)
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    speech_output = "Your worst Sales representative is. Samir Meharali.  with " + r_decoded["Sales_Reps"][0]["Total_Closed_Won"] + " of closed deals. Oh my god ! He is so bad. You should probably fire him !"
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))



# -------------------Total Number of lost deals -----------------\

def zoho_lost_deals(intent,session):
    url = 'https://creator.zoho.com/api/json/alexa/view/Sales_Reps_Report/zc_ownername=tejaszoholics16&scope=creatorapi&authtoken=477ebc164fe043f942f0cac15398729f&raw=true'
    response = urllib2.urlopen(url).read()
    r_decoded = json.loads(response)
    output = 0
    for i in range(len(r_decoded["Sales_Reps"])-1):
        money = (r_decoded["Sales_Reps"][i]["Total_Closed_Lost"])
        output = Decimal(sub(r'[^\d.]', '', money))
        for i in range(len(r_decoded["Sales_Reps"]) - 1):
            output =  output + value
    output = '${:,.2f}'.format(output)
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    speech_output = "Total value of deals that you lost is " + output + ". "
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# -------------------Total Number of closed deals -----------------\

def zoho_closed_deals(intent,session):
    url = 'https://creator.zoho.com/api/json/alexa/view/Sales_Reps_Report/zc_ownername=tejaszoholics16&scope=creatorapi&authtoken=477ebc164fe043f942f0cac15398729f&raw=true'
    response = urllib2.urlopen(url).read()
    r_decoded = json.loads(response)
    output = 0
    for i in range(len(r_decoded["Sales_Reps"])-1):
        money = (r_decoded["Sales_Reps"][i]["Total_Closed_Won"])
        value = Decimal(sub(r'[^\d.]', '', money))
        for i in range(len(r_decoded["Sales_Reps"]) - 1):
            output =  output + value
    output = '${:,.2f}'.format(output)
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    speech_output = "Total value of deals that you closed is " + output + ". "
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# -------------------Total Number of  deals in pipeline -----------------\

def zoho_deals_pipeline(intent,session):
    url = 'https://creator.zoho.com/api/json/alexa/view/Sales_Reps_Report/zc_ownername=tejaszoholics16&scope=creatorapi&authtoken=477ebc164fe043f942f0cac15398729f&raw=true'
    response = urllib2.urlopen(url).read()
    r_decoded = json.loads(response)
    output = 0
    for i in range(len(r_decoded["Sales_Reps"])-1):
        money = (r_decoded["Sales_Reps"][i]["Total_Pipeline"])
        value = Decimal(sub(r'[^\d.]', '', money))
        for i in range(len(r_decoded["Sales_Reps"]) - 1):
            output =  output + value
    output = '${:,.2f}'.format(output)
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    speech_output = "Total value of deals in your pipeline is " + output + ". "
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
