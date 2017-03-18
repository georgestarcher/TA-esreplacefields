import sys
import re,json

from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators

@Configuration()
class ESReplaceFieldsCommand(StreamingCommand):

    def stream(self,events):

        if len(self.fieldnames) < 1:
            raise Exception('Please specify at least one field')

        for event in events:
            for fieldname in self.fieldnames:
                fieldname = fieldname.strip()
                if fieldname not in event: continue
                tokenized_field = event.get(fieldname)
                eventDict = dict(event)
                retokenized_field =  re.sub(r"\$(\w+?)\$", r"{\1}", tokenized_field)
                try:
                    event.update({fieldname:retokenized_field.format(**eventDict)})
                except Exception as err_message:
                    pass 
            yield event

dispatch(ESReplaceFieldsCommand, sys.argv, sys.stdin, sys.stdout, __name__)

