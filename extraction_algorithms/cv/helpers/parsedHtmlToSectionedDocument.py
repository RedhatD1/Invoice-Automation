from langchain.docstore.document import Document
# This module creates the sections grabbed from the parsed html
# The Document class is used to represent a document with content and associated metadata.
def convert(snippets, data):

    cur_idx = -1
    # The current idx position in our snippets object

    sectionedDocument = []
    # This will contain the organized snippets where there are formed together
    # based on their relative font size in the document

    # Assumption: headings have higher font size than their respective content
    for snippet in snippets:
        # if current snippet's font size > previous section's heading => it is a new heading
        if not sectionedDocument or snippet[1] > sectionedDocument[cur_idx].metadata['heading_font']:
            metadata={'heading':snippet[0], 'content_font': 0, 'heading_font': snippet[1]}
            # Since we saved the heading and its fontsize as a tuple
            # Its first index contains the heading text
            # and the second index contains the fontsize of the heading
            # We also initialized the content_font of the heading to 0

            metadata.update(data.metadata) # Here data is inherited from langchain document library.

            sectionedDocument.append(Document(page_content='',metadata=metadata))
            cur_idx += 1
            continue

        # if (current snippet's font size <= previous section's content)
        # -> content belongs to the same section
        if not sectionedDocument[cur_idx].metadata['content_font'] \
                    or snippet[1] <= sectionedDocument[cur_idx].metadata['content_font']:

           # checks if the content font size is not yet set or
           # whether the current snippet's font size (snippet[1]) is
           # less than or equal to the font size of the previous section's content
           # if these conditions are true, then the new snippet is part of the previous section
            sectionedDocument[cur_idx].page_content += snippet[0]
            sectionedDocument[cur_idx].metadata['content_font'] \
                    = max(snippet[1], sectionedDocument[cur_idx].metadata['content_font'])
            continue

        else:
            # else if current snippet's font size > previous section's content
            # but less than previous section's heading than also make a new section
            metadata={'heading':snippet[0], 'content_font': 0, 'heading_font': snippet[1]}
            metadata.update(data.metadata)
            sectionedDocument.append(Document(page_content='',metadata=metadata))
            cur_idx += 1
    return sectionedDocument

