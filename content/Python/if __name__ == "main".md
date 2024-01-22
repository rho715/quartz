---
title: _. if __name__ == "main"
tags:
  - python
---
<iframe src="https://www.youtube.com/embed/3dHyS1W4TIE" Width="560" Height="315" > </iframe>

# why use `if __name__ == "main"` in Python?

## Example 1
---

### `mymath.py`
```python
def add(a, b):
	return a + b

print(add(100, 60))
```

### `test.py`
```python
import mymath

print(mymath.add(90, 4))
```

### result: `python3 test.py`
> `160`        
> `94`

> [!note]
> when you run `test.py` you also see the returned result from `mymath.py`.
> This is because when you import `mymath.py`, it runs the full script.

## Example 2
---
### `mymath.py`
```run-python

def add(a, b):
	return a + b

print(__name__)
```

### `test.py`
```run-python
import mymath

print(mymath.add(90, 4))

```

### result: `python3 mymath.py`
> `__main__`
### result: `python3 test.py`
> `mymath`      
> `94`

> [!note]
> when you run a file, `__name__` becomes `__main__`. but if you import the file, `__name__` becomes the file name.

# Summary
---

> [!summary]
> - Use `if __name__ == "__main__":` to distinguish between script execution and module imports.
> - It promotes code organization and prevents unintended behavior.
> - Apply this construct to create well-structured and reusable Python code.

