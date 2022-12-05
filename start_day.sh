#!/bin/bash

YEAR=2022

# find your token like this https://github.com/wimglenn/advent-of-code-wim/issues/1
# and save to file 'aoc_token.txt' - add it to .gitignore to not share
TOKEN=$(cat aoc_token.txt)

HELP=""

##############################
# Parse arguments
case $# in
    0)
        LC_ALL=en_US date "+Today is %A, %Y-%m-%d"
        echo ""
        DAY_NUMBER=$(date "+%d" | sed "s/^0//")
        ;;
    1)
        case $1 in
            [0-9]|[0-9][0-9])
                DAY_NUMBER=$1
                ;;
            -h|--help)
                echo "$HELP"
                ;;
            *)
                echo "Invalid argument, aborting"
                echo "Use integer day number as argument"
                exit 1
                ;;
        esac
        ;;
    *)
        echo "Too many arguments, aborting"
        echo "Use integer day number as argument"
        exit 1
        ;;
esac

##############################
# Set paths
echo "Day $DAY_NUMBER begins!"

DAY_PAD=$(printf '%02s' $DAY_NUMBER)

DAILY_URL="https://adventofcode.com/${YEAR}/day/${DAY_NUMBER}"
INPUT_URL="${DAILY_URL}/input"
INPUT_FILE="./inputs/${DAY_PAD}_input.txt"
EXAMPLE_FILE="./inputs/${DAY_PAD}_input_example.txt"
CODE_FILE="./${DAY_PAD}.py"


##############################
# Download puzzle input
echo "================================"
echo "Check the puzzle at ${DAILY_URL}"
echo "================================"

if [ -f "$INPUT_FILE" ]
then
    echo "Solution file $INPUT_FILE already exists."
else
    echo "Downloading input from ${INPUT_URL}"
    curl --cookie "session=${TOKEN}" "$INPUT_URL" --output "$INPUT_FILE"
    echo "================================"

    if grep -q -e "Please don't .* before it unlocks!" -e "404 Not Found" "$INPUT_FILE"
    then
        echo "Puzzle for day ${DAY_NUMBER} not accessible!"
        rm "$INPUT_FILE"
        exit 1
    fi

    touch "$EXAMPLE_FILE"
    echo "Please fill the example file ${EXAMPLE_FILE}"
    echo "Check the input file ${INPUT_FILE}"
fi


##############################
# Create python template for solution
if [ -f "$CODE_FILE" ]
then
    echo "Solution file $CODE_FILE already exists."
    exit
else
    echo "Creating solution file ${CODE_FILE}"
    sed "s|\$DAILY_URL|${DAILY_URL}|" template.py \
        | awk "/^DAY_NUMBER/{sub(\"None\", \"${DAY_NUMBER}\")} {print}" \
        > "$CODE_FILE"
fi
