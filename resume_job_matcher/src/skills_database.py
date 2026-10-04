"""
skills_database.py
-------------------
A categorized taxonomy of technical and professional skills used for
keyword-based extraction from resumes and job descriptions.

Each skill maps to a list of synonyms/aliases so that variations in
phrasing (e.g. "JS" vs "JavaScript") are still detected.
"""

SKILLS_DATABASE = {
    # ---------------- Programming Languages ----------------
    "python": ["python", "python3"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "c": ["c programming", " c language"],
    "javascript": ["javascript", "js", "es6"],
    "typescript": ["typescript", "ts"],
    "sql": ["sql", "mysql", "postgresql", "t-sql", "pl/sql"],
    "r": ["r programming", "r language"],
    "go": ["golang", " go "],
    "php": ["php"],
    "ruby": ["ruby"],
    "swift": ["swift"],
    "kotlin": ["kotlin"],
    "scala": ["scala"],

    # ---------------- Web / Frameworks ----------------
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "react": ["react", "react.js", "reactjs"],
    "angular": ["angular", "angular.js"],
    "vue": ["vue", "vue.js"],
    "node.js": ["node.js", "nodejs", "node js"],
    "django": ["django"],
    "flask": ["flask"],
    "spring boot": ["spring boot", "spring framework"],
    "express.js": ["express.js", "expressjs"],
    "bootstrap": ["bootstrap"],
    "rest api": ["rest api", "restful api", "rest apis"],
    "graphql": ["graphql"],

    # ---------------- Data Science / ML / AI ----------------
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "natural language processing": ["natural language processing", "nlp"],
    "computer vision": ["computer vision", "cv"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "keras": ["keras"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "opencv": ["opencv"],
    "data analysis": ["data analysis", "data analytics"],
    "data visualization": ["data visualization", "tableau", "power bi"],
    "statistics": ["statistics", "statistical analysis"],
    "spacy": ["spacy"],
    "nltk": ["nltk"],
    "llm": ["llm", "large language model", "generative ai", "genai"],

    # ---------------- Databases ----------------
    "mongodb": ["mongodb", "mongo db"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "oracle": ["oracle db", "oracle database"],
    "firebase": ["firebase"],
    "redis": ["redis"],

    # ---------------- Cloud / DevOps ----------------
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "ci/cd": ["ci/cd", "continuous integration", "continuous deployment"],
    "jenkins": ["jenkins"],
    "git": ["git", "github", "gitlab", "version control"],
    "linux": ["linux", "unix"],

    # ---------------- Software Engineering ----------------
    "data structures": ["data structures", "dsa"],
    "algorithms": ["algorithms"],
    "object oriented programming": ["oop", "object oriented programming", "object-oriented"],
    "system design": ["system design"],
    "microservices": ["microservices"],
    "agile": ["agile", "scrum", "kanban"],
    "testing": ["unit testing", "test automation", "junit", "pytest"],

    # ---------------- Soft / Professional Skills ----------------
    "communication": ["communication skills", "communication"],
    "teamwork": ["teamwork", "collaboration", "team player"],
    "leadership": ["leadership"],
    "problem solving": ["problem solving", "problem-solving"],
    "time management": ["time management"],
    "project management": ["project management", "pmp"],
}


def get_all_skills():
    """Return the flat list of canonical skill names."""
    return list(SKILLS_DATABASE.keys())
