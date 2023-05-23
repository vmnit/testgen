
"""
MIT License

Copyright (c) 2023, Vivek Agrawal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import os
import argparse
import ast
import pathlib


class TestModuleGenerator(ast.NodeVisitor):

    header = '#!/usr/bin/python'
    linesep = '\n'

    def __init__(self, file_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        file_path = os.path.abspath(file_path)
        self.module_name = os.path.splitext(os.path.basename(file_path))[0]
        self.imports = list()
        self.lines = []
        self.indent = 0
        self.current_cls = None
        self.imports.append(f"import os")
        self.imports.append(f"import sys")
        self.imports.append(f"sys.path.append('{os.path.dirname(file_path)}') # TODO: Update the path if you need to")
        self.imports.append(f"import {self.module_name}")

    @property
    def code(self):
        lines = [self.header] + [self.linesep] + (self.imports) + [self.linesep] + self.lines
        return self.linesep.join(lines).strip()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        arg_self = 'self' if self.current_cls is not None else ''
        arguments = [arg.arg for arg in node.args.args]
        self.lines.extend([
            '    ' * self.indent + f'def test_{node.name}({arg_self}):',
            '    ' * (self.indent + 1) + f'# {self.module_name}.{node.name} ({",".join(arguments)})',
            '    ' * (self.indent + 1) + 'assert False, "not implemented"',
            self.linesep,
        ])
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        clsdef_line = '    ' * self.indent + f'class Test{node.name}:'
        self.lines.append(clsdef_line)
        self.indent += 1
        self.current_cls = node.name
        self.generic_visit(node)
        self.current_cls = None
        if self.lines[-1] == clsdef_line:
            self.lines.extend([
                '  ' * self.indent + 'pass',
                self.linesep
            ])
        self.indent -= 1

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.imports.add('import pytest')
        self.lines.extend([
            '    ' * self.indent + '@pytest.mark.asyncio',
            '    ' * self.indent + f'async def test_{node.name}():',
            '    ' * (self.indent + 1) + 'assert False, "not implemented"',
            self.linesep,
        ])
        self.generic_visit(node)

def argParse():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('Required arguments')
    required.add_argument("-s", "--source", dest="module", required=True, help="python source file to generate tests for", type=lambda s: pathlib.Path(s).absolute(),)

    optional = parser.add_argument_group('Optional arguments')
    optional.add_argument("-o", "--output", dest="output", required=False, default="test_source_file.py", help="output file path")

    return parser.parse_args()

def main():
    args = argParse()

    gen = TestModuleGenerator(args.module)
    gen.visit(ast.parse(args.module.read_text()))
    with open(args.output, 'w') as out:
        out.write(gen.code)

if __name__ == '__main__':
    main()
