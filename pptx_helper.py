import logging
import pathlib
import re
import tempfile
from typing import List, Tuple

import json5
import pptx
from global_config import GlobalConfig

PATTERN = re.compile(r"^slide[ ]+\d+:", re.IGNORECASE)
SAMPLE_JSON_FOR_PPTX = '''
{
    "title": "Understanding AI",
    "slides": [
        {
            "heading": "Introduction",
            "bullet_points": [
                "Brief overview of AI",
                [
                    "Importance of understanding AI"
                ]
            ]
        }
    ]
}
'''

logging.basicConfig(
    level=GlobalConfig.LOG_LEVEL,
    format='%(asctime)s - %(message)s',
)


def remove_slide_number_from_heading(header: str) -> str:
    """
    Remove the slide number from a given slide header.

    :param header: The header of a slide
    """

    if PATTERN.match(header):
        idx = header.find(':')
        header = header[idx + 1:]

    return header


def generate_powerpoint_presentation(
        structured_data: str,
        slides_template: str,
        output_file_path: pathlib.Path
) -> List:
    """
    Create and save a PowerPoint presentation file containing the content in JSON format.

    :param structured_data: The presentation contents as "JSON" (may contain trailing commas)
    :param slides_template: The PPTX template to use
    :param output_file_path: The path of the PPTX file to save as
    :return A list of presentation title and slides headers
    """

    # The structured "JSON" might contain trailing commas, so using json5
    parsed_data = json5.loads(structured_data)
    config = GlobalConfig()
    
    logging.debug(
        "*** Using PPTX template: %s",
        config.PPTX_TEMPLATE_FILES[slides_template]['file']
    )
    presentation = pptx.Presentation(config.PPTX_TEMPLATE_FILES[slides_template]['file'])

    # The title slide
    if len(presentation.slides) > 0:
        for i in range(len(presentation.slides)-1, -1, -1): 
            rId = presentation.slides._sldIdLst[i].rId
            presentation.part.drop_rel(rId)
            del presentation.slides._sldIdLst[i]
        #
    #
    title_slide_layout = presentation.slide_layouts[0]
    slide = presentation.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = parsed_data['title']
    logging.debug('Presentation title is: %s', title.text)
    if 'subtitle' in parsed_data:
        subtitle.text = parsed_data['subtitle']
        logging.debug('Presentation subtitle is: %s', subtitle.text)
    else:
        subtitle.text = ''
    #
    all_headers = [title.text, ]

    # background = slide.background
    # background.fill.solid()
    # background.fill.fore_color.rgb = RGBColor.from_string('C0C0C0')  # Silver
    # title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 0, 128)  # Navy blue
    slides_parsed_data = None
    if 'slides' in parsed_data: slides_parsed_data = parsed_data['slides']
    if slides_parsed_data is None:
        error_message = 'No slides found in the parsed data'
        logging.error('error_message')
        print(error_message)
        return []
    #
    print("**************")
    print("slides_parsed_data=",slides_parsed_data)
    print("slides_parsed_data type=",type(slides_parsed_data))
    print("slides_parsed_data len=", len(slides_parsed_data))
    # if slides_parsed_data is of type string, convert it to a json dictionary
    if type(slides_parsed_data) == str:
        slides_parsed_data = json5.loads(slides_parsed_data)
        print("AFTER CORRECTION:")
        print("slides_parsed_data type=",type(slides_parsed_data))
        print("slides_parsed_data len=", len(slides_parsed_data))    
    #
         
    # Add contents in a loop    
    for a_slide in slides_parsed_data:
        print("------------------")
        print("a_slide=",a_slide)
        if "type" in a_slide and a_slide["type"] == "sectionheader":
            bullet_slide_layout = presentation.slide_layouts[2]
        else:
            bullet_slide_layout = presentation.slide_layouts[1]
        #
        
        slide = presentation.slides.add_slide(bullet_slide_layout)
        shapes = slide.shapes

        title_shape = shapes.title
            
            
        body_shape = shapes.placeholders[1]
        title_shape.text = remove_slide_number_from_heading(a_slide['heading'])
        all_headers.append(title_shape.text)
        text_frame = body_shape.text_frame

        # The bullet_points may contain a nested hierarchy of JSON arrays
        # In some scenarios, it may contain objects (dictionaries) because the LLM generated so
        #  ^ The second scenario is not covered

        flat_items_list = get_flat_list_of_contents(a_slide['bullet_points'], level=0)

        for an_item in flat_items_list:
            paragraph = text_frame.add_paragraph()
            paragraph.text = an_item[0]
            paragraph.level = an_item[1]

    # The thank-you slide
    #last_slide_layout = presentation.slide_layouts[0]
    #slide = presentation.slides.add_slide(last_slide_layout)
    #title = slide.shapes.title
    #title.text = 'Thank you!'

    presentation.save(output_file_path)

    return all_headers
#

def generate_powerpoint_presentation_advanced(
        structured_data: str,
        slides_template: str,
        output_file_path: pathlib.Path
) -> List:
    """
    Create and save a PowerPoint presentation file containing the content in JSON format.

    :param structured_data: The presentation contents as "JSON" (may contain trailing commas)
    :param slides_template: The PPTX template to use
    :param output_file_path: The path of the PPTX file to save as
    :return A list of presentation title and slides headers
    """

    # The structured "JSON" might contain trailing commas, so using json5
    parsed_data = None
    try:
        parsed_data = json5.loads(structured_data)
    except Exception as e:
        print("Error parsing JSON5 data: ", e)
        print("structured_data = ", structured_data)
        return []
    #
    print("--------")
    print("parsed_data = ", parsed_data)
    print("--------")
    
    data_slides = []
    data_title = ""
    data_subtitle = ""
    if 'slides' in parsed_data: 
        data_slides = parsed_data['slides'] 
    else: 
        print(f"[ERROR] No slides in parsed_data: f{parsed_data}")
    #
    
    if 'title' in parsed_data: data_title = parsed_data['title']
    if 'subtitle' in parsed_data: data_subtitle = parsed_data['subtitle']
    
    print("==============")
    print("data_slides = ", data_slides)
    print("==============")
    print(f"data_title = {data_title}, data_subtitle = {data_subtitle}")
    print("==============")
      
    slides = json5.loads(data_slides)  
    config = GlobalConfig()
    
    logging.debug(
        "*** Using PPTX template: %s",
        config.PPTX_TEMPLATE_FILES[slides_template]['file']
    )
    presentation = pptx.Presentation(config.PPTX_TEMPLATE_FILES[slides_template]['file'])

    # The title slide
    pptx_slide = None
    if len(presentation.slides) > 0:
        for i in range(len(presentation.slides)-1, -1, -1): 
            rId = presentation.slides._sldIdLst[i].rId
            presentation.part.drop_rel(rId)
            del presentation.slides._sldIdLst[i]
        #
    #
    title_slide_layout = presentation.slide_layouts[0]
    pptx_slide = presentation.slides.add_slide(title_slide_layout)
    pptx_title = pptx_slide.shapes.title
    pptx_title.text = data_title
    pptx_subtitle = pptx_slide.placeholders[1]
    pptx_subtitle.text = data_subtitle

    all_headers = [pptx_title.text, ]
    print("all_headers = ", all_headers)

    # Add contents in a loop   
    lettered = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    for a_slide in slides:
        numbered_indexes = [0,0,0,0,0]
        lettered_indexes = [0,0,0,0,0]
        print("------------------")
        print(f"slide = {a_slide}")
        
        heading = ""
        bullet_points = []
        section_type = ""
        is_section_header = False
        
        if "heading" in a_slide: heading = a_slide['heading']
        if "bullet_points" in a_slide: bullet_points = a_slide['bullet_points']
        if "type" in a_slide: section_type = a_slide['type']
        
        if section_type == "sectionheader": 
            is_section_header = True
            print("This is a section header")
            bullet_slide_layout = presentation.slide_layouts[2]
        else:
            bullet_slide_layout = presentation.slide_layouts[1]
        #
        
        current_slide = presentation.slides.add_slide(bullet_slide_layout)
        current_shapes = current_slide.shapes
        title_shape = current_shapes.title            
        body_shape = current_shapes.placeholders[1]
        title_shape.text = remove_slide_number_from_heading(heading)
        all_headers.append(title_shape.text)
        text_frame = body_shape.text_frame

        if len(bullet_points) > 0:
            
            
            # The bullet_points is a flat array with indentation level explicitly set
            # We create bullets, numbers and letters 'bullets' manually
            previous_numbered_level = -1
            previous_lettered_level = -1
            
            for an_item in bullet_points:
                
                bullet_type = "none"
                bullet_level = 0
                bullet_text = ""
                
                if "bullet_type" in an_item: bullet_type = an_item["bullet_type"]    
                if "bullet_level" in an_item: bullet_level = int(an_item["bullet_level"])
                if "bullet_text" in an_item: bullet_text = an_item["bullet_text"]
                
                indentation = bullet_level
                if bullet_type == "bullet":
                    bullet_text = "• " + bullet_text
                elif bullet_type == "number":
                    if previous_numbered_level < bullet_level: numbered_indexes[bullet_level] = 0
                    bullet_text = f"{numbered_indexes[bullet_level] + 1}. " + bullet_text
                    previous_numbered_level = bullet_level
                    numbered_indexes[bullet_level] += 1
                    #indentation += 2
                elif bullet_type == "letter":
                    if previous_lettered_level < bullet_level: lettered_indexes[bullet_level] = 0
                    bullet_text = f"{lettered[lettered_indexes[bullet_level]]}. " + bullet_text
                    lettered_indexes[bullet_level] += 1
                    previous_lettered_level = bullet_level
                    #indentation += 3
                #        
                
                print(f"bullet_type = {bullet_type}, bullet_level = {bullet_level}, bullet_text = {bullet_text}, indentation = {indentation}")           
                paragraph = text_frame.add_paragraph()
                paragraph.text = bullet_text
                paragraph.level = indentation
            #
        else:
            # create a blank bullet point
            paragraph = text_frame.add_paragraph()
            paragraph.text = ""
            paragraph.level = 0
        #
    #

    presentation.save(output_file_path)

    return all_headers
#



def get_flat_list_of_contents(items: list, level: int) -> List[Tuple]:
    """
    Flatten a (hierarchical) list of bullet points to a single list containing each item and
    its level.

    :param items: A bullet point (string or list)
    :param level: The current level of hierarchy
    :return: A list of (bullet item text, hierarchical level) tuples
    """

    flat_list = []

    for item in items:
        if isinstance(item, str):
            flat_list.append((item, level))
        elif isinstance(item, list):
            flat_list = flat_list + get_flat_list_of_contents(item, level + 1)

    return flat_list


if __name__ == '__main__':
    # bullets = [
    #     'Description',
    #     'Types',
    #     [
    #         'Type A',
    #         'Type B'
    #     ],
    #     'Grand parent',
    #     [
    #         'Parent',
    #         [
    #             'Grand child'
    #         ]
    #     ]
    # ]

    # output = get_flat_list_of_contents(bullets, level=0)
    # for x in output:
    #     print(x)

    json_data = '''
    {
    "title": "Understanding AI",
    "slides": [
        {
            "heading": "Introduction",
            "bullet_points": [
                "Brief overview of AI",
                [
                    "Importance of understanding AI"
                ]
            ]
        },
        {
            "heading": "What is AI?",
            "bullet_points": [
                "Definition of AI",
                [
                    "Types of AI",
                    [
                        "Narrow or weak AI",
                        "General or strong AI"
                    ]
                ],
                "Differences between AI and machine learning"
            ]
        },
        {
            "heading": "How AI Works",
            "bullet_points": [
                "Overview of AI algorithms",
                [
                    "Types of AI algorithms",
                    [
                        "Rule-based systems",
                        "Decision tree systems",
                        "Neural networks"
                    ]
                ],
                "How AI processes data"
            ]
        },
        {
            "heading": "Pros of AI",
            "bullet_points": [
                "Increased efficiency and productivity",
                "Improved accuracy and precision",
                "Enhanced decision-making capabilities",
                "Personalized experiences"
            ]
        },
        {
            "heading": "Cons of AI",
            "bullet_points": [
                "Job displacement and loss of employment",
                "Bias and discrimination",
                "Privacy and security concerns",
                "Dependence on technology"
            ]
        },
        {
            "heading": "Future Prospects of AI",
            "bullet_points": [
                "Advancements in fields such as healthcare and finance",
                "Increased use"
            ]
        }
    ]
}'''

    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pptx')
    path = pathlib.Path(temp.name)

    generate_powerpoint_presentation(
        json5.loads(json_data),
        output_file_path=path,
        slides_template='Blank'
    )
