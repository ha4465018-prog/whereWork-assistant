from main import generate_answer
import traceback
try:
    print(generate_answer("hello"))
except Exception as e:
    traceback.print_exc()
