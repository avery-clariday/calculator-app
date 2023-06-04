from tkinter import Tk, Frame, Label, Button


class CalculatorApp:
    # Root window
    __root = None
    # max number of columns a row can have in the calculator
    __max_column_size = 5

    # calculator buttons, in the order they are displayed on the calculator
    __buttons = {
        '7':    {},    '8': {},     '9': {},    '/': {},    '(':      {},
        '4':    {},    '5': {},     '6': {},    'x': {},    ')':      {},
        '1':    {},    '2': {},     '3': {},    '-': {},    'clear':  {},
        '+/-':  {},    '0': {},     '.': {},    '+': {},    '=':      {}
    }
    # Section for the actual calculator buttons
    __calculator_section = None
    # Arithmetic expression to be evaluated
    __expression_label = None
    # Keeps track of whether or not the current expression has been evaluated
    __expression_evaluated = False
    # Holds the last number entered into the expression. If the calculate button is hit and the
    # last character in the expression is an arithmetic operator, the calculator will assume the
    # last number entered is to be tacked onto the end of the expression to complete it.
    __last_number_entered = 0


    def __initialize_root(self) -> None:
        # Screen root
        self.__root = Tk()
        # Set application title
        self.__root.title("Calculator App")
        # Set the background color
        self.__root.configure(background='#3c4266')
        # prevent screen resizing
        self.__root.resizable(False, False)


    def __set_add_character_command(self, button_name: str) -> lambda: function:
        return lambda: self.__add_character(button_name)


    def __initialize_buttons(self) -> None:
        # Counts the number of buttons in the calculator
        button_count = 0
        # A button's row position on the grid
        row = 2
        # A button's column position on the grid
        column = 0
        # filler buttons that are disabled
        filler = ['', ' ', '  ']

        # Initialize each button
        # Get the button's row, column, and state
        # Then create the button itself and anchor the button on the grid
        # Filler buttons are buttons with no text and have a state of disabled
        for button_name in self.__buttons:
            # Set row and column positions, create button key in the nested dictionary
            self.__buttons[button_name]['button'] = None
            self.__buttons[button_name]['row'] = row
            self.__buttons[button_name]['column'] = column


            # Set button state
            if button_name not in filler:
                self.__buttons[button_name]['state'] = 'normal'
            else:
                self.__buttons[button_name]['state'] = 'disabled'


            # Increment number of buttons, get the column the button belongs to
            button_count += 1
            column = button_count % self.__max_column_size


            # Increment row when the column resets to 0
            if column % self.__max_column_size == 0 and button_count != 0:
                row += 1


            # Set lambda commands for buttons
            command = None
            if button_name == '=':
                command = lambda: self.__calculate()
            elif button_name == 'clear':
                command = lambda: self.__clear()
            elif button_name == '+/-':
                command = lambda: self.__flip_sign()
            else:
                # This must be done in a separate helper function otherwise all the buttons
                # set to this command will use the last button name in the for loop instead of the
                # current one in the loop
                command = self.__set_add_character_command(button_name)


            # Set button
            self.__buttons[button_name]['button'] = Button(self.__calculator_section,
                                                    text=button_name, height=3, width=10,
                                                    state=self.__buttons[button_name]['state'],
                                                    foreground='white', background='black',
                                                    command=command)


            # Place button on the grid
            self.__buttons[button_name]['button'].grid(row=self.__buttons[button_name]['row'],
                                                       column=self.__buttons[button_name]['column'])


    def __init__(self) -> None:
        # Initialize GUI
        self.__initialize_root()
        # self.__initialize_sections()
        # The frame that contains the calculator buttons and labels
        self.__calculator_section = Frame(self.__root, border=2)
        self.__calculator_section.grid(row=1, column=0)
        # The label that displays the expression
        self.__expression_label = Label(self.__calculator_section, height=3)
        self.__expression_label.grid(row = 0, column = 0, columnspan=5, sticky='ew')
        self.__expression_label.configure(foreground='black', background='grey')
        # Initialize Calculator Buttons
        self.__initialize_buttons()


        # Run loop GUI loop
        self.__root.mainloop()


    def __flip_sign(self) -> None:
        # The text from the label. Holds the expression before and after the sign is flipped
        text = self.__expression_label.cget('text')
        # Holds the reversed new expression as it is built. It is reversed because we want to flip
        # the latest number in the expression
        expression = ''
        # Flag for whether or not the number has been flipped
        number_flipped = False
        # Flag for whether or no the current character is a number
        character_is_number = False
        # Holds the previous character
        previous_character = ''
        # List of arithmetic symbols used in expressions
        symbols_list = ['-', '+', '/', 'x']
        # List of numbers
        numbers_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


        # Go through the reversed expression, find the last number in the equation, and flip its
        # sign.
        for character in reversed(text):
            # If the number has already been flipped, append the all the character to the end of
            # the expression
            if number_flipped:
                expression += character
                previous_character = character
                continue


            # If the character is in the symbols list, check for the correct way to flip the sign
            if character in symbols_list:
                character_is_number = False
                # If the character is a negative sign, replace it with a positive sign
                if character == '-':
                    expression += '+'
                    number_flipped = True


                # If the character is a positive sign, replace it with a negative sign
                elif character == '+':
                    expression += '-'
                    number_flipped = True


                # Otherwise, check if a number came before the symbol
                else:
                    # If a number came before the symbol, add a negative sign then add the symbol
                    if previous_character in numbers_list and not character_is_number:
                        expression += '-'
                        expression += character
                        number_flipped = True


                    # Otherwise, there is no number in front of the symbol to be flipped so just
                    # add the symbol and keep searching
                    else:
                        expression += character


                # Assign previous character to the current character
                previous_character = character
                continue


            # Check if the character is a number
            if character in numbers_list:
                character_is_number = True


            # If the previous character is in the symbols list and the current character is not a
            # number, then the beginning of the last number in the expression has been found. Flip
            # the sign.
            if previous_character in symbols_list and not character_is_number:
                expression += character
                expression += '-'
                number_flipped = True


            # Otherwise, append the character to the expression
            else:
                expression += character


            # Set the previous character equal to the current character at the end of the loop
            previous_character = character


        # set text equal to the unreversed expression
        text = expression[::-1]
        # If no number was flipped, the text has at least on character in it, and that character is
        # a number, then add a negative sign to the front.
        if not number_flipped and len(text) > 0 and character in numbers_list:
            text = '-' + text


        # Set the expression label to the new text.
        self.__expression_label.configure(text=f'{text}')


    def __add_character(self, button_name: str) -> None:
        # If the expression hasn't been evaluated, get the expression so it can be modified
        if not self.__expression_evaluated:
            text = self.__expression_label.cget('text')
        # Otherwise, clear the previous expression
        else:
            text = ''


        # append the button name to the text
        text += button_name
        # Set the expression text to the modified text
        self.__expression_label.configure(text=text)
        # Set expression evaluated to False
        self.__expression_evaluated = False
        # if the button is a number, set the last number entered to that number
        if button_name in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.__last_number_entered = button_name


    def __prep_expression(self, expression: str) -> str:
        # Replace all x multiplication signs with *s since python uses *s from multiplication
        # instead of x's
        expression = expression.replace('x', '*')


        # If the last character in the expression is an arithmetic symbol, assume the last number
        # entered in the expression should be added to the end of the expression
        if expression[-1] in ['-', '+', '/', '*', '(']:
            expression += f'{self.__last_number_entered}'


        # index
        i = 0
        # number of (s in the expression
        open_brace_count = 0
        # number of )s in the expression
        closed_brace_count = 0

        # Go through the expression and check for implicite multiplication and open and closed braces
        for i in range(len(expression)):
            # If the character is a symbol and the index + 1 is less than the number of characters
            # in the expression, check if the next character is a open brace
            if expression[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and i + 1 < len(expression) - 1:
                # If the next character is a open brace, add a multiplication symbol between the
                # number and the open brace, since python will does not know about implicite multiplication
                if expression[i + 1] == '(':
                    first_half = expression[:i + 1] + '*'
                    second_half = expression[i + 1:]
                    expression = first_half + second_half
            # If the character is a open brace, increment the count
            if expression[i] == '(':
                open_brace_count += 1
            # If the character is a closed brace, increment the count
            if expression[i] == ')':
                closed_brace_count += 1


        # reset index to 0
        i = 0
        # If there are more open braces, pad the right side of the expression with closed braces
        if open_brace_count > closed_brace_count:
            for i in range(open_brace_count - closed_brace_count):
                expression += ')'
        # If there are more closed braces, pad the right side of the expression with open braces
        else:
            for i in range(closed_brace_count - open_brace_count):
                expression = '(' + expression


        # return the expression so it can be evaluated
        return expression


    def __calculate(self) -> None:
        # Get the text from the expression
        text = self.__expression_label.cget('text')
        # If there is no text, do nothing
        if not text:
            return
        # Prep the expression for evaluation
        text = self.__prep_expression(text)
        # Evaluate the expression
        evaulation = eval(text)
        # Set the text in the expression label to the evaluated expression
        self.__expression_label.configure(text=f'{evaulation}')
        # Mark the current expression as evaluated
        self.__expression_evaluated = True


    def __clear(self) -> None:
        # Clear the text from the expression label
        self.__expression_label.configure(text='')


if __name__ == '__main__':
    calculator = CalculatorApp()
