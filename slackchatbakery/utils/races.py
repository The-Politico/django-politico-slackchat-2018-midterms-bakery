from slackchatbakery.utils.stater import slug_to_postal, postal_to_slug


def race_to_state_division(race):
    race_parts = race.split("-")
    if len(race_parts) < 2:
        return None, None
    return race_parts[0].upper(), "-".join(race_parts[1:]).lower()


def normalize_race_id(race):
    state, division = race_to_state_division(race)
    return "{}-{}".format(state, division)


def message_in_body(message, body):
    race_id = get_race_from_message(message)
    if get_body_from_race(race_id) == body:
        return True
    else:
        return False


def message_in_state(message, state_slug):
    race_id = get_race_from_message(message)
    if race_id.split("-")[0].lower() == slug_to_postal(state_slug).lower():
        return True
    else:
        return False


def message_has_race(message):
    race_id = get_race_from_message(message)
    if race_id.split("-")[0].lower() != "":
        return True
    else:
        return False


def get_states_in_channel(messages):
    states = []
    for message in messages:
        race_id = get_race_from_message(message)
        state_postal = race_id.split("-")[0].upper()

        if state_postal != "":
            state_slug = postal_to_slug(state_postal)

            if state_slug not in states:
                states.append(state_slug)

    return states


def get_bodies_in_channel(messages):
    bodies = []
    for message in messages:
        race_id = get_race_from_message(message)
        body = get_body_from_race(race_id)

        if body not in bodies:
            bodies.append(body)

    return bodies


def get_body_from_race(race):
    if race.endswith("sen") or race.endswith("sen-special"):
        return "senate"
    if race.endswith("gov"):
        return "governor"
    else:
        return "house"


def get_body_from_division(division):
    if division == "sen" or division == "sen-special":
        return "senate"
    if division == "gov":
        return "governor"
    else:
        return "house"


def get_race_from_message(message):
    return message.get("kwargs", {"race": ""}).get("race", "").lower()


def filter_body_and_group_by_race(messages, body):
    return group_by_race(
        [message for message in messages if message_in_body(message, body)]
    )


def group_by_race(messages):
    d = {}
    for message in messages:
        race = normalize_race_id(message["kwargs"]["race"])
        if race not in d:
            d[race] = []
        d[race].append(message)
    return d
