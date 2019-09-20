# Functions for creating html tags

def generic_tag(type):
    def return_tag(text):
        tagged = f"<{type}>{text}</{type}>"
        return tagged
    return return_tag

tag_p = generic_tag("p")
tag_h1 = generic_tag("h1")