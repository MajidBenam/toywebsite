from references.models import Citation
import re
def remove_bad_chars_pps(a_str):
    """
    First check for the P or Pp or P. (any number of them) and remove them
    
    Keyword arguments:
    a_string
    Return: augmented string
    """
    # Define the regex pattern
    pattern = r'(?i)[\s,;:.](?:p|pp)\.?\s?\d{1,3}(?:-\d{1,3})?'

    # would be good to remove also : Ezzamel 2004, 504)
    pattern2 = r'[\s,]\d{1,3}\)'
    #  remove also : Ezzamel 2004, 504p
    pattern3 = r'\s\d{1,3}[pP]\s'
    #  also : Ezzamel 2004, 504-6)
    pattern4 = r'[\s,]\d{1,3}-\d{1,3}\)'

    # Remove the matched patterns from the string
    result = re.sub(pattern, '', a_str)
    result = re.sub(pattern2, '', result)
    result = re.sub(pattern3, '', result)
    result = re.sub(pattern4, '', result)

    # remove all extra chars (including spaces:)
    bad_chars = [",", ".", ":", " ","(",")","-","_","'", '"', "?", "&", "</i>", "<i>"]
    for c in bad_chars:
        result = result.replace(c, "")

    result = result.lower()

    return result
    

def check_for_duplicates(all_citations):
    """Checks to see if a string has duplicates in the dataabse:Citation table
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    all_unique_texts = []
    all_unique_objects = []
    counters = [0,0,0]
    for citation in all_citations:
        a = remove_bad_chars_pps(citation.citation_text)
        # a is happening for the first time
        if a not in all_unique_texts:
            # make a rep
            all_unique_texts.append(a)
            all_unique_objects.append(citation)
            citation.certainty = -1 # rep = -1
        else:
            citation.certainty = -2 # 
            counters[0] +=1
            if not citation.done:
                counters[1] +=1
                counters[2] += citation.child_count_browser
        #if not citation.done and citation.certainty == -1:
        #    counters[2] +=1
        #citation.save()

    print(counters[0], " and  ", counters[1], " and ", counters[2])
    return all_unique_objects


# if the item has been done already and does not have a rep: make it the rep
# if the item has been done already and has a rep: make it a sub
# if the item has not been done yet, and does not have a rep: make it rep
# if the item has not been done yet, and has a rep:  make it a sub

