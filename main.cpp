#include <iostream>
#include <string>
#include <fstream>
#include <sstream>


using namespace std;

struct Node {

};

Node *buildTree(string s) {
    Node *root = new Node();



    return root;
}

int _compute_word_score(string word, Node *root) {
    return 0;
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
    return 0;
}
