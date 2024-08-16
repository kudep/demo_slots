from dff.pipeline import Pipeline
from dff.script import slots
from . import script
from .slots import CustomSlot


slots.GroupSlot(
        name="restaurant",
        children=[
            CustomSlot(
                name="person",
                prompt=(
                    'As an answer, print full name from the sentence.'
                    'If there no answer return None. Sentence:'
                ),
                tag="PER"
            ),
            CustomSlot(
                name="address",
                prompt=(
                    'As an answer, return location from the sentence. '
                    'Print only location. Sentence:'
                ),
                tag="LOC"
            ),
            CustomSlot(
                name="name",
                prompt=(
                    'As an answer, print name of the restaurant from the sentence. '
                    'Print only name. If there no answer return None. Sentence:'
                ),
                tag="ORG"
            )
        ],
    )

pipeline: Pipeline = Pipeline.from_script(
    script=script.script,
    start_label=("root", "start"),
    fallback_label=("root", "fallback"),
)
