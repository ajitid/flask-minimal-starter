from voluptuous import Schema, Email, Invalid

validate_email = Schema(Email())


def is_email(v):
    try:
        validate_email(v)
        return True
    except Invalid:
        return False
