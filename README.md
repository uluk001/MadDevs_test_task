# HTML Message Splitter

## Description

This project is a Python library designed to split HTML messages into fragments of a specified maximum length. The splitting is done in a way that preserves the HTML structure and, as much as possible, the integrity of words. The library utilizes "HTMLParser" for parsing and manipulating HTML content.

Clone the repository

```bash
git clone https://github.com/uluk001/MadDevs_test_task.git
cd MadDevs_test_task
```

To use this library, you need Python version 3.6 or higher.

Set up a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

You can install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```


## Usage

To use this HTML Message Splitter, you can follow these steps:

1. **Import the Function**: 

    First, you need to import the `split_html` function from the script.

    ```python
    from script import split_html
    ```

2. **Prepare Your HTML Content and Maximum Length**: 

    Define the HTML content that you want to split and the maximum length of each fragment.

    ```python
    html_content = "<p>This is a <b>sample</b> HTML message</p>"
    max_length = 20
    ```

3. **Split the HTML Content**: 

    Call the `split_html` function with the HTML content and the maximum length as arguments.

    ```python
    fragments = split_html(html_content, max_length)
    ```

4. **Handle the Result**: 

    The `split_html` function will return a list of fragments. You can then handle or display these fragments as needed.

    ```python
    print(fragments)  # Output: ['<p>This is a <b>sa', 'mple</b> HTML mes', 'sage</p>']
    ```

5. **Error Handling**: 

    If the HTML content contains a word or a tag longer than the maximum length, a `ValueError` will be raised.

    ```python
    try:
        fragments = split_html(html_content, max_length)
    except ValueError as e:
        print(f"Error: {e}")
    ```

This function ensures that HTML tags are not broken and words are not split across fragments unless they are longer than the maximum length.



## Author

[GitHub](https://github.com/uluk001)  
[LinkedIn](https://www.linkedin.com/in/ismailov-uluk-92784a233/)