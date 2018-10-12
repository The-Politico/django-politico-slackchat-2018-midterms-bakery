from slackchatbakery.utils.stater import slug_to_postal, postal_to_slug


def get_races_from_message(message):
    """
    Parses a comma separated list from a Slack message with a kwarg of race.
    """
    message_kwargs = message.get(
        "kwargs", {"race": ""}
    ).get("race", "").lower()
    races = message_kwargs.replace(' ', '').split(',')
    return races


def race_to_state_division(race):
    """
    Parses the state and division (e.g. "sen", "gov", "04") and returns them
    as two normalized parts. (States are upercase and divisions are lower.)
    """
    race_parts = race.split("-")
    if len(race_parts) < 2:
        return None, None
    return race_parts[0].upper(), "-".join(race_parts[1:]).lower()


def normalize_race_id(race):
    """
    Normalizes a race Id so that states are uppercase and division are lower.
    """
    state, division = race_to_state_division(race)
    return "{}-{}".format(state, division)


def message_in_body(message, body):
    """
    Checks if a message is tagged with a race that is in a given body.
    """
    races = get_races_from_message(message)
    for race in races:
        if get_body_from_race(race) == body:
            return True
    return False


def message_in_state(message, state_slug):
    """
    Checks if a message is tagged with a race that is in a given state.
    """
    races = get_races_from_message(message)
    for race in races:
        if race.split("-")[0].lower() == slug_to_postal(state_slug).lower():
            return True
    return False


def message_has_races(message):
    """
    Checks to see if a message has a race kwarg.
    """
    races = get_races_from_message(message)
    return len(races) > 0 and races[0] != ''


def get_states_in_channel(messages):
    """
    Given a list of messages in a channel, returns a list of all the states
    refereced in all the messages.
    """
    states = []
    for message in messages:
        races = get_races_from_message(message)
        for race in races:
            state_postal = race.split("-")[0].upper()

            if state_postal != "":
                state_slug = postal_to_slug(state_postal)

                if state_slug not in states:
                    states.append(state_slug)

    return states


def get_bodies_in_channel(messages):
    """
    Given a list of messages in a channel, returns a list of all the bodies
    refereced in all the messages.
    """
    bodies = []
    for message in messages:
        races = get_races_from_message(message)
        for race in races:
            body = get_body_from_race(race)

            if body not in bodies:
                bodies.append(body)

    return bodies


def get_body_from_race(race):
    """
    Returns a body from a given race Id. (e.g. "TX-04" returns "house").
    """
    if race.endswith("sen") or race.endswith("sen-special"):
        return "senate"
    if race.endswith("gov"):
        return "governor"
    else:
        return "house"


def get_body_from_division(division):
    """
    Returns a body from a given division. (e.g. "04" returns "house").
    """
    if division == "sen" or division == "sen-special":
        return "senate"
    if division == "gov":
        return "governor"
    else:
        return "house"


def get_state_from_race(race):
    """
    Returns a state postal code from a given race Id.
    (e.g. "TX-04" returns "TX").
    """
    return race.split("-")[0].upper()


def filter_races_by_body(races, body):
    """
    Filters a dictionary of races for only those in a given body. Removes keys
    that are not part of the body.
    """
    filtered = {}
    for race in races:
        if get_body_from_race(race) == body:
            filtered[race] = races[race]
    return filtered


def filter_races_by_state(races, state):
    """
    Filters a dictionary of races for only those in a given state. Uses state
    slugs. Removes keys that are not part of the body.
    """
    filtered = {}
    for race in races:
        if get_state_from_race(race) == slug_to_postal(state):
            filtered[race] = races[race]
    return filtered


def group_by_race(messages):
    """
    Groups messages by the races they're tagged with. If a message is tagged
    with more than one race, it will be in both groups. For this reason the
    total number of entires in the output dict will not necesarily equal the
    the number of entries in the original list.
    """
    d = {}
    for message in messages:
        races = get_races_from_message(message)
        for race in races:
            race_id = normalize_race_id(race)
            if race_id not in d.keys():
                d[race_id] = []
            d[race_id].append(message)
    return d


def filter_and_group_by_race(messages, **kwargs):
    """
    Filters and groups a message list into a dictionary with only races in a
    given body.
    """
    output = group_by_race(messages)
    if(kwargs.get('body', None)):
        output = filter_races_by_body(output, kwargs["body"])
    if(kwargs.get('state', None)):
        output = filter_races_by_state(output, kwargs["state"])
    return output
