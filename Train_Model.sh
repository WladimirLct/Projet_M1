# Check if an argument is provided
if [ $# -gt 0 ]; then
    # If an argument is provided, pass it to the Python script
    python Split_generator.py $1
else
    # If no argument is provided, run the Python script without any arguments
    python Split_generator.py
fi

python Model.py