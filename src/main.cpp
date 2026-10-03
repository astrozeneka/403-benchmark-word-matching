#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <unordered_set>

using namespace std;

struct Node {
    unordered_map<char, Node*> children;
    int occurences = 0;
};

Node *buildTree(string text) {
    Node *root = new Node();
    unordered_set<char> separators = {' ', '\n', ','};

    // Iterate over text
    Node *curr = root;
    for (char c: text) {
        if (!separators.count(c)) {
            if (!curr->children.count(c)) // the children nodes doesn't exist yet
                curr->children[c] = new Node();
            curr->children[c]->occurences++;
            curr = curr->children[c];
        } else { // end of a word
            if (!curr->children.count('\0'))
                curr->children['\0'] = new Node();
            curr->children['\0']->occurences++;
            curr = root;
        }
    }

    return root;
}

int _compute_word_score(string word, Node *root) {
    Node *curr = root;
    for (char c: word) {
        if (!curr->children.count(c))
            return 0;
        curr = curr->children[c];
    }
    if (!curr->children.count('\0'))
        return 0;
    return curr->children['\0']->occurences;
}

int main(int argc, char const *argv[]) {
    string in;
    for (int i = 1; i < argc; i++)
        if (string(argv[i]) == "--in" && i+1 < argc)
            in = argv[++i];
    cout << in << endl;

    stringstream buffer;
    buffer << ifstream(in).rdbuf();
    string content = buffer.str();

    cout << content << endl;
    Node *root = buildTree(content);
    _compute_word_score("the", root);

    return 0;
}
