moderation_prompt = \
"""
Moderate the following user message:
---------------
Hello! Can you help me with my homework?
---------------

Please provide a response in JSON format with the following fields:

cyberbullying: boolean
notAgeAppropriate: boolean
personalInfo: boolean
strangerDanger: boolean
languageFilter: boolean
negativeCommunication: boolean

For example:
{
    "cyberbullying": false,
    "notAgeAppropriate": false,
    "personalInfo": false,
    "strangerDanger": true,
    "languageFilter": false,
    "negativeCommunication": false
}
"""