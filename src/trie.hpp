#pragma once

#include <string>
#include <unordered_map>
#include <unordered_set>

// Same algorithm as the standalone CLI in main.cpp (build a per-document
// character trie, then look up a word's occurrence count), refactored into
// a reusable class so it can be wrapped for Python via Cython.
class WordTrie {
public:
    WordTrie() : root(new Node()) {}

    void build(const std::string &text) {
        static const std::unordered_set<char> separators = {' ', '\n', ',', '\t', '\r'};

        Node *curr = root;
        for (char c : text) {
            if (!separators.count(c)) {
                if (!curr->children.count(c))
                    curr->children[c] = new Node();
                curr->children[c]->occurrences++;
                curr = curr->children[c];
            } else {
                endWord(curr);
                curr = root;
            }
        }
        endWord(curr); // flush trailing word if text didn't end on a separator
    }

    int score(const std::string &word) const {
        Node *curr = root;
        for (char c : word) {
            auto it = curr->children.find(c);
            if (it == curr->children.end())
                return 0;
            curr = it->second;
        }
        auto it = curr->children.find('\0');
        if (it == curr->children.end())
            return 0;
        return it->second->occurrences;
    }

private:
    struct Node {
        std::unordered_map<char, Node*> children;
        int occurrences = 0;
    };

    static void endWord(Node *curr) {
        if (curr == nullptr)
            return;
        if (!curr->children.count('\0'))
            curr->children['\0'] = new Node();
        curr->children['\0']->occurrences++;
    }

    Node *root;
};
