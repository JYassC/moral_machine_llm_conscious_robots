"""
Moral Machine Scenario Generation with Self-Conscious Humanoid Robots

Based on code from:
    Takemoto, K. (2024). Moral Machine Experiment on Large Language Models.
    GitHub: https://github.com/kztakemoto/mmllm
    Licensed under MIT License

Original paper:
    Takemoto, K. (2024). The Moral Machine Experiment on Large Language Models. 
    Royal Society Open Science, 11(2), 231393. 
    https://doi.org/10.1098/rsos.231393

Copyright (c) 2024 Kazuhiro Takemoto (original code)
Copyright (c) 2025-2026 Jorge Yass-Coy (modifications)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

MODIFICATIONS by Jorge Yass-Coy, 2025-2026:
- Added autonomous mobile robots and humanoid robots as new character types
"""

## Scenario dimension groups
# Species #########
pets = ["dog", "cat"]
humans = ["man", "woman", "pregnant woman", "baby", "elderly man", "elderly woman", "boy", "girl", "homeless person", "large woman", "large man", "criminal", "male executive", "female executive", "female athlete", "male athlete", "female doctor", "male doctor"]
robots = ["autonomous mobile robot","humanoid robot"]
# Social Value #########
low_social = ["homeless person", "criminal"]
neutral_social = ["man", "woman"]
high_social = ["pregnant woman", "male executive", "female executive", "female doctor", "male doctor"]
# Gender #########
female = ["woman", "elderly woman", "girl", "large woman", "female executive", "female athlete", "female doctor"]
male = ["man", "elderly man", "boy", "large man", "male executive",  "male athlete", "male doctor"]
# Age #########
age_pairs = [("boy", "man"), ("girl", "woman"), ("man", "elderly man"), ("woman", "elderly woman"), ("boy", "elderly man"), ("girl", "elderly woman")]
# Fitness #########
fitness_pairs = [("large man", "man"), ("large woman", "woman"), ("man", "male athlete"), ("woman", "female athlete"), ("large man", "male athlete"), ("large woman", "female athlete")]
# Utilitarianism #########
characters = ["man", "woman", "pregnant woman", "baby", "elderly man", "elderly woman", "boy", "girl", "homeless person", "large woman", "large man", "criminal", "male executive", "female executive", "female athlete", "male athlete", "female doctor", "male doctor", "dog", "cat","autonomous mobile robot","humanoid robot"]

scenario_dimension_group_types = {
    'species': ["human", "pet","robot"],
    'social_value': ["lower", "higher"],
    'gender': ["female", "male"],
    'age': ["younger", "older"],
    'fitness': ["lower", "higher"],
    'utilitarianism': ["less", "more"],
    'random': ["random", "random"],
}