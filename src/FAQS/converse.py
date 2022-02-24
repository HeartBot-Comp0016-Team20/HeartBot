import re
import random
from FAQS import best_match

class Chat:
    def __init__(self, pairs, reflections={}):
        self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()

    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections, key=len, reverse=True)
        return re.compile(r"\b({})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE)

    def _substitute(self, str):
        return self._regex.sub(lambda mo: self._reflections[mo.string[mo.start() : mo.end()]], str.lower())

    def _wildcards(self, response, match):
        pos = -1
        while pos >= 0:
            num = int(response[pos + 1 : pos + 2])
            response = (
                response[:pos]
                + self._substitute(match.group(num))
                + response[pos + 2 :]
            )
            pos = response.find("%")
        return response

    def respond(self, str):
        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)  # pick a random response
                resp = self._wildcards(resp, match)  # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == "?.":
                    resp = resp[:-2] + "."
                if resp[-2:] == "??":
                    resp = resp[:-2] + "?"
                return resp


    def check_input(self, user_input):
        matcher = best_match.BestMatch()
        if user_input:
            while user_input[-1] in "!.":
                user_input = user_input[:-1]
            try:
                user_input = matcher.findClosestQuestion(user_input)
                if (self.respond(user_input)!= None):
                    print(self.respond(user_input))
                else:
                    print("I dont understand")
            except ZeroDivisionError:
                print("I dont understand")

    # Hold a conversation with a chatbot
    def converse(self, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try:
                user_input = input(">")
            except EOFError:
                print(user_input)
            self.check_input(user_input)

    # The following methods are variations of the methods
    # above that will used for the website chatbot interface:

    # Same as converse() but without while loop
    def web_converse(self, user_input):
        return self.web_check_input(user_input)

    # Same as check_input() but without prints
    def web_check_input(self, user_input):
        matcher = best_match.BestMatch()
        if user_input:
            while user_input[-1] in "!.":
                user_input = user_input[:-1]
            try:
                user_input = matcher.findClosestQuestion(user_input)
                if (self.respond(user_input)!= None):
                    return (1,self.respond(user_input))
                else:
                    return (0,user_input)
            except ZeroDivisionError:
                return (1,"I dont understand")