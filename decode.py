import re

OBSCURE_CHARACTER = 'ˆ'
def decode_schema_string(schema_string):
    # Step 1: Replace spaces within backticks with a rare character and remove the backticks
    schema_string = re.sub(r'`([^`]*)`', lambda match: match.group(1).replace(' ', OBSCURE_CHARACTER), schema_string)

    # Step 2: Split the string using regex to match sequences of word characters or non-word characters
    split_list = re.findall(r'\w+|\W+', schema_string)

    # Step 3: Reconstitute the string, adding quotes around words
    schema = ''.join(f'"{part}"' if re.match(r'^[a-zA-Z_]\w*$', part) else part for part in split_list)

    # Step 4: Replace the rare character back with spaces
    schema = schema.replace(OBSCURE_CHARACTER, ' ')
    return schema

# Example usage
#schema_string = '{description:`this is a description`, test:test, test2: `this is a test`}'
schema_string =  '{`title`:`Entities and Relationships`,`type`:`object`,`properties`:{`entities`:{`type`:`array`,`items`:{`type`:`object`,`properties`:{`id`:{`type`:`string`,`description`:`Unique identifier for the entity`},`name`:{`type`:`string`,`description`:`Name of the entity`},`category`:{`type`:`string`,`description`:`Main category of the entity`},`subcategory`:{`type`:`string`,`description`:`Subcategory under the main category`},`related_entities`:{`type`:`array`,`items`:{`type`:`object`,`properties`:{`id`:{`type`:`string`,`description`:`Unique identifier of the related entity`},`relation_type`:{`type`:`string`,`description`:`Type of the relationship`},`relation_subtype`:{`type`:`string`,`description`:`Subtype of the relationship`},`commentary`:{`type`:`string`,`description`:`Commentary or description of the relationship`}},`required`:[`id`,`relation_type`,`relation_subtype`]},`description`:`List of related entities`}},`required`:[`id`,`name`,`category`,`subcategory`]}}},`required`:[`entities`]}'
decoded_schema = decode_schema_string(schema_string)

print("decoded_schema =", decoded_schema)