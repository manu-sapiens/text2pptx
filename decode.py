import re, json

OBSCURE_CHARACTER = 'ˆ'

def decode(schema_string):
    # create a new array to store the parsed schema
    # go through the string character by character
    # if the character is a delimiter (either "{" "}" "[" "]" "," ":") then add it to the parsed array as is
    # if the character is not in that list, take not of the start index and keep going until you find the end index or the next delimiter
    # once you have the start and end index, extract the string and add it to the parsed array
    # however, if a fragment is between backticks ("`"), do not look for diminters between the backticks and remove the backticks from the final string
    
    # Now go through the parsed array and recreate the new string 'schema'
    # If the element is a string, add quotes around it and add it to the schema string
    # If the element is not a string, add it to the schema string as is
    # return schema
    
    parsed = []
    word = "" # a word is anyting that is between delimiters
    backtick_word = False
    
    delimiters = ['{', '}', '[', ']', ',', ':']
    
    length = len(schema_string) 
    for i in range(length):
        c = schema_string[i]
        
        if c == "`":
            if backtick_word:
                # end of a word between backticks. Note that the backticks themselves are discarded
                parsed.append(word)
                backtick_word = False
                word = ""
            else:
                if word == "":
                    # beginning of a word between backticks. Note that the backticks themselves are discarded
                    backtick_word = True
                else:
                    # mid sentence `, so we just add it to the word
                    word += c
                #
            #
        else:        
            if c in delimiters and backtick_word == False:
                # is it a closing delimiter?
                if word != "":
                    parsed.append(word)
                    word = ""
                #
                parsed.append(c)
            else:
                word += c
            #
    #
    if word != "":
        parsed.append(word)
    #

    schema = ""
    for p in parsed:
        if p in delimiters:
            schema += p
        else:
            word = p.strip()
            if word != "": schema += f'"{word}"'
        #
    #
    return schema    
#    
    
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
#schema_string = '{description:this is a description, test:[test_a, test_b], test2: {this:this is another test}}'
#schema_string =  '{`title`:`Entities and Relationships`,`type`:`object`,`properties`:{`entities`:{`type`:`array`,`items`:{`type`:`object`,`properties`:{`id`:{`type`:`string`,`description`:`Unique identifier for the entity`},`name`:{`type`:`string`,`description`:`Name of the entity`},`category`:{`type`:`string`,`description`:`Main category of the entity`},`subcategory`:{`type`:`string`,`description`:`Subcategory under the main category`},`related_entities`:{`type`:`array`,`items`:{`type`:`object`,`properties`:{`id`:{`type`:`string`,`description`:`Unique identifier of the related entity`},`relation_type`:{`type`:`string`,`description`:`Type of the relationship`},`relation_subtype`:{`type`:`string`,`description`:`Subtype of the relationship`},`commentary`:{`type`:`string`,`description`:`Commentary or description of the relationship`}},`required`:[`id`,`relation_type`,`relation_subtype`]},`description`:`List of related entities`}},`required`:[`id`,`name`,`category`,`subcategory`]}}},`required`:[`entities`]}'
simplified_schema = "{title:`Entities, {and} Bob's [Re]lationships`,type:object,properties:{entities:{type:array,items:{type:object,properties:{id:{type:string,description:Unique identifier for the entity},name:{type:string,description:Name's of the entity},category:{type:string,description:Main category of the entity},subcategory:{type:string,description:Subcategory under the main category},related_entities:{type:array,items:{type:object,properties:{id:{type:string,description:Unique identifier of the related entity},relation_type:{type:string,description:Type of the relationship},relation_subtype:{type:string,description:Subtype of the relationship},commentary:{type:string,description:Commentary or description of the relationship}},required:[id,relation_type,relation_subtype]},description:List of related entities}},required:[id,name,category,subcategory]}}},required:[entities]}"

print("-------")
print("simplified_schema = ", simplified_schema)
print("-------")
decoded_schema = decode(simplified_schema) # decode_schema_string(schema_string)
print("decoded_schema =", decoded_schema)

print("-------")
decoded_json = json.loads(decoded_schema)
print("decoded_json =", decoded_json)

print("-------")
