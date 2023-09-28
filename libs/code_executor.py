# general_utils.py
import base64
import os
import tempfile
from libs.logger import logger
import subprocess
import traceback
import libs.extensions_map as extensions_map
from libs.extensions_map import get_file_extesion

def LangCodes():
    
    LANGUAGE_CODES = {
        'C': 'c',
        'C++': 'cpp',
        'Java': 'java',
        'Ruby': 'ruby',
        'Scala': 'scala',
        'C#': 'csharp',
        'Objective C': 'objc',
        'Swift': 'swift',
        'JavaScript': 'nodejs',
        'Kotlin': 'kotlin',
        'Python': 'python3',
        'GO Lang': 'go',
    }
    return LANGUAGE_CODES

class CodeExecutor:
    def __init__(self, compiler_mode: str, code: str,language: str,code_extenstion: str):
        self.compiler_mode = compiler_mode
        self.language = language
        self.code = code
        self.extracted_code = code
        self.code_extenstion = code_extenstion
    
    def execute_code(self, compiler_mode: str, code: str,language: str):
        
        if not code or len(code.strip()) == 0 or not language or len(language.strip()) == 0:
            logger.error("Error in code execution: Generated code is empty.")
            return
        
        logger.info(f"Executing code: {code[:50]} in language: {language} with Compiler Mode: {compiler_mode}")

        try:
            if len(code) == 0 or code == "":
                return
            
            if compiler_mode.lower() == "online":
                html_content = self.generate_dynamic_html(language, code)
                logger.info(f"HTML Template: {html_content[:100]}")
                return html_content

            else:
                output = self.run_code(code, language)
                
                # Check for errors in code execution
                if "error" in output.lower() or "exception" in output.lower() or "SyntaxError" in output.lower() or "NameError" in output.lower():
                    output = "There were Error in output code"
                return output

        except Exception as e:
            logger.error(f"Error in code execution: {traceback.format_exc()}")

    def check_compilers(self, language):
        language = language.lower().strip()
        
        compilers = {
            "python": ["python", "--version"],
            "nodejs": ["node", "--version"],
            "c": ["gcc", "--version"],
            "c++": ["g++", "--version"],
            "csharp": ["csc", "--version"],
            "go": ["go", "version"],
            "ruby": ["ruby", "--version"],
            "java": ["java", "--version"],
            "kotlin": ["kotlinc", "--version"],
            "scala": ["scala", "--version"],
            "swift": ["swift", "--version"]
        }

        if language not in compilers:
            logger.error("Invalid language selected.")
            return False

        compiler = subprocess.run(compilers[language], capture_output=True, text=True)
        if compiler.returncode != 0:
            logger.error(f"{language.capitalize()} compiler not found.")
            return False

        return True
    
    def run_code(self,code, language):
        language = language.lower()
        logger.info(f"Running code: {code[:100]} in language: {language}")

        # Check for code and language validity
        if not code or len(code.strip()) == 0:
            return "Code is empty. Cannot execute an empty code."
        
        # Check for compilers on the system
        compilers_status = self.check_compilers(language)
        if not compilers_status:
            return "Compilers not found. Please install compilers on your system."
        
        if language == "python":
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=True) as file:
                file.write(code)
                file.flush()

                logger.info(f"Input file: {file.name}")
                output = subprocess.run(
                    ["python", file.name], capture_output=True, text=True)
                logger.info(f"Runner Output execution: {output.stdout + output.stderr}")
                return output.stdout + output.stderr

        elif language == "c" or language == "c++":
            ext = ".c" if language == "c" else ".cpp"
            with tempfile.NamedTemporaryFile(mode="w", suffix=ext, delete=True) as src_file:
                src_file.write(code)
                src_file.flush()

                logger.info(f"Input file: {src_file.name}")

                with tempfile.NamedTemporaryFile(mode="w", suffix="", delete=True) as exec_file:
                    compile_output = subprocess.run(
                        ["gcc" if language == "c" else "g++", "-o", exec_file.name, src_file.name], capture_output=True, text=True)

                    if compile_output.returncode != 0:
                        return compile_output.stderr

                    logger.info(f"Output file: {exec_file.name}")
                    run_output = subprocess.run(
                        [exec_file.name], capture_output=True, text=True)
                    logger.info(f"Runner Output execution: {run_output.stdout + run_output.stderr}")
                    return run_output.stdout + run_output.stderr

        elif language == "javascript":
            with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=True) as file:
                file.write(code)
                file.flush()

                logger.info(f"Input file: {file.name}")
                output = subprocess.run(
                    ["node", file.name], capture_output=True, text=True)
                logger.info(f"Runner Output execution: {output.stdout + output.stderr}")
                return output.stdout + output.stderr
            
        elif language == "java":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".java", delete=True) as file:
                    file.write(code)
                    file.flush()
                    classname = "Main"  # Assuming the class name is Main, adjust if needed
                    compile_output = subprocess.run(["javac", file.name], capture_output=True, text=True)
                    if compile_output.returncode != 0:
                        return compile_output.stderr
                    run_output = subprocess.run(["java", "-cp", tempfile.gettempdir(), classname], capture_output=True, text=True)
                    return run_output.stdout + run_output.stderr

        elif language == "swift":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".swift", delete=True) as file:
                    file.write(code)
                    file.flush()
                    output = subprocess.run(["swift", file.name], capture_output=True, text=True)
                    return output.stdout + output.stderr

        elif language == "c#":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".cs", delete=True) as file:
                    file.write(code)
                    file.flush()
                    compile_output = subprocess.run(["csc", file.name], capture_output=True, text=True)
                    if compile_output.returncode != 0:
                        return compile_output.stderr
                    exe_name = file.name.replace(".cs", ".exe")
                    run_output = subprocess.run([exe_name], capture_output=True, text=True)
                    return run_output.stdout + run_output.stderr

        elif language == "scala":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".scala", delete=True) as file:
                    file.write(code)
                    file.flush()
                    output = subprocess.run(["scala", file.name], capture_output=True, text=True)
                    return output.stdout + output.stderr

        elif language == "ruby":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".rb", delete=True) as file:
                    file.write(code)
                    file.flush()
                    output = subprocess.run(["ruby", file.name], capture_output=True, text=True)
                    return output.stdout + output.stderr

        elif language == "kotlin":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".kt", delete=True) as file:
                    file.write(code)
                    file.flush()
                    compile_output = subprocess.run(["kotlinc", file.name, "-include-runtime", "-d", "output.jar"], capture_output=True, text=True)
                    if compile_output.returncode != 0:
                        return compile_output.stderr
                    run_output = subprocess.run(["java", "-jar", "output.jar"], capture_output=True, text=True)
                    return run_output.stdout + run_output.stderr

        elif language == "go":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".go", delete=True) as file:
                    file.write(code)
                    file.flush()
                    compile_output = subprocess.run(["go", "build", "-o", "output.exe", file.name], capture_output=True, text=True)
                    if compile_output.returncode != 0:
                        return compile_output.stderr
                    run_output = subprocess.run(["./output.exe"], capture_output=True, text=True)
                    return run_output.stdout + run_output.stderr
        else:
            return "Unsupported language."
        
    # Generate Dynamic HTML for JDoodle Compiler iFrame Embedding.
    def generate_dynamic_html(self,language, code_prompt):
        logger.info("Generating dynamic HTML for language: %s", language)
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Online JDoodle Compiler</title>
        </head>
        <body>
            <div data-pym-src='https://www.jdoodle.com/plugin' data-language="{language}"
                data-version-index="0" data-libs="" >{script_code}
            </div>
            <script src="https://www.jdoodle.com/assets/jdoodle-pym.min.js" type="text/javascript"></script>
        </body>
        </html>
        """.format(language=LangCodes()[language], script_code=code_prompt)
        return html_template
    
            # get the code extension from bard response - automatically detects the language from bard response.
    
    def get_code_extension(self, code=None):
        try:
            code = code if code else self.code
            logger.info(f"Getting code extension from code {code[:100]}")
            if code and not code in "can't help":
                self.code_extension = code.split('```')[1].split('\n')[0]
                logger.info(f"Code extension: {self.code_extension}")
                return self.code_extension
        except Exception as exception:
            stack_trace = traceback.format_exc()
            logger.error(f"Error occurred while getting code extension: {exception}")
            raise Exception(stack_trace)
        return None
    
    def save_code(self,code,filename):
        try:
            logger.info(f"Saving code {code[:100]} with filename: {filename}")
            self.code = code
            self.code_extenstion = '.' + self.get_code_extension()
            logger.info(f"Code extension: {self.code_extenstion}")
            if code:
                code = code.replace("\\n", "\n").replace("\\t", "\t")
                logger.info(f"Saving code with filename: {filename} and extension: {self.code_extenstion} and code: {code}")

                # Add extension to filename
                extension = extensions_map.get_file_extesion(self.code_extenstion) or self.code_extenstion
                filename = filename + extension

                with open(filename, 'w') as file:
                    file.write(self.extracted_code)
                    logger.info(f"{filename} saved.")
                return filename
        except Exception as exception:
            stack_trace = traceback.format_exc()
            logger.error(f"Error occurred while saving code: {exception}")
            raise Exception(stack_trace)
            return None

    # save multiple codes from bard response
    def save_code_choices(self, filename):
        try:
            logger.info(f"Saving code choices with filename: {filename}")
            extension = self.get_code_extension()
            if extension:
                self.code_extension = '.' + extension
                self.code_extension = extensions_map.get_file_extesion(self.code_extenstion) or self.code_extenstion

            for index, choice in enumerate(self.code_choices):
                choice_content = self.get_code_choice(index)
                logger.info(f"Enumerated Choice content: {choice}")
                self.save_file("codes/"+filename+'_'+str(index+1) + self.code_extension, choice_content)
        except Exception as exception:
            stack_trace = traceback.format_exc()
            logger.error(f"Error occurred while saving code choices: {exception}")
            raise Exception(stack_trace)
                