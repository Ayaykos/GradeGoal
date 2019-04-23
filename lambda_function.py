# -*- coding: utf-8 -*-
"""Simple fact sample app."""

import random
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response


# =========================================================================================================================================
# TODO: The items below this comment need your attention.
# =========================================================================================================================================
SKILL_NAME = "GradeGoal"
GET_FACT_MESSAGE = "Here's your fact: "
HELP_MESSAGE = "You can say tell me your current grade and what your goal is, or you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The Grade Goal skill can't help you with that. How can I help you calculate your grade?"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."
desiredScore = 100
calculatedScore = 50
#slotVar = slots.get("currentPercentage").value

# =========================================================================================================================================
# TODO: Replace this data with your own.  You can find translations of this data at http://github.com/alexa/skill-sample-python-fact/lambda/data
# =========================================================================================================================================

data = ["Might as well skip the exam. Good job!", "Smooth sailing hot shot!",
"Easy peasy.","You're gonna do great",
"Not bad!","Good job!",
"You should probably study.","Good luck!","Hope it goes well", "You might struggle a little bit.",
"You are not gonna have a great time.", "Go to office hours.","Study hard.",
"Rest in piece.","Drop the class while you can. If you can't, uh oops.","yikes."]

# =========================================================================================================================================
# Editing anything below this line might break your skill.
# =========================================================================================================================================

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def responseSentiment(grade):
    if (grade <= 10):
        return data[random.randint(0,1)]
    elif (grade > 10 and grade <= 40):
        return data[random.randint(2,3)]
    elif (grade > 40 and grade <= 75):
        return data[random.randint(4,5)]
    elif (grade > 75 and grade <= 90):
        return data[random.randint(6,9)]
    elif (grade > 90 and grade <= 100):
        return data[random.randint(10,12)]
    elif (grade > 100):
        return data[random.randint(13,15)]
        
def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

print (text2int("one hundred"))

def normalize(number):
    temp = str(number)
    
    if ('percent' in temp):
        number = str(number)
        number = temp[:-7]
        if(' point ' in number):
            number = number.replace(' point ','.')
    
    return float(number)




class currentPercentageIntentHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or 
        is_intent_name("currentPercentageIntent")(handler_input))

        

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNewFactHandler")
        
        #random_fact = "random.choice(data)"
        #speech = "GET_FACT_MESSAGE + random_fact"
        
        slots = handler_input.request_envelope.request.intent.slots
        
        currentPercentage = (normalize(slots.get("currentPercentage").value))*0.01
        goal = (normalize(slots.get("goal").value))*0.01
        weight = (normalize(slots.get("weight").value))*0.01

        result =  float( (goal) - (1-weight)*currentPercentage) / weight
        
        
        speech = str( round(   (result*100),2    ) )
        speech = "You need a " + speech + "% on your exam to achieve your grade goal. " + responseSentiment(result*100)

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, speech))
        return handler_input.response_builder.response
        

# Built-in Intent Handlers
"""
class IntroductionIntentHandler(AbstractRequestHandler):
    #Handler for Skill Launch and GetNewFact Intent.
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        #return (is_request_type("LaunchRequest")(handler_input) or
                #is_intent_name("GetNewSpaceFactIntent")(handler_input))
        return (is_request_type("LaunchRequest")(handler_input) or 
        is_intent_name("IntroductionIntent")(handler_input))
        

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNewFactHandler")

        #random_fact = random.choice(data)
        #speech = GET_FACT_MESSAGE + random_fact
        speech = "Welcome to grade goal. What would you like help with?"
        
        
        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, speech))
        return handler_input.response_builder.response
"""


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(currentPercentageIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
# sb.add_global_request_interceptor(RequestLogger())
# sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
