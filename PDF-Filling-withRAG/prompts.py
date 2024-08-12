from langchain.prompts import PromptTemplate

# there are two type of document filling one in which the lines are blanked and need to be filled and other in which just question and no dashed line blow
# both handled seperately


template1 = """
Fill in the blanks of the following form based on the provided context.

**Context:**
{context}

**Form:**
{input}

* make sure the format of the form kept unchanged like headings, numberings
* Form should be complete in length in the output as provided
"""
# template = """
# You are required to fill in the blanks in the form below by only using the provided context.

# **Context:**
# {context}

# **Form:**
# {input}

# ***** if no fields(____) found in the **Form** output will be the provided **Form** only ****

# Instructions:
# 1. Complete **all** sections of the form based on the context provided.
# 2. Maintain the original structure, headings, and numbering exactly as they are presented in the form.
# """
promptforfilling = PromptTemplate.from_template(template1)

template2 = """
Fill in the blanks of the following form based on the provided context.

**Context:**
{context}

**Form:**
{input}

***** if no fields(____) found in the **Form** output will be the provided **Form** only ****
"""
promptwithoutfilling = PromptTemplate.from_template(template2)


def select_prompt(input):
  if '____' in input:
    return promptforfilling
  else:
    return promptwithoutfilling