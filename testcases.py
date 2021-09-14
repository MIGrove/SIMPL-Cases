#!/usr/bin/env python

from os import error
import subprocess
import sys

# bcolors class obtained from https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal in answer by "joeld"
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def make(name, wd, success_output):
    make_result = subprocess.run("make " + name, stdout=subprocess.PIPE, text=True, cwd=wd, shell=True)
    if make_result.stdout == success_output:
        print("\n" + bcolors.OKCYAN + "[INFO]" + bcolors.ENDC + "\tcompiled successfully:\t" + name)
        return True
    else:
        sys.exit(bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "\tcompiled with warnings/errors:\t" + name)
        return False


def test(name, input_file, output_file_path, error_file_path):
    test_result = subprocess.run("./" + name + " ../tests/" + input_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd="../bin/", shell=True, errors="ignore")

    if test_result.stderr != "":
        with open(error_file_path) as error_file:
            error_file_contents = error_file.read()
            if test_result.stderr != error_file_contents:
                print(bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "\nexpected:\n\t" + "\t".join(error_file_contents.splitlines(keepends=True)) + "\n\nbut received:\n\t" + "\t".join(test_result.stderr.splitlines(keepends=True)))
                return False
            else:
                print(bcolors.OKGREEN + "[PASS]" + bcolors.ENDC + "\t" + input_file)
                return True
    
    with open(output_file_path) as output_file:
        output_file_contents = output_file.read()
        if test_result.stdout != output_file_contents:
            print(bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "\nexpected:\n\t" + "\t".join(output_file_contents.splitlines(keepends=True)) + "\n\nbut received:\n\t" + "\t".join(test_result.stdout.splitlines(keepends=True)))
            return False
        else:
            print(bcolors.OKGREEN + "[PASS]" + bcolors.ENDC + "\t" + input_file)
            return True


def split_parser():
    with open("02_parser/error.output.txt") as error_output_file:
        lines = error_output_file.readlines()
        file_names = []

        for i in range(201, 245):
            with open("02_parser/error" + str(i) + ".output.txt", "w") as new_file:
                new_file.write(lines[i - 201])
                file_names.append(new_file.name)
        
        return file_names


def test_scanner():
    pass_count, fail_count = [0] * 2

    make("testscanner", "../src/", "clang -ggdb -O0 -Wall -Wextra -Wno-variadic-macros -Wno-overlength-strings -pedantic  -o ../bin/testscanner testscanner.c error.o scanner.o token.o\n")
    print("\n" + ("*" * 10) + " testing: scanner " + ("*" * 10))

    for i in range(101, 121):
        if test("testscanner", "01_scanner/test" + str(i) + ".simpl", "01_scanner/test" + str(i) + ".simpl.out.txt", "01_scanner/test" + str(i) + ".simpl.err.txt"):
            pass_count += 1
        else:
            fail_count += 1
    
    return pass_count, fail_count


def test_parser():
    pass_count, fail_count = [0] * 2

    make("testparser", "../src/", "clang -ggdb -O0 -Wall -Wextra -Wno-variadic-macros -Wno-overlength-strings -pedantic  -o ../bin/simplc simplc.c error.o scanner.o token.o\n")
    print("\n" + ("*" * 10) + " testing: parser " + ("*" * 10))
    file_names = split_parser()

    i = 201
    for file_name in file_names:
        if test("simplc", "02_parser/error" + str(i) + ".simpl", None, file_name):
            pass_count += 1
        else:
            fail_count += 1
        i += 1

    return pass_count, fail_count


def print_stats(pass_count, fail_count):
    if pass_count + fail_count == 0:
        sys.exit(bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "\tcannot print stats when there are no stats!")

    print("\n\tpassed: " + str(pass_count) + "\n\tfailed: " + str(fail_count) + "\n\tpass-rate: {rate:.2f}".format(rate=pass_count/(fail_count + pass_count)))


def main():
    if len(sys.argv) == 2:
        mode = sys.argv[1]
    else:
        sys.exit(bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "\ttest.py requires one argument (either \"scanner\", \"parser\", \"all\", or \"compile\")")

    match mode:
        case "scanner":
            pass_count, fail_count = test_scanner()
            print_stats(pass_count, fail_count)
        case "parser":
            pass_count, fail_count = test_parser()
            print_stats(pass_count, fail_count)
        case "all":
            pass_count_scanner, fail_count_scanner = test_scanner()
            pass_count_parser, fail_count_parser = test_parser()
            print_stats(pass_count_scanner + pass_count_parser, fail_count_scanner + fail_count_parser)
        case "compile":
            make("testscanner", "../src/", "clang -ggdb -O0 -Wall -Wextra -Wno-variadic-macros -Wno-overlength-strings -pedantic  -o ../bin/testscanner testscanner.c error.o scanner.o token.o\n")
            make("testparser", "../src/", "clang -ggdb -O0 -Wall -Wextra -Wno-variadic-macros -Wno-overlength-strings -pedantic  -o ../bin/simplc simplc.c error.o scanner.o token.o\n")
        case _:
            sys.exit(bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "\ttest.py currently only supports the following as an argument:\n\tscanner\n\tparser\n\tall\n\tcompile")


if __name__ == "__main__":
    main()
