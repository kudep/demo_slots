import pytest
from dff.script import Message
from dff.utils.testing.common import check_happy_path
from dialog_graph.pipeline import pipeline


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "happy_path",
    [
        (
            (
                Message(text="Hi"),
                Message(text="Would you like help with an order?")
            ),
            (
                Message(text="yes"),
                Message(text="In what area would you like to find a restaurant?")
            ),
            (
                Message(text="none"),
                Message(text="In what area would you like to find a restaurant?")
            ),
            (
                Message(text="London"),
                Message(text="London, got it. Which restaurant do you want to go to?")
            ),
            (
                Message(text="Andromeda restaurant"),
                Message(text="In whose name should I book a table in Andromeda?")
            ),
            (
                Message(text="Ivan Ivanov"),
                Message(text="All done, a table for Ivan Ivanov has been reserved"),
            ),
            (
                Message(text="ok"),
                Message(text="Have a good day!")
            ),
            (
                Message(text="bye"),
                Message(text="Nice chatting with you!")
            ),
        )
    ]
)
async def test_happy_path(happy_path):
    check_happy_path(pipeline, happy_path)
