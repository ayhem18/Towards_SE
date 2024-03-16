double calculate(double operand1, double operand2, char operation){
    if (operation == '+')
        return operand1 + operand2;
    else if (operation == '-')
        return operand1 - operand2;
    else if (operation == '*') 
        return operand1 * operand2;
    else
        return operand1 / operand2;
}
