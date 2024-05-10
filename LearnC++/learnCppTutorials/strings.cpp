# include <iostream>
# include <string>

// std::getline input for text data
// std::cin >> std::ws manipulates the input stream to discard any leading white spaces
// 'std::cin >> std::ws' will not accept empty input...
// keep in mind that std::string.length will return an unsigned integer

std::string getStringInput(const std::string& input_prompt) {
    std::cout << input_prompt <<'\n';
    std::string input_text {};
    std::getline(std::cin >> std::ws, input_text);
    return input_text;
}

