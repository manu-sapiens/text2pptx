
BIG_PPTX_SCHEMA = "{type:object,properties:{slides:{type:array,items:{type:object,properties:{heading:{title:Heading,description:The_slide_Heading,type:string},bullet_points:{title:Bullet_Points,description:The_bullet_points,type:array,items:{type:string}}},required:[heading,bullet_points]}}},required:[slides]}"

BIG_DM_SLIDES_SCHEMA = """
    {
        type: object, 
        properties: {
            slides: {
                type: array, 
                items: {
                    oneOf: [
                        {
                            type: object, 
                            properties: {
                                introduction: {
                                    type: object, 
                                    properties: {
                                        title: {
                                            type: string, 
                                            description: The title text for the Introduction slide }, 
                                        subtitle: {
                                            type: string, 
                                            description: The optional subtitle text for the Introduction slide}}, 
                                    required: [title]}}, 
                            required: [introduction]
                        }, 
                        {
                            type: object, 
                            properties: {
                                section: {
                                    type: object, 
                                    properties: {
                                        title: {
                                            type: string, 
                                            description: The title text for the Section slide}, 
                                        subtitle: {
                                            type: string, 
                                            description: The optional subtitle text for the Section slide}}, 
                                    required: [title]}}, 
                            required: [section]
                        }, 
                        {
                            type: object, 
                            properties: {
                                bullet_slide: {
                                    type: object, 
                                    properties: {
                                        title: {
                                            type: string, 
                                            description: The title text for the Bullet slide},                                         
                                        bullets: {
                                            type: array, 
                                            items: {
                                                type: object, 
                                                properties: {
                                                    text: {
                                                        type: string,
                                                        description: Plain text element for the bullet point}, 
                                                    bullet_level: {
                                                        type: string, 
                                                        enum: [1, 2, 3, 4, 5, 6], 
                                                        description: The indentation level for bullet points}}, 
                                                required: [text, bullet_level]}, 
                                            description: Array of text and bullet elements for the Bulletpoints slide}}, 
                                    required: [bullets]}}, 
                            required: [bullet_slide]
                        },
                        {
                            type: object, 
                            properties: {
                                card: {
                                    type: object, 
                                    properties: {
                                        title: {
                                            type: string, 
                                            description: The title text for the Card},                                         
                                        bullets: {
                                            type: array, 
                                            items: {
                                                type: object, 
                                                properties: {
                                                    text: {
                                                        type: string,
                                                        description: Plain text element for the bullet point}, 
                                                    bullet_level: {
                                                        type: string, 
                                                        enum: [1, 2, 3, 4, 5, 6], 
                                                        description: The indentation level for bullet points}}, 
                                                required: [text, bullet_level]}, 
                                            description: Array of text and bullet elements for the Card}}, 
                                    required: [bullets]}}, 
                            required: [card]
                        }                        
                    ]}}}, 
    required: [slides]
}
"""

org__BIG_DM_SLIDES_SCHEMA = """
    {
        type: object, 
        properties: {
            slides: {
                type: array, 
                items: {
                    oneOf: [{
                        type: object, 
                        properties: {
                            introduction: {
                                type: object, 
                                properties: {
                                    title: {
                                        type: string, 
                                        description: The title text for the Introduction slide }, 
                                    subtitle: {
                                        type: string, 
                                        description: The optional subtitle text for the Introduction slide}}, 
                                required: [title]}}, 
                        required: [introduction]}, {
                        type: object, 
                        properties: {
                            section: {
                                type: object, 
                                properties: {
                                    title: {
                                        type: string, 
                                        description: The title text for the Section slide}, 
                                    subtitle: {
                                        type: string, 
                                        description: The optional subtitle text for the Section slide}}, 
                                required: [title]}}, 
                        required: [section]}, {
                            type: object, 
                            properties: {
                                bulletpoints: {
                                    type: object, 
                                    properties: {
                                        elements: {
                                            type: array, 
                                            items: {
                                                type: object, 
                                                properties: {
                                                    text: {
                                                        type: string,
                                                        description: Plain text element for the bullet point}, 
                                                    bullet_level: {
                                                        type: string, 
                                                        enum: [1, 2, 3, 4, 5, 6], 
                                                        description: The indentation level for bullet points}}, 
                                                required: [text, bullet_level]}, 
                                            description: Array of text and bullet elements for the Bulletpoints slide}}, 
                                required: [elements]}}, 
                    required: [bulletpoints]}]}}}, 
    required: [slides]
}
"""