from dff.script import labels as lbl
from dff.script import (
    RESPONSE, TRANSITIONS, PRE_TRANSITIONS_PROCESSING,
    GLOBAL, LOCAL, Message
)
from dff.script import conditions as cnd
from dff.script.slots import processing as slot_procs
from dff.script.slots import response as slot_rsp
from dff.script.slots import conditions as slot_cnd


script = {
    GLOBAL: {
        TRANSITIONS: {
            ("restaurant", "ask"): cnd.regexp(r"^Start|Hi|Hello"),
            lbl.repeat(0.5): cnd.true()
        }
    },
    "restaurant": {
        "ask": {
            RESPONSE: Message(text="Would you like help with an order?"),
            TRANSITIONS: {
                ("restaurant", "address", 1.1): cnd.regexp(r"[yY]es|[yY]eah"),
                ("chitchat", "chat_3", 0.9): cnd.true()
            }
        },
        "address": {
            RESPONSE: Message(text="In what area would you like to find a restaurant?"),
            PRE_TRANSITIONS_PROCESSING: {
                "get_slot": slot_procs.extract(["restaurant/address"])
            },
            TRANSITIONS: {
                ("restaurant", "name", 1.2): slot_cnd.is_set_all(
                    ["restaurant/address"]
                ),
            },
        },
        "name": {
            RESPONSE: slot_rsp.fill_template(
                Message(
                    text=(
                        "{restaurant/address}, got it. "
                        "Which restaurant do you want to go to?")
                )
            ),
            PRE_TRANSITIONS_PROCESSING: {
                "get_slot": slot_procs.extract(["restaurant/name"])
            },
            TRANSITIONS: {
                ("restaurant", "person", 1.2): slot_cnd.is_set_all(["restaurant/name"]),
            },
        },
        "person": {
            RESPONSE: slot_rsp.fill_template(
                Message(
                    text="In whose name should I book a table in {restaurant/name}?"
                )
            ),
            PRE_TRANSITIONS_PROCESSING: {
                "get_slot": slot_procs.extract(["restaurant/person"])
            },
            TRANSITIONS: {
                ("restaurant", "form_filled", 1.2): slot_cnd.is_set_all(
                    ["restaurant/person"]
                ),
            },
        },
        "form_filled": {
            RESPONSE: slot_rsp.fill_template(
                Message(
                    text="All done, a table for {restaurant/person} has been reserved"
                )
            ),
            TRANSITIONS: {("chitchat", "chat_3", 1.1): cnd.true()},
        },
    },
    "chitchat": {
        LOCAL: {TRANSITIONS: {lbl.forward(1): cnd.true()}},
        "chat_1": {RESPONSE: Message(text="How's life?")},
        "chat_2": {
            RESPONSE: Message(text="In what area would you like to find a restaurant?"),
            PRE_TRANSITIONS_PROCESSING: {
                "get_slot": slot_procs.extract(["restaurant/address"])
            },
            TRANSITIONS: {
                ("restaurant", "name", 1.2): slot_cnd.is_set_all(
                    ["restaurant/address"]
                ),
            },
        },
        "chat_3": {
            RESPONSE: Message(text="Have a good day!"),
            TRANSITIONS: {lbl.to_fallback(1.1): cnd.true()},
        },
    },
    "root": {
        "start": {
            RESPONSE: Message(text=""),
            TRANSITIONS: {("restaurant", "ask", 2): cnd.true()}
        },
        "fallback": {
            RESPONSE: Message(text="Nice chatting with you!"),
            TRANSITIONS: {("chitchat", "chat_1", 2): cnd.true()},
        },
    },
}
