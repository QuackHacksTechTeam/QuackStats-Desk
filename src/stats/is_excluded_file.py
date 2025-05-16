

# Exclude paths that contain libraries and such 
EXCLUDED_PATHS = [
    "node_modules", "bower_components", "dist", "build", "bin",
    "env", "venv", ".env", "__pycache__", ".mypy_cache", ".pytest_cache", ".tox", ".eggs",
    ".git", ".github", ".vscode", ".idea", ".settings", ".project",
    "target", "cmake-build-debug", "cmake-build-release",
    "tmp", "temp", "logs", "coverage", "docs",
    ".DS_Store", "*.log", "*.min.js", "*.map", "*.class", "*.o", "*.obj",
    "*.exe", "*.dll", "*.so", "*.dylib",
    "package-lock.json", "yarn.lock", "poetry.lock", "Pipfile.lock", "Gemfile.lock",
    ".prettierignore", ".eslintignore", ".editorconfig",
    ".babelrc", ".pylintrc", ".flake8", ".stylelintrc",
    "*.iml"
]

# Only count files that are programming languages 
INCLUDED_EXTENSIONS = [
    # General Purpose Languages
    ".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".cs", ".java", ".py",
    ".js", ".mjs", ".cjs", ".ts", ".tsx", ".go", ".rs", ".swift", ".kt", ".kts", ".dart",
    
    # Web Development
    ".html", ".htm", ".css", ".scss", ".sass", ".less", ".php", ".rb", ".aspx", ".cshtml",
    ".twig", ".liquid",

    # Shell and Scripting
    ".sh", ".ps1", ".psm1", ".bat", ".cmd", ".pl", ".perl",

    # Data Science & Config
    ".r", ".jl", ".ipynb",

    # Low-Level & Embedded
    ".asm", ".s", ".v", ".sv", ".vhdl", ".ino",

    # Database & Query
    ".sql", ".psql",

    # Functional Languages
    ".hs", ".lhs", ".ml", ".mli", ".fs", ".fsi", ".fsx", ".clj", ".cljs", ".edn", ".lisp", ".scm", ".rkt",

    # Misc
    ".lua", ".coffee"
]

def is_excluded_file(filename: str) -> bool: 
    """
    Used to check if the file should be excluded or not 

    Three casees exclude a file: 
    
    If the line count is greater than a set threshold. This is here incase
    the other 2 conditions miss a file to exclude

    If the path of the file contains an excluded path, i.e. node_modules

    If the file does not end with an included extension for a programming language 

    """

    if any(excluded_path in filename for excluded_path in EXCLUDED_PATHS):
        return True 

    if not any(filename.endswith(included_ext) for included_ext in INCLUDED_EXTENSIONS): 
        return True

    return False

