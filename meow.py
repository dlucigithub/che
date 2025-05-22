from urllib.parse import urlparse
import webbrowser
import time

def val(url):
    parsed = urlparse(url)

    if not parsed.scheme:
        ask = input("Your link is missing the scheme. Add 'http://'? (Y/N): ").upper()
        if ask == "Y":
            url = "http://" + url
            parsed = urlparse(url)
        else:
            return None

    if all([parsed.scheme, parsed.netloc]):
        return url
    return None

basic_actions = ["open", "visit", "go to", "launch", "start"]
revisit_actions = ["again", "open it again", "reopen", "go back to", "revisit", "relaunch"]
search_intents = ["search", "look up", "browse", "check", "check out", "surf"]
navigation_intents = ["navigate to", "access", "load", "pull up", "jump to", "take me to", "connect to"]
display_intents = ["show", "display", "fire up", "show me", "open site", "visit page", "load page"]

negative_intents = [
    "no", "nope", "nah", "not now", "cancel", "stop", "don't", "don’t do it",
    "never mind", "forget it", "i changed my mind", "nuh uh"
]

confirmation_intents = ["yes", "yeah", "yep", "sure", "ok", "okay"]

last_valid_url = None
awaiting = False
last_target = None

def detect_intent(user_input):
    user_input_lower = user_input.lower()
    for kw in negative_intents:
        if kw in user_input_lower:
            return ("negative_intents", kw)
    for kw in revisit_actions:
        if kw in user_input_lower:
            return ("revisit_actions", kw)
    for kw in basic_actions:
        if kw in user_input_lower:
            return ("basic_actions", kw)
    for kw in confirmation_intents:
        if kw in user_input_lower:
            return ("confirmation_intents", kw)
    return (None, None)

def extract_target(user_input, detected_intent):
    user_input_lower = user_input.lower()
    intent_lower = detected_intent.lower()
    target_part = user_input_lower.replace(intent_lower, "", 1).strip()
    return target_part

def st():
    global last_valid_url, awaiting, last_target

    while True:
        user_input = input("Input: ").strip()

        if awaiting:
            category, _ = detect_intent(user_input)
            if category == "confirmation_intents":
                validated_url = val(last_target)
                if validated_url:
                    print("Opening:", validated_url)
                    webbrowser.open(validated_url)
                    last_valid_url = validated_url
                else:
                    print("Still invalid URL.")
                awaiting = False
                continue
            elif category == "negative_intents":
                print("Operation canceled.")
                awaiting = False
                continue
            else:
                print("Please answer yes or no.")
                continue

        intent_category, intent_keyword = detect_intent(user_input)

        if intent_category == "negative_intents":
            print("Action canceled.")
            continue

        elif intent_category == "revisit_actions":
            if last_valid_url:
                print("Reopening last URL:", last_valid_url)
                webbrowser.open(last_valid_url)
            else:
                print("No previous URL to reopen.")
            continue

        elif intent_category == "basic_actions":
            target = extract_target(user_input, intent_keyword)
            if not target:
                print("Please specify a URL or keyword to open.")
                continue

            validated_url = val(target)
            if validated_url:
                print("Opening:", validated_url)
                webbrowser.open(validated_url)
                last_valid_url = validated_url
            else:
                last_target = target
                awaiting = True
            continue

        else:
            print("Sorry, I didn't understand. Try again.")

if __name__ == "__main__":
    st()
