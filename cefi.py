import re

from docx import Document

from dataextractor import find_paras_between_headings, process_paragraphs

# Could load these from file
keywords = [('fullscale', 'Full Scale'),
            ('organization', 'Organization'),
            ('attention', 'Attention'),
            ('memory', 'Working Memory'),
            ('planning', 'Planning'),
            ('flexibility', 'Flexibility'),
            ('inhibitory', 'Inhibitory Control'),
            ('selfmonitoring', 'Self-Monitoring'),
            ('initiation', 'Initiation'),
            ('emotion', 'Emotion Regulation')]

keyphrases = {'Full Scale': 'fullscale',
            'Organization': 'organization',
            'Attention': 'attention',
            'Working Memory': 'memory',
            'Planning': 'planning',
            'Flexibility': 'flexibility',
            'Inhibitory Control': 'inhibitory',
            'Self-Monitoring': 'selfmonitoring',
            'Initiation': 'initiation',
            'Emotion Regulation': 'emotion'}
def remove_text_up_to_word(text, word):
    # Find the first occurrence of the word
    index = text.find(word)
    if index != -1:
        # Remove all text up to and including the word
        return text[index:].strip()
    else:
        # Return the original text if the word is not found
        return text

def str_right(text, phrase, idx):
    # Calculate the starting index for the substring to the right of the phrase
    start_idx = idx + len(phrase)
    # Slice the text starting from the calculated index
    return text[start_idx:].strip()

def check_and_extract(text, predefined_text):
    # Check if the text starts with the predefined text
    start_pattern = f"{predefined_text}’s"
    index = text.find(start_pattern)
    if index >= 0:
        # Define the pattern to search for the phrases "scale score" or "standard score"
        subtext = str_right(text, start_pattern, index)
        pattern = r"(.*?)\b(scale score|standard score)\b"
        match = re.search(pattern, subtext, re.IGNORECASE)
        if match:
            # Extract the words leading up to the matched phrase
            newtext = match.group(1).strip()
            return newtext
    return None

eliminated_text = "(See the CEFI Items by Scale section of this report for additional low item scores.)"
# Function to read the file and group paragraphs
def group_paragraphs(paragraphs, start_text, replacementprefix):
    grouped_data = {}
    current_paragraphs = []

    for para in paragraphs:
        # Find the first paragraph in a sequence which will of the form
        # First Name Last Name's <keyterm>
        phrase = check_and_extract(para.text, start_text)
        keyword = keyphrases.get(phrase, None)
        if keyword:
            newtext = remove_text_up_to_word(para.text, phrase)
            para.text = replacementprefix + newtext
            para.text = para.text.replace(eliminated_text, '').strip()
            current_paragraphs = [para]
#            current_paragraphs = [newtext]
            grouped_data[keyword] = current_paragraphs
        else:
            para.text = para.text.replace(eliminated_text, '').strip()
            current_paragraphs.append(para)
#            current_paragraphs.append(para.text)

    return grouped_data
# Function to remove names at the beginning of paragraphs
def remove_names(grouped_data):
    processed_data = {}
    for keyword, text in grouped_data.items():
        lines = text.split('. ')
        if lines[0].split()[0].isalpha():
            lines = lines[1:]
        processed_data[keyword] = '. '.join(lines)
    return processed_data

def process_cefi(doc, clientfullname, clientfirstname):
    keypoints = [('fullscale', 'CEFI Results', 'CEFI Items by Scale', False)]

    paras = []
    for heading in keypoints:
        starttext = heading[1]
        endtext = heading[2]
        paras = find_paras_between_headings(doc, 0, starttext, endtext, heading[3])

        cefi = group_paragraphs(paras, clientfullname, f"{clientfirstname}'s ")
        return cefi

def fetch_cefi_data(context):
    cefi = {
        'fullscale_score': 78,
        'attention_score': 86,
        'emotionalregulation_score': 69,
        'flexibility_score': 80,
        'inhibitorycontrol_score': 77,
        'initiation_score': 74,
        'organization_score': 89,
        'planning_score': 81,
        'selfmonitoring_score': 77,
        'workingmemory_score': 86
    }

    active_path = context['active_path']
    cefi_doc_path = f"{active_path}/word/cefi.docx"
    cefi_doc = Document(cefi_doc_path)
    cefi_text = process_cefi(cefi_doc, context['clientfullname'], context['client_firstname'])

    process_paragraphs(cefi, cefi_text, context['style'])
    ratingscales = context['rs']
    ratingscales['cefi'] = cefi

    return cefi