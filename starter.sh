#!/bin/bash

YEAR=2022

# find your token like this https://github.com/wimglenn/advent-of-code-wim/issues/1
# and save to file 'aoc_token.txt' - add it to .gitignore to not share
TOKEN=$(cat aoc_token.txt)


##############################
# Read day number, set paths
DAY_NUMBER=$1

# check if there are any parameters
if [ $# -eq 0 ]
then
    echo "No arguments supplied, aborting"
    echo "Use day number as parameter"
    exit
elif [ -z "${DAY_NUMBER##*[!0-9]*}" ]  # https://stackoverflow.com/a/2704760/9003767
then
    echo "Non-integer supplied, aborting"
    echo "Use day number as parameter"
    exit
else
    echo "Day $DAY_NUMBER begins!"
fi

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
