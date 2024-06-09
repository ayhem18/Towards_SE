/**
 * This file implements a complete-like binary Tree based on the dynamic array data structure
 */

#ifndef LEARNC___BINARYTREE_H
#define LEARNC___BINARYTREE_H

# include <cmath>
# include <vector>
# include <string>

# include "../linear/ArrayList.h"
# include "tree.h"

template <typename T>
class BinaryTree: public BTree<T> {
private:
    ArrayList<T> array;
public:
    explicit BinaryTree(T val): BTree<T>(1) {
        // initial the inner array list with the passed value
        array = ArrayList<T>(val);
    };

    BinaryTree(): BTree<T>(0){
        // initialize the array list
        array = ArrayList<T>();
    }

    void add(const T& element) override{
        array.add(element);
        this -> m_size = array.size();
    };
    void remove(const T& element) override{
        array.remove(element);
        this -> m_size = array.size();
    }
    int depth() const override{
        return static_cast<int>(log2(this -> m_size)) + 1;
    }

    // let's implement the << operator to display the tree
    friend std::ostream& operator << (std::ostream& out, const BinaryTree& tree) {
         // extract the depth of the tree
         int treeDepth = tree.depth();
         int C = 3;
         std::vector<std::string> level_strings {};
         std::string padding;
         std::string separator  {" ", 1};

         for (int d=treeDepth; d > 0; d--) {
             // start with the padding to the left
             std::string level_string  {padding};
            int first_element_at_depth = static_cast<int>(pow(2, d - 1) - 1);
            int last_element_at_depth = std::min<int>(pow(2, d) - 1, tree.size());

            // add each element on the current level seperated by the 'separator'
            for (int i = first_element_at_depth; i < last_element_at_depth; i ++){
                level_string += (std::to_string(tree.array.get(i)) + separator);
            }

            int separatorLength = separator.size();
            padding = {" ", static_cast<std::size_t>((separatorLength + C) / 2)};
            separator = {" ", static_cast<std::size_t>(2 * separatorLength + C)};
            // make sure to append the list
            level_strings.push_back(level_string);
         }

         // at this point, we are ready to display the tree: it should be displayed in reverse though
        for (int i = level_strings.size() - 1; i >= 0; i--) {
            out << level_strings[i] << "\n";
        }
        return out;
    }


};

#endif //LEARNC___BINARYTREE_H
