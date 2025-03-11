moderation_prompt = \
"""
Moderate the following user message:
---------------
{message}
---------------

Please provide a response in JSON format with the following fields:

cyberbullying: boolean
notAgeAppropriate: boolean
personalInfo: boolean
strangerDanger: boolean
languageFilter: boolean
negativeCommunication: boolean
"""