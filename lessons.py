lessons = {
    "Python": {
        "1. Print Commands": {
            "summary": "The `print()` function is Python's way of displaying text or numbers onto the screen.",
            "challenge": "Use print() to display 'Hello, Arcade!' on the TV screen.",
            "video": "python_print.mp4",
            "starter_code": "print('Hello, Arcade!')",
            "quiz": {
                "question": "Which command is used to display output on the screen in Python?",
                "options": [
                    'print("Hello World")',
                    'System.out.println("Hello World")',
                    'echo "Hello World"',
                    'console.log("Hello World")'
                ],
                "correct": 'print("Hello World")'
            }
        },
        "2. Syntax Rules": {
            "summary": "Python relies on clean indentation and proper punctuation to understand code blocks.",
            "challenge": "Fix the indentation or syntax in a simple Python script.",
            "video": "python_syntax.mp4",
            "starter_code": "if True:\n    print('Correct Syntax!')",
            "quiz": {
                "question": "What does Python use to define code blocks instead of curly braces?",
                "options": ["Indentation", "Semicolons", "Parentheses", "Colons only"],
                "correct": "Indentation"
            }
        },
        "3. Variables": {
            "summary": "Variables are containers for storing data values, like score = 100.",
            "challenge": "Create a variable named player_score and assign it value 50.",
            "video": "python_vars.mp4",
            "starter_code": "player_score = 50\nprint(player_score)",
            "quiz": {
                "question": "How do you correctly assign a value to a variable in Python?",
                "options": ["x == 10", "x = 10", "10 = x", "var x = 10"],
                "correct": "x = 10"
            }
        },
        "4. Global Variables": {
            "summary": "Global variables can be accessed throughout your entire program scope.",
            "challenge": "Define a global variable outside a function and read it inside.",
            "video": "python_global.mp4",
            "starter_code": "score = 100\n\ndef show_score():\n    print(score)\n\nshow_score()",
            "quiz": {
                "question": "Where are global variables defined?",
                "options": ["Inside a function", "Outside any function", "Only in loops", "Inside classes only"],
                "correct": "Outside any function"
            }
        },
        "5. Loops": {
            "summary": "Loops let you repeat blocks of code multiple times efficiently using `for` or `while`.",
            "challenge": "Write a loop that prints numbers from 1 to 3.",
            "video": "python_loops.mp4",
            "starter_code": "for i in range(1, 4):\n    print(i)",
            "quiz": {
                "question": "Which loop keyword is typically used to iterate over a sequence in Python?",
                "options": ["repeat", "for", "loop", "iterate"],
                "correct": "for"
            }
        }
    },
    "Java": {
        "1. Print Commands": {
            "summary": "Java uses `System.out.println()` to output text to the console terminal.",
            "challenge": "Write a Java print statement to display 'Java Arcade'.",
            "video": "java_print.mp4",
            "starter_code": 'System.out.println("Java Arcade");',
            "quiz": {
                "question": "Which command does Java use to print text to the screen?",
                "options": [
                    'print("Hello World")',
                    'System.out.println("Hello World")',
                    'echo "Hello World"',
                    'console.log("Hello World")'
                ],
                "correct": 'System.out.println("Hello World")'
            }
        },
        "2. Syntax Rules": {
            "summary": "Every Java statement must end with a semicolon (;), and code lives inside classes.",
            "challenge": "Add a missing semicolon to a Java statement.",
            "video": "java_syntax.mp4",
            "starter_code": 'int points = 50;',
            "quiz": {
                "question": "What symbol must end almost every statement in Java?",
                "options": [".", ",", ";", ":"],
                "correct": ";"
            }
        },
        "3. Variables": {
            "summary": "Java is statically typed, meaning you must declare the data type (like `int` or `String`) before the variable name.",
            "challenge": "Declare an integer variable named level with value 5.",
            "video": "java_vars.mp4",
            "starter_code": 'int level = 5;',
            "quiz": {
                "question": "What must you declare before a variable name in Java?",
                "options": ["The data type", "The color", "The screen size", "Nothing"],
                "correct": "The data type"
            }
        },
        "4. Global Variables": {
            "summary": "Global or class-level variables in Java are usually marked as `static` so they can be accessed easily.",
            "challenge": "Create a static int variable inside a class.",
            "video": "java_global.mp4",
            "starter_code": 'public class Main {\n    static int highScore = 500;\n}',
            "quiz": {
                "question": "Which keyword is typically used for class-level variables in Java?",
                "options": ["static", "global", "shared", "public_var"],
                "correct": "static"
            }
        },
        "5. Loops": {
            "summary": "Java uses `for`, `while`, and `do-while` loops for repetitive tasks.",
            "challenge": "Write a standard `for` loop counting from 1 to 3.",
            "video": "java_loops.mp4",
            "starter_code": 'for(int i=1; i<=3; i++) {\n    System.out.println(i);\n}',
            "quiz": {
                "question": "Which loop structure is commonly used for counted repetition in Java?",
                "options": ["for loop", "repeat loop", "loop-to", "count loop"],
                "correct": "for loop"
            }
        }
    },
    "JavaScript": {
        "1. Print Commands": {
            "summary": "JavaScript uses `console.log()` to print out messages and debug values.",
            "challenge": "Use console.log() to print 'JS Ninja active!'.",
            "video": "js_print.mp4",
            "starter_code": "console.log('JS Ninja active!');",
            "quiz": {
                "question": "What function does JavaScript use to log messages to the console?",
                "options": [
                    'print("Hello World")',
                    'System.out.println("Hello World")',
                    'echo "Hello World"',
                    'console.log("Hello World")'
                ],
                "correct": 'console.log("Hello World")'
            }
        },
        "2. Syntax Rules": {
            "summary": "JavaScript is flexible with semicolons and uses camelCase naming conventions.",
            "challenge": "Write a valid variable assignment using camelCase.",
            "video": "js_syntax.mp4",
            "starter_code": "let playerCoins = 100;",
            "quiz": {
                "question": "Which naming convention joins multiple words with a capital letter like `playerCoins`?",
                "options": ["camelCase", "snake_case", "kebab-case", "flatcase"],
                "correct": "camelCase"
            }
        },
        "3. Variables": {
            "summary": "JavaScript uses `let`, `const`, and `var` to declare variables.",
            "challenge": "Declare a constant variable for max health.",
            "video": "js_vars.mp4",
            "starter_code": "const MAX_HEALTH = 100;",
            "quiz": {
                "question": "Which keyword defines a constant value in JavaScript that won't change?",
                "options": ["const", "let", "var", "fixed"],
                "correct": "const"
            }
        },
        "4. Global Variables": {
            "summary": "Variables declared outside of functions or blocks in JavaScript have global scope.",
            "challenge": "Declare a global variable at the top of your script.",
            "video": "js_global.mp4",
            "starter_code": "let gameActive = true;\n\nfunction checkStatus() {\n    console.log(gameActive);\n}",
            "quiz": {
                "question": "How do you make a variable global in JavaScript?",
                "options": ["Declare it outside of any function or block", "Use the global keyword", "Put it inside brackets", "Type uppercase letters"],
                "correct": "Declare it outside of any function or block"
            }
        },
        "5. Loops": {
            "summary": "JavaScript supports `for`, `while`, and modern array looping methods like `.forEach()`.",
            "challenge": "Write a quick `for` loop in JavaScript.",
            "video": "js_loops.mp4",
            "starter_code": "for (let i = 0; i < 3; i++) {\n    console.log(i);\n}",
            "quiz": {
                "question": "Which keyword is used to initialize loop counters in modern JavaScript loops?",
                "options": ["let", "var", "int", "loop"],
                "correct": "let"
            }
        }
    }
}