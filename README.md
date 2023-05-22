# AutoBard-Coder
![cover_logo](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/logo.png?raw=true "")</br>

## General Information
AutoBard-Coder is a code generator for bard.🙌👩‍💻👨‍💻 It uses the Bard API to interact with bard and refine the results for coding purposes. The main purpose of this is for research and educational purposes. This can generate code from prompts and fix itself unless the code is fixed. It is written in Python and has dependencies on streamlit and bard-coder.

## Application main UI.
### BardCoder:
![bard_coder](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/bardcoder_main.png?raw=true "")</br>

### Coder Interpreter:
![code_interpreter](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/code_interpreter_main_ui.png?raw=true "")</br>

## Setup Process
To set up AutoBard-Coder, you will need to install the dependencies: `streamlit` and `bardapi`. </br>
You will also need to authenticate with the Bard API by visiting https://bard.google.com/, </br>
1.Opening the console with F12 </br>
2.Going to **Application** → **Cookies**, and copying the value of the **__Secure-1PSID** cookie.</br>
3.Then you can setup the key to your **local environment** by running the following command:</br>
```export _BARD_API_KEY=<__Secure-1PSID value>``` Remember the `_` before `BARD_API_KEY` is important. </br>
Or you can use `bardcoder_lib.py` to set the key to your **local environment** by running the following method `bard_coder.set_api_key(<__Secure-1PSID value>)` </br>
![showcase_api_key](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/showcase_api_key.png?raw=true "")</br>

4.Then you can run the application by running the following command:
```python bardcoder.py``` </br>
5.You can also run the code interpreter by running the following command:
```python code_interpreter.py``` </br>

## Installation Guide
Do not expose the `__Secure-1PSID value`. 
Note that while it is referred to as an `API KEY` for convenience, it is not an officially provided API KEY.

To install the dependencies, you can use pip to install from the **requirements.txt** file:
This will install streamlit, bard-coder-api, and any other dependencies listed in the `requirements.txt` file.

## Usage
There are 3 components of this application:
1. BardCoder: A coding assistant from Bard which automatically generates code from bard responses and refines it for coding purposes. This can be used by developers to get the correct code from Bard when they need help because the output is refined and fixed multiple times to provide the correct code.
- File: `bardcoder.py`

![bardcoder_main](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/bardcoder_main.png?raw=true "")</br>

2. AutoBard-Coder Interpreter: This is an interpreter for bardcoder which can be used to run the code generated from bardcoder. This can be very useful for all users who want to do data analysis and machine learning with bard. This can generate graphs and charts from bard responses and can be used to do data analysis.
- File: `bardcode_interpreter.py`

3. BardCoder Lib: This is a library for bardcoder which can be used to generate code from bard responses and refine it for coding purposes. You can use it to build your own application using bard.
- File: `bardcoder_lib.py`

## Using BardCoder:
To use BardCoder, you will need to run the following command:
```python bardcoder.py```
This will open the BardCoder UI in the terminal. And will be asked to enter prompts for bard.
![bard_coder](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/bardcoder_main.png?raw=true "")</br>
Not this assumes you have already set the `API KEY` in your local environment. If you have not, please refer to the setup process.
The code generated will be placed in folder `codes` and the response will be placed in folder `response`.

## Using Code Interpreter:
To use Code Interpreter, you will need to run the following command:
```python bardcode_interpreter.py```
This will open the Code Interpreter UI in the Web Browser. And will be asked to enter prompts for bard.
![code_interpreter](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/code_interpreter_main_ui.png?raw=true "")</br>

Now this assumes you have already set the `API KEY` in your local environment. If you have not, please refer to the setup process.
You can also setup the `API KEY` in the UI settings.
![code_interpreter_settings](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/code_interpreter_settings.png?raw=true "")</br>

Before prompting you should check the **Options** to change **Filenames** and **Filepaths** and other settings.

### Uploading data for data analysis:
You can set the `Upload Data` in **Options** to upload data for data analysis.
![upload_data_ui](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/upload_data_ui.png?raw=true "")</br>

After uploading the files you can ask for the prompts from bard. And you will get the output like this.
![upload_data_output](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/upload_data_output.png?raw=true "")</br>

You can also set the `Expected Output` in **Options** to get the **Accuracy** of the code generated.
![expected_output](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/code_interpreter_expected_output.png?raw=true "")</br>

And output will be generated like this with hilighting the **Accuracy** of the code generated.
![expected_output](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/code_interpreter_output.png?raw=true "")</br>

### Code Interpreter Demo:
[Code Interpreter Demo](https://github.com/haseeb-heaven/AutoBard-Coder/blob/master/resources/code_interpreter_demo.webm)</br>
[![code_interpreter_demo](https://img.youtube.com/vi/Flg1qUzs9ew/0.jpg)](https://youtube.com/shorts/Flg1qUzs9ew)

The code generated will be placed in folder `codes` and the response will be placed in folder `response` and upload files will be placed in folder `uploads`.

### Graphs and Visual Charts output:
To get Graphs and Charts output for your data visualization, you will install python packages `matplotlib`, `seaborn`, `cartopy`, `plotnine` and more. and run the following command: </br>
```python bardcode_interpreter.py``` </br>
And ask for the prompts from bard. And you will get the output like this:
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
This application uses the Bard API to interact with bard and refine the results for coding purposes. All data that is generated is stored in the following directories:
- `response`: This directory contains all the responses from bard.
- `codes`: This directory contains all the code generated from bard.
- `upload_data`: This directory contains all the data that is uploaded to bard.

## Features
Some of the features of AutoBard-Coder include:
- Automatic code generation from bard responses
- Refinement of code for coding purposes
- Ability to fix its own code
- Ability to debug its own code
- Ability to generate single or multiple responses from bard
- Ability to save responses and run them locally
- Ability to access local files for code interpretation
- Data analysis and machine learning capabilities
- Graphs and charts generation from bard responses
- Ability to upload files for data analysis and machine learning.

## License and Author
AutoBard-Coder was created by HeavenHM and is licensed under the MIT license.
