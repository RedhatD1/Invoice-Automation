def extract_sections(semantic_snippets, snippets):
    section_titles_with_content = []  # For storing titles and their corresponding content
    # In the below condition, if no text>len 2 is detected then try another algo
    if len(semantic_snippets) >= 2:  # More than just the title has been captured
        sorted_snippets = sorted(semantic_snippets, key=lambda x: x.metadata['heading_font'], reverse=True)
        # This ensures that snippets with the largest heading font come first in the sorted list

        second_largest_heading_font = sorted_snippets[1].metadata['heading_font']
        # Since the list is zero-indexed, sorted_snippets[1] corresponds to the second element.

        second_largest_headings = [snippet for snippet in sorted_snippets \
                                   if snippet.metadata['heading_font'] \
                                   == second_largest_heading_font]
        # This will group snippets that have the second-largest heading font size

        second_largest_headings_info = []
        #  to store tuples containing the index and heading text
        #  of the snippets from second_largest_headings
        for heading in second_largest_headings:
            index = snippets.index((heading.metadata['heading'], heading.metadata['heading_font']))
            second_largest_headings_info.append((index, heading.metadata['heading']))

        # Sorts the extracted heading info based on the index
        second_largest_headings_info.sort(key=lambda x: x[0])

        # Now we will use this index information to extract the content
        # print(second_largest_headings_info)

        # Extract the content for each section from the original snippet object
        for idx, heading in enumerate(second_largest_headings_info):

            start_idx, heading_text = second_largest_headings_info[idx]
            heading_text = heading_text.strip()

            if idx + 1 < len(second_largest_headings_info):
                end_idx, next_heading = second_largest_headings_info[idx + 1]
            else:
                end_idx, next_heading = len(snippets), ''

            print(f'{heading_text} is between {start_idx} and {end_idx}')
            content = ''
            for i in range(start_idx, end_idx):
                content += snippets[i][0]
            section_titles_with_content.append((heading_text.lower(), content))
            print(section_titles_with_content)
    return section_titles_with_content