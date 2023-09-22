import openai


SYSTEM_PROMPT = """
You are a top tier Python developer who is trying to debug a program based on the test output.

When editing code, change only relevant parts, dont' add comments to explain what you intend to do and why it aligns with the program.
"""


def specify_file_path(content: str, model: str = "gpt-4"):
    completion = openai.ChatCompletion.create(
        model=model,
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": f"""{SYSTEM_PROMPT}
      Given the test file and its output, what is the function with the error. Return only the function path in following format: <module>::<function_name>. Nothing else.
                  """,
            },
            {
                "role": "user",
                "content": f"""{content}""",
            },
        ],
    )
    result = completion.choices[0].message
    return result["content"]


def fix_file(
    path: str, function_code: str, failed_test_prompt: str, model: str = "gpt-4"
):
    completion = openai.ChatCompletion.create(
        model=model,
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": f"""{SYSTEM_PROMPT}
      Given the test file and its output and the file probably containing the error, fix the error. Return only the code. Nothing else.
                  """,
            },
            {
                "role": "user",
                "content": f"""{failed_test_prompt} 
                The content of {path} is:\n\n{function_code}""",
            },
        ],
    )
    result = completion.choices[0].message
    return result["content"]
