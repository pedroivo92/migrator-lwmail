schema_migration = {
    'type': 'array',
    "minItems": 1,
    "maxItems": 1000,
    "items": {
        "type": "object",
        "properties": {
            "id_globo": {
                "type": "string"
            },
            "person_type": {
                "type": "string"
            },
            "current_email_address": {
                "type": "string"
            },
            "password": {
                "type": "string"
            },
            "name": {
                "type": "string"
            },
            "company_name": {
                "type": "string"
            },
            "cpf": {
                "type": "string"
            },
            "cnpj": {
                "type": "string"
            },
            "rg": {
                "type": "string"
            },
            "phones": {
                "description": "Phones for the costumer..",
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "number": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "number"
                    ]
                },
                "minItems": 1
            },
            "emails": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "address": {
                            "type": "string"
                        },
                        "main": {
                            "type": "boolean"
                        },
                        "confirmed": {
                            "type": "boolean"
                        }
                    },
                    "required": [
                        "address", "main", "confirmed"
                    ]
                },
                "minItems": 1
            },
            "address": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string"
                    },
                    "state": {
                        "type": "string"
                    },
                    "postal_code": {
                        "type": "string"
                    },
                    "country": {
                        "type": "string"
                    },
                    "number": {
                        "type": "string"
                    },
                    "street": {
                        "type": "string"
                    }
                },
                "required": [
                    "city", "state", "postal_code", "country", "number", "street"
                ]
            }
        },
        "required": [
            "id_globo", "person_type", "current_email_address", "password", "cpf", "name", "phones", "emails"
        ]
    }
}
    
schema_migration_status = {
    'type': 'array',
    "minItems": 1,
    "maxItems": 1000,
    "items": {
        "type": "object",
        "properties": {
            "id_globo": {
                "type": "string"
            }
        },
        "required": [
            "id_globo"
        ]
    }
}   

schema_banner = {
    "type": "array",
    "minItems": 1,
    "maxItems": 1000,
    "items": {
        "type": "object",
        "properties": {
            "id_migration": {
                "type": "string"
            },
            "current_email_address": {
                "type": "string"
            },
            "message": {
                "type": "string"
            },
            "background_color": {
                "type": "string"
            },
            "message_link": {
                "type": "string"
            },
            "redirect_link": {
                "type": "string"
            },
            "titulo_alert": {
                "type": "string"
            },
            "message_alert": {
                "type": "string"
            },
            "message_link_alert": {
                "type": "string"
            },
            "redirect_link_alert": {
                "type": "string"
            },
        },
        "required": [
            "id_migration", "current_email_address", "message", "background_color", "message_link", "redirect_link",
            "titulo_alert", "message_alert", "message_link_alert", "redirect_link_alert"
        ]
    }
}