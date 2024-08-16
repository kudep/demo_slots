from typing import Callable

from dff.script import Context
from dff.pipeline.pipeline.pipeline import Pipeline, SLOT_STORAGE_KEY  # noqa: F401
from dff.script.slots.types import ValueSlot

from .ner_model import get_response_ner
from .llm_model import get_response_oasst


class CustomSlot(ValueSlot):
    """
    CustomSlot is a slot type that extracts its value using a different models.
    You can pass a prompt for LLM model to the `prompt` argument.
    You can pass a tag to be retrieved by a NER model to the `tag` argument.
    """
    tag: str
    prompt: str

    def fill_template(self, template: str) -> Callable:
        def fill_inner(ctx: Context, pipeline: Pipeline):
            checked_template = (
                super(CustomSlot, self).fill_template(template)(ctx, pipeline)
            )
            if checked_template is None:
                return template

            value = ctx.framework_states[SLOT_STORAGE_KEY][self.name]
            return checked_template.replace("{" + self.name + "}", value)
        return fill_inner

    def extract_value(self, ctx: Context, _: Pipeline):
        """
        Method to extract slots depending on the selected model.
        """
        if ctx.last_request.misc:
            flag = ctx.last_request.misc['flag']
        else:
            flag = 'NER'  # default value for testing

        if flag == 'NER':
            self.value = get_response_ner(ctx.last_request.text, self.tag)
        elif flag == 'Open Assistant':
            self.value = get_response_oasst(f'{self.prompt} {ctx.last_request.text}')
        else:
            raise ValueError(f"This slot type is not defined: {flag}")
        return self.value
