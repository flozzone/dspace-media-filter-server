from dspace_media_filter.filter import MediaFilterRequest
from pptx import Presentation

from dspace_media_filter.text import TextFilter


class PPTTextFilter(TextFilter):
    def filter_text(self, req: MediaFilterRequest) -> str:
        # the following could be also rewritten as a "one"-liner
        # return '\n'.join(['\n'.join([shape.text for shape in slide.shapes if hasattr(shape, "text")])
        #                             for slide in Presentation(req.abs_file).slides])

        text = ""
        prs = Presentation(req.abs_file)
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text

        return text
