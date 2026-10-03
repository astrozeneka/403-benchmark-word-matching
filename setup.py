from setuptools import Extension, setup
from Cython.Build import cythonize

ext = Extension(
    "trie_matcher",
    sources=["src/trie.pyx"],
    include_dirs=["src"],
    language="c++",
    extra_compile_args=["-std=c++17"],
)

setup(
    name="trie_matcher",
    ext_modules=cythonize([ext], language_level=3),
)
