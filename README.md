# testgen

The Test Template Generator is a Python script that automates the creation of a template file containing unit test cases for functions in a given source file. It saves you time by generating the initial structure of test cases, allowing you to focus on writing test assertions and verifying the correctness of your code.

## Features

- Automatically generates a template file with unit test cases for functions in a source file.
- For now, it supports only pytest test frameworks
- Provides customizable options to specify the output file name, and other settings.
- Allows you to easily add or modify test cases based on your requirements.

## Getting Started

### Prerequisites

To run the Test Template Generator, you need to have Python installed on your system. Ensure you have a compatible version of Python installed.

### Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/vmnit/testgen.git
```

2. Navigate to the project directory:
```bash
cd testgen
```

### Usage
To generate a test template file, follow these steps:
1. Prepare your source file containing functions that need unit test cases.
2. Run the script with the following command:

```bash
python testgen.py -s <source_file.py> -o <test_source_file.py>
```

Replace source_file.py with the actual path and name of your source file.
1. The script will generate a test template file named test_source_file.py in the same directory as the source file.
2. Open the test template file in your preferred text editor and customize the generated test cases according to your needs.
3. Run the modified test template file using your chosen test framework to execute the test cases against your source code.

For more details and customization options, refer to the script's documentation.

## Contributing
Contributions to the Test Template Generator are welcome! If you encounter any issues or have suggestions for improvements, please submit them in the [issue tracker](https://github.com/vmnit/testgen/issues).
Before making a contribution, kindly review the [contribution guidelines](CONTRIBUTING.md) for instructions on how to get started.

## License
This project is licensed under the [MIT License](License). Feel free to use, modify, and distribute the code within the terms of the license.
