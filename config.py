# keywords = {
#     'high_level': [
#         'machine_learning', 'natural_language_processing', 'optical_character_recognition',
#         'deep_learning', 'cybersecurity', 'artificial_intelligence', 'quantum_computing',
#         'blockchain', 'predictive_models', 'threat_detection', 'neural_networks', 'cloud_security',
#         'edge_computing', 'autonomous_systems', 'big_data', 'data_science', 'computer_vision',
#         'reinforcement_learning', 'internet_of_things', '5G_technology'
#     ],
#     'medium_level': [
#         'flask', 'mysql', 'sqlalchemy', 'bootstrap', 'figma', 'role_based_access_control',
#         'data_management', 'database_schema', 'security_testing', 'performance_optimization',
#         'horizontal_scaling', 'devops', 'docker', 'cloud_computing', 'encryption',
#         'referential_integrity', 'modular_architecture', 'api_integration', 'microservices',
#         'containerization', 'serverless_architecture', 'continuous_integration'
#     ],
#     'low_level': [
#         'modular_design', 'user_interface', 'responsive_design', 'mobile_compatibility',
#         'authentication', 'authorization', 'secure_authentication', 'system_performance',
#         'UI_UX_principles', 'data_consistency', 'software_architecture', 'scalability',
#         'secure_access_control', 'index_numbers', 'real_time_feedback', 'dynamic_UI',
#         'session_management', 'load_balancing', 'cross_browser_compatibility', 'web_accessibility',
#         'error_handling', 'form_validation', 'data_validation', 'debugging'
#     ]
# }

# Configuration file for the AI-based question generation system

# Keywords for difficulty levels
keywords = {
    "low_level": [
        "html", "css", "javascript", "database", "api", "interface", "frontend", "backend",
        "testing", "documentation", "version control", "git", "debugging", "programming",
        "function", "variable", "loop", "condition", "class", "object", "method"
    ],

    "medium_level": [
        "flask", "django", "react", "angular", "vue", "bootstrap", "tailwind",
        "sqlalchemy", "orm", "mvc", "rest", "graphql", "docker", "ci/cd",
        "devops", "agile", "scrum", "kanban", "microservices", "nosql",
        "authentication", "authorization", "security", "performance", "scalability",
        "data modeling", "api gateway", "monitoring", "logging"
    ],

    "high_level": [
        "machine_learning", "artificial intelligence", "deep learning", "neural network",
        "distributed systems", "cloud architecture", "serverless", "kubernetes",
        "system design", "high availability", "disaster recovery", "fault tolerance",
        "load balancing", "caching strategies", "event-driven architecture",
        "microservices architecture", "domain-driven design", "blockchain",
        "quantum computing", "edge computing", "internet of things", "big data",
        "data science", "natural language processing", "computer vision",
        "reinforcement learning", "data engineering", "data warehousing"
    ]
}

# Configuration for spaCy NLP model
nlp_config = {
    "model": "en_core_web_sm",
    "disable": ["parser"]  # Disable components not needed for question generation
}

# Configuration for BERT model
bert_config = {
    "model": "paraphrase-MiniLM-L6-v2",
    "similarity_threshold": 0.7  # Minimum similarity score for valid questions
}

# Question generation parameters
question_config = {
    "min_question_length": 7,
    "max_question_length": 30,
    "min_answer_length": 5,
    "max_answer_length": 100,
    "min_options": 4,
    "max_options": 4  # Maximum number of answer options
}

# File handling parameters
file_config = {
    "allowed_extensions": ["pdf", "docx", "txt", "pptx"],
    "max_file_size_mb": 10,
    "min_paragraphs": 1,
    "max_paragraphs": 100
}

# Default settings
default_config = {
    "default_difficulty": "Medium Level",
    "questions_per_request": 10,
    "min_paragraph_length": 50,
    "max_paragraph_length": 500
}