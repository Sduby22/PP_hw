from src.RunPy import runpy

@runpy.register("foo")
def foo():
    print('foo')

print(1)
