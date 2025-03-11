tool_list = [
    {
        "toolSpec": {
            "name": "chat_moderation",
            "description": "Moderate user message for nickname cyberbullying, age appropriateness, personal information, stranger danger, language filter, and negative communication.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "cyberbullying": {
                            "type": "boolean",
                            "description": "Evaluation of cyberbullying.",
                        },
                        "notAgeAppropriate": {
                            "type": "boolean",
                            "description": "Evaluation of age appropriateness.",
                        },
                        "personalInfo": {
                            "type": "boolean",
                            "description": "Evaluation of personal information sharing.",
                        },
                        "strangerDanger": {
                            "type": "boolean",
                            "description": "Evaluation of stranger danger.",
                        },
                        "languageFilter": {
                            "type": "boolean",
                            "description": "Evaluation of language filter.",
                        },
                        "negativeCommunication": {
                            "type": "boolean",
                            "description": "Evaluation of negative communication.",
                        },
                    },
                    "required": ["cyberbullying", "notAgeAppropriate", "personalInfo", "strangerDanger", "languageFilter", "negativeCommunication"],
                }
            },
        },
    }
]