import os

a = os.path.dirname(__file__)
b = os.path.abspath(__file__)
print(os.path.splitext(os.path.basename(b))[0])