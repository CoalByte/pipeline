# pipeline
A simple lightweight and expandable pipeline framwork for Python.

# CURRENTLY NOT MAINTAINED
The readme might be a bit outdated, make sure to open a request If you'd like to change anything.

### Basic Usage:

Not using the pipeline wrapper:
```py
from pipeline import * # Import the classes from the pipeline.py file


if __name__ == "__main__": 
    pipe = Pipeline() # Create the pipeline object

    def caps_rule(input): # Define a pipeline rule 
        if input.isupper() is True:
            return True

    def on_event(line): # Define the function to be executed after something has been added to the production line
        print(line.data[0])
     
    line = ProductionLine(name="cap", filter=[caps_rule], on_section=on_event) # Create the ProductionLine object
     
    pipe.add_line(line) # Append the production to the pipe

    o = pipe.process_data(data="HELLO",
                         single_sec=True) # Process some example data and return after a single section
                         
    print(o.name) # Print the resulting production's name
```

You may also use the pipeline.wrapper even though It won't allow you to add any on_section function.

```py
pipe.wrapper(line_name="cap", func=caps_rule)
```
