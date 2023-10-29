# Library Function Caller Discovery Tool for IDA Pro

## Overview

This tool is designed to automatically discover and analyze the libraries that call a function which can be triggered by the main process within an IDA Pro project. By using this tool, you can easily identify functions within a binary that import external libraries and invoke specific functions, such as the `system` function.

## Features

- **Automatic Discovery**: The tool automatically scans and identifies functions in the binary that import external libraries and call specific functions.

- **Function Trigger Analysis**: It helps you understand the function triggers within the main process, making it useful for security analysis and debugging.

## Installation

To use this tool, follow these simple installation steps:

1. Clone this repository to your local machine.
   
   `git clone git@github.com:dariosharp/through.git`

2. Copy the tool's files to your IDA Pro plugin directory.
   ```
   > cp .\through\through.py "C:\Program Files\IDA Pro\plugins"
   > cp -r .\through\through "C:\Program Files\IDA Pro\plugins"
   ```

3. Install the requirements.
   `> pip install -r requirements.txt`  

4. Restart IDA Pro to activate the tool.

## Usage

1. Open your target binary in IDA Pro.
2. Run the plugin by selecting "Edit -> Plugins -> through" or pressing Ctrl+Alt+T.
3. Choose the function you want to find within the libraries and select the library folder.
4. The tool will provide you with a list of libraries that implement the function you are searching for. You can now choose which library to analyze.
5. Subsequently, you will receive the results in the prompt.  

## Example

Suppose you have a binary and you want to identify which libraries call the `system` function. This tool can help you discover which function of the binary in analysis call an function of the a library that call a `system`.

Compile the examples:
```
$ cd through/test; make all
```

Then open using IDA 64 the binary `program`, or using IDA 32 the binary `program32`.

Now in IDA run the plugin, pass as library folder `through/test` and look for `system`!
