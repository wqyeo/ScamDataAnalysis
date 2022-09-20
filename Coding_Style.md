1. [General](#general)
    1. [Naming](#naming)
    2. [Spacing](#spacing)
    3. [Commenting](#commenting)
2. [Python](#python)
    1. [Order of imports](#order-of-imports)

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

For clarity as well, avoid vague abbreviations, single-letter names, and acronyms, in both texts and variables/functions names:
- `stats` -> `statistics`
- `config` -> `configurations`
- `k, v` -> `key, value`

It is better for an object to have a longer name, than a vague confusing name.

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
    
    some_code()
    # A comment
    some_code()
    
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