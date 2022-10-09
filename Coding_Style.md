1. [General](#general)
    1. [Naming](#naming)
    2. [Spacing](#spacing)
    3. [Commenting](#commenting)
2. [Python](#python)
    1. [Order of imports](#order-of-imports)
    2. [Local Functions](#local-functions)
3. [Modules]

# General

- **Group** related logic together and separate with new lines:

    Instead of: ❌
    ```python
    total_strawberries = 0
    total_bananas = 0
    for strawberry in strawberries:
        total_strawberries += 1
    for banana in bananas:
        total_bananas += 1
    ```

    Do: ✅
    ```python
    total_strawberries = 0
    for strawberry in strawberries:
        total_strawberries += 1
    total_bananas = 0
    for banana in bananas:
        total_bananas += 1
    ```

## **Naming**

- For functions, use PascalCase.
- For classes, use PascalCase.
- For classes/function variables, use camelCase.
- For modules, use PascalCase.
- For constant variables, use UPPERCASE_SNAKE_CASE.
- All private variable/functions should start with a trailing `_` before the name.

Variables/functions names should be clear. Anyone reading the code later should know what the variable/function is for. Avoid generic names such as `p`, `var1`, `tmp`, `flag`, etc.

For clarity as well, avoid vague abbreviations and single-letter names, in both texts and variables/functions names:
- `k, v` -> `key, value`

As a rule of thumb, it is better for an object to have a longer name, than a vague confusing name.

## **Spacing**

- Variable assignment:
    `a = 5`
- Function parameters:
    `a(b, c, d)`
- Named parameters:
    `a(b=c, d=e)`
- Dictionary / objects:
    ```python
    a = {
        'b': c,
        'd': 'e'
    }
    ```

- One-line dictionary / objects / lists:
    ```python
    a = { 'b': c, 'd': 'e' }
    a = [ a, b, c ]
    ```
    *Note the spaces surrounding elements.*

## **Commenting**

- Python:
    ```python
    #region Name of Section
    
    SomeFunction()
    # A comment about ANother Function
    AnotherFunction()
    
    #endregion
    ```
    
Use `#TODO:` to mark undone, but still functional scripts.<br>
Use `#NOTE:` for longer comment explaining certain functionalities.

# Python

## Order of imports

1. Standard libraries
2. Installed libraries (installed by requirements.txt)
3. Project imports

Within each section, try to sort by length. Shortest naming import to longest naming imports.

## Local Functions

```python
def YourFunction():
    """
    Your pydoc comments
    """
#region Local_Function
def LocalFunction():
    return None

def AnotherLocalFunction():
    return None
#endregion

    x = "YourFunction operations"
    return x
```

Local Functions should be at the start of the function, after the pydoc comments, before the functions main operations. All local functions should be wrapped in `#region` comments, marking it as Local Functions.

Local Functions should not have any local functions within. (Have only 1 level of Local Function indent.)

Try to keep each local function short. If the function is long, consider implementing a private function in the same module instead.

# Modules

## Logging

*This module is under `Core.Logging`*

Try to log some sort of data when preforming `try-except`, to indicate the reasoning why an exception might occur.<br>For logging severities, this is the guideline.

**Log Severity**
- DEBUG : Use it for testing or debugging.
- LOG : Use it to keep track of certain actions being performed.
- WARNING : Report unusual actions that occur. Those actions provides no negative impact to any future actions.
- ERROR : Report unusual actions that occur. Those actions might result in unwanted outputs by the user, but does not interfere with the user using the application.
- SEVERE : Report unusual actions that occur. Those actions will interfere with the user using the application.

All Log files will be saved under a `LogDump` folder that is automatically created in the same project directory.