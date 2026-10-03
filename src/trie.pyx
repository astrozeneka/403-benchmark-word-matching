# distutils: language = c++
from libcpp.string cimport string


cdef extern from "trie.hpp":
    cdef cppclass WordTrie:
        WordTrie()
        void build(string text)
        int score(string word)


cdef class PyWordTrie:
    cdef WordTrie *thisptr

    def __cinit__(self):
        self.thisptr = new WordTrie()

    def __dealloc__(self):
        del self.thisptr

    def build(self, str text):
        self.thisptr.build(text.encode("utf-8"))

    def score(self, str word):
        return self.thisptr.score(word.encode("utf-8"))
