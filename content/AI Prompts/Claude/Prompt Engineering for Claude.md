---
title: _. Prompt Engineering for Claude
tags:
  - ai
  - claude
  - prompt
  - bookmark
---
> [!note]
> [Claude 2.1](https://www.anthropic.com/index/claude-2-1-prompting) Add `“Here is the most relevant sentence in the context:”` At the end when finding the information from the context.![[Pasted image 20231213150601.png]]
# Summary 
- Prompt Composition Sample ![[Pasted image 20231204193856.png]]![[Pasted image 20231204193916.png]]![[Pasted image 20231204194109.png]]
- [Legal Services](https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8/edit#gid=898779877)
- [Financial Services](https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8/edit#gid=1348878889)
- [Coding](https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8/edit#gid=1171654224)
- [Cookbook](https://github.com/anthropics/anthropic-cookbook)

---
[googlesheet link](https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8/edit#gid=150872633)
# Basic
## Basic Prompt Structure
- Every prompt sent through the API / console *must start with two newlines* followed by *"Human:"*, and later contain two newlines followed by *"Assistant:"*.![[Pasted image 20231204190625.png]]
- *With Claude 2.1*, you can also now use a system prompt to give Claude instructions and guidelines. A system prompt simply refers to text that is above the "Human:" turn rather than after or below it. You should stil use two new lines after the system prompt, before "Human:".![[Pasted image 20231204190739.png]]

## Other Tips
- Be Clear & Direct
- Role Prompting
- Tags and Delimeters
	- XML tags (<> to open, </> to close) are a common and highly effective way to organize information within a prompt. Sometimes it also helps to ask Claude to think about its answer first before responding.

# Intermediate
## Use Prompt Template
![[Pasted image 20231204191716.png]]![[Pasted image 20231204191849.png]]
## JSON Output
![[Pasted image 20231204192228.png]]
## Allow Claude to think and perform 
![[Pasted image 20231204192756.png]]![[Pasted image 20231204192901.png]]
## Order Matters
- *Claude is sometimes sensitive to the order of arguments.* Claude is more likely to choose the second of two options.
	- negative first and positive second: overall assessment may be positive
	- positive first and negative second 
## few-shot prompting 
![[Pasted image 20231204193109.png]]![[Pasted image 20231204193244.png]]

# Advanced
## Minimize Hallucination 
- by giving Claude an option that it is OK for it to decline to answer, or to only answer if it actually knows the answer with certainty ![[Pasted image 20231204193415.png]]
- it is best practice to have the question at the bottom after any text or doc
- make Claude gather evidence first ![[Pasted image 20231204193612.png]]
## Double Check using AI
- Provide Claude chat history to prove, verify, improve, double check and etc.
![[Pasted image 20231204195127.png]]
## Multiple Calls 
![[Pasted image 20231204195113.png]]

## Function Calling 
- In previous substitution exercises, we substituted text into prompts. In function calling, we substitute function results into prompts. Claude can't literally call or access functions. Instead, we have Claude output the function name and arguments, halt while the function is called, then we reprompt with the function results.