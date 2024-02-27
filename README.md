# Gemini-Coder
![cover_logo](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/logo.png?raw=true "")</br>
### **Hosting and Spaces:**
[![Plugin](https://img.shields.io/badge/Bard%20Coder-Repo-blue)](https://replit.com/@HaseebMir/AutoBard-Coder)
[![Plugin](https://img.shields.io/badge/Bard%20Coder-Replit-blue)](https://autobard-coder.haseebmir.repl.co)
[![Plugin](https://img.shields.io/badge/Code%20Interpreter-HuggingFace-blue)](https://huggingface.co/spaces/haseeb-heaven/AutoBard-Coder)
[![Plugin](https://img.shields.io/badge/Code%20Interpreter-CodeSpace-blue)](https://haseeb-heaven-legendary-guide-x555j7vpv4phprg6-8501.preview.app.github.dev/)</br>
<a href="https://www.buymeacoffee.com/haseebheaven"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=haseebheaven&button_colour=40DCA5&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00" /></a>

## 🌟 General Information 🌟
**Gemini-Coder** is a _code generator_ and _code interpreter_ for [Google Gemini](https://gemini.google.com/).🙌👩‍💻👨‍💻 It now uses the **Official** [Gemini API](https://makersuite.google.com/app/apikey) provided by Google, which is safe to use. 🛡️
This application interacts with Google Bard and refines the results for coding purposes. 🎯
The main purpose of this is for **research** 🧪 and **educational** 🎓 purposes. It can be very useful for **data analysis** 📊 and **Programmers** 💻.

## Application main UI.
### GeminiCoder:
![gemini_coder](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/bardcoder_main.png?raw=true "")</br>

### Code Interpreter:
![code_interpreter](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/code_interpreter_main_ui.png?raw=true "")</br>

## Setup Process - OUTDATED
~~To set up AutoBard-Coder, you will need to install the dependencies: `streamlit` and `bardapi`.~~ </br>
~~You will also need to authenticate with the Bard API by visiting https://bard.google.com/,~~ </br>
~~- Opening the console with F12~~ </br>
~~- Going to **Application** → **Cookies**, and copying the value of the **__Secure-1PSID** cookie.~~</br>
~~- Then you can setup the key to your **local environment** by running the following command:~~</br>
~~```export _BARD_API_KEY=<__Secure-1PSID value>``` Remember the `_` before `BARD_API_KEY` is important.~~ </br></br>


## Installation Guide - UPDATED

*Step 1:* **Obtain the Google Palm API key.**

*Step 2:* Visit the following URL: *https://makersuite.google.com/app/apikey*

*Step 3:* Click on the **Create API Key** button.

*Step 4:* The generated key is your API key. Please make sure to **copy** it and **paste** it in the required field below.

*Note:* The API key is crucial for the functioning of the AutoBard-Coder. Please ensure to keep it safe and do not share it with anyone.

## Usage
There are 3 components of this application:
1. **_Geminioder_**: A coding assistant from Gemini which automatically generates code from Gemini responses and refines it for coding purposes. This can be used by developers to get the correct code from Gemini when they need help because the output is refined and fixed multiple times to provide the correct code.
- File: `bardcoder.py`

2. **_Code Interpreter_**: This is an interpreter for Gemini which can be used to run the code generated from Geminicoder. This can be very useful for all users who want to do data analysis and machine learning with Gemini. This can generate graphs and charts from Gemini responses and can be used to do data analysis.
- File: `Geminicode_interpreter.py`

3. **_GeminiCoder Lib_**: This is a library for Geminicoder which can be used to generate code from bard responses and refine it for coding purposes. You can use it to build your own application using Gemini.
- File: `bardcoder_lib.py`

## Using BardCoder:
To use GeminiCoder, you will need to run the following command:
```python bardcoder.py```
This will open the GeminiCoder UI in the terminal. And will be asked to enter prompts for Gemini.
![bard_coder](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/bardcoder_main.png?raw=true "")</br>
Not this assumes you have already set the `API KEY` in your local environment. If you have not, please refer to the setup process.
The code generated will be placed in folder `codes` and the response will be placed in folder `response`.

## Using Code Interpreter:
To use Code Interpreter, you will need to run the following command:</br>
```streamlit run bardcode_interpreter.py```</br></br>
If you need to Disable CORS Headers, you can run the following command:</br>
```streamlit run bardcode_interpreter.py --server.enableCORS false --server.enableXsrfProtection false```</br></br>
This will open the Code Interpreter UI in the Web Browser. And will be asked to enter prompts for bard.
![code_interpreter](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/code_interpreter_main_ui.png?raw=true "")</br>

Now this assumes you have already set the `API KEY` in your local environment. If you have not, please refer to the setup process.
You can also setup the `API KEY` in the UI settings.</br>
![code_interpreter_settings](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/code_interpreter_settings.png?raw=true "")</br>

Before prompting you should check the **Options** to change **Filenames** and **Filepaths** and other settings.</br>

### Uploading data for data analysis:
You can set the `Upload Data` in **Options** to upload data for data analysis. (Right now this only supports Text files).
![upload_data_ui](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/upload_data_ui.png?raw=true "")</br>

After uploading the files you can ask for the prompts from Gemini. And you will get the output like this.
![upload_data_output](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/upload_data_output.png?raw=true "")</br>

You can also set the `Expected Output` in **Options** to get the **Accuracy** of the code generated.
![expected_output](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/code_interpreter_expected_output.png?raw=true "")</br>

And output will be generated like this with hilighting the **Accuracy** of the code generated.
![expected_output](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/code_interpreter_output.png?raw=true "")</br>

### Sharing code with others:
You can share code with others by using the **ShareGPT** feature. You will get sharable link for your code.
![bard_code_share](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/bard_code_share.png?raw=true "")</br>

### Code Interpreter Demo:
[Code Interpreter Demo](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/code_interpreter_demo.webm)</br>
[![code_interpreter_demo](https://img.youtube.com/vi/Flg1qUzs9ew/0.jpg)](https://youtube.com/shorts/Flg1qUzs9ew)

The code generated will be placed in folder `codes` and the response will be placed in folder `response` and upload files will be placed in folder `uploads`.

### Safety and Measures:
This now has **safety measures** built in _Code Interpreter_ and now it can detect the **safety** of the code generated and can **fix** it.</br>
So now all the repo and code in **READ_ONLY** mode. And you can only run the code in **READ_ONLY** mode.</br>
All the commands which **__changes,move,delete,rename__** files are disabled in **READ_ONLY** mode.</br>
This has advanced **safety measures** and can detect the **safety** of the code generated and can **fix** it.</br>
![safety_output](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/safety_output.png?raw=true "")</br>


### Graphs and Visual Charts output:
To get Graphs and Charts output for your data visualization, you will install python packages `matplotlib`, `seaborn`, `cartopy`, `plotnine` and more. and run the following command: </br>
```python bardcode_interpreter.py``` </br>
And ask for the prompts from Gemini. And you will get the output like this:
Example Prompt:
```
In Python write me program to.
1.Read the data from file called 'employees.json'
2.Count no. of Males and Females in file.
4.Draw PIE graph of these in using Python Matplotlib.
5.Show me that output.
```

And you will get output like this.
![expected_output](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/employees_chart.png?raw=true "")</br>

## Directory Structure
This application uses the Gemini API to interact with Gemini and refine the results for coding purposes. All data that is generated is stored in the following directories:
- `response`: This directory contains all the responses from Gemini.
- `codes`: This directory contains all the code generated from Gemini.
- `uploads`: This directory contains all the data that is uploaded to Gemini.
- `lib`: This directory contains all the libraries for Geminicoder.
- `resources`: This directory contains all the resources for Geminicoder.

## Features
Some of the features of Gemini-Coder include:
- **Automatic** _code generation_ from Gemini responses
- **Refinement** of code for coding purposes
- Ability to **fix/debug** its own code
- Ability to generate **single** or **multiple** responses from Gemini
- Ability to **save** responses and run them locally
- Ability to access _local files_ for code interpretation
- **Data analysis** and machine learning capabilities
- **Graphs** and **Charts** generation from Gemini responses
- Ability to **upload files** for data analysis and machine learning.
- Share code with others with powerered by **ShareGPT**.
- Advanced **safety measures** to detect the safety of the code generated.

## Help Section.
Now you can get help directly from the application. You can get help by clicking on the **Help** button in the UI.
![code_interpreter_help](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/code_interpreter_help.png?raw=true "")</br>

## Changelog 📝

All notable changes to this project will be documented in this file.

[CHANGELOGS](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/CHANGELOGS.md)

---

| Version | Date       | Added                                              | Fixed                |
| ------- | ---------- | -------------------------------------------------- | -------------------- |
| 1.4     | 2023-09-28 | - Added Palm 2 Official API now. | - Settings and Logs and Bug fixes |
| 1.3     | 2023-05-29 | - **Updated** with totally new _UI_ and _UX_. 🎨<br>- Updated security for code checking and prompt checking. 🔒<br>- Added new Help section. 🆘 | - Fixed API Key issues. |
| 1.2     | 2023-05-28 | - Advanced security for code and prompt checking. 🔒<br>- Support for graphs, charts, and tables. 📊<br>- More libraries for data science. 🧬 |                      |
| 1.1     | 2023-05-27 | - Upload files option. 📤<br>- API key settings. 🔑  | - Error handling from server. 🛠 |
| 1.0     | 2023-05-26 | - Auto barcode generator. 🏷<br>- Auto barcode interpreter. 🔎 |                      |




## License and Author
Gemini-Coder was created by HeavenHM and is licensed under the MIT license.
