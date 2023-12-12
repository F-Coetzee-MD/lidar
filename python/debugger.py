import matplotlib.pyplot as plt
import numpy as np

class Debugger:
    def plot(self, y_values_array, labels):
        x_values = np.arange(max(map(len, y_values_array)))  # Generating x values as a range of numbers

        # Plotting each set of y values
        for y_values, label in zip(y_values_array, labels):
            plt.plot(x_values[:len(y_values)], y_values, marker="o", linestyle="-", label=label)

        # Adding labels and title
        plt.xlabel("X values")
        plt.ylabel("Y values")
        plt.title("Value Plots")

        # Display the legend
        plt.legend()

        # Show the plot
        plt.show()

    def save_array_to_txt(self, array, file_path):
        with open(file_path, "w") as file:
            for item in array:
                file.write(str(item) + '\n')

    def read_array_from_txt(self, file_path):
        """
        Read a Python array from a text file.

        Parameters:
        - file_path: The file path from which the array will be read.

        Returns:
        - array: The Python array read from the file.
        """
        array = []

        with open(file_path, 'r') as file:
            for line in file:
                # Remove leading and trailing whitespaces, then convert to the appropriate data type
                element = line.strip()
                try:
                    element = eval(element)  # Try to evaluate the string as a literal (e.g., int, float)
                except (NameError, SyntaxError):
                    pass  # If not a literal, keep it as a string

                array.append(element)

        return array