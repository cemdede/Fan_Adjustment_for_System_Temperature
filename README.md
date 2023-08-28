(FAST) Fan_Adjustment_for_System_Temperature
A script that would monitor Dell R730 PowerEdge temperature sensors and manage the fan speeds in real-time.

Here's the simulated plot representing the expected values of temperature and fan speeds:

![image](https://github.com/cemdede/Fan_Adjustment_for_System_Temperature/assets/14031604/68d8f0c0-b6c9-47e2-89aa-2cc54f2689c7)

Interpretation of Plots
Temperature Zones Plot (Left Side):
Green Zone (34-38°C): Everything is fine; no need to worry.
Yellow Zone (38-50°C): Keep an eye out; might need some attention soon.
Orange Zone (50-70°C): Warning; consider taking action.
Red Zone (70+°C): Critical; immediate action required.

Fan Speed based on Temperature Plot (Right Side):
The blue curve shows how the fan speed changes as a function of the temperature. The fan speed is represented as a percentage, calculated using the sigmoid function. It's a smooth curve that starts to steeply rise after 60°C, which means the fan will speed up more quickly as the temperature increases beyond that point.

**Concepts and Explanations**
**Curses**: The curses library allows you to create text-based user interfaces. It handles keyboard input and display formatting, allowing you to make dynamic, terminal-based applications. You initialize it with curses.wrapper(main), which takes care of setup and teardown.

**IPMItool**: You're using the Intelligent Platform Management Interface tool (ipmitool) to interact with the hardware. It's a powerful utility for managing and monitoring devices that support IPMI.

**Sigmoid Function**: You use a sigmoid function to map temperature values to fan speeds in a smooth way. This is a really interesting approach! The sigmoid function is often used in machine learning, specifically in logistic regression and neural networks, to map any input into a value between 0 and 1.

**Regular Expressions**: You're using regex (re.search) to extract numeric values from the shell output. This is very efficient for text parsing.

**Logging**: You're logging the status and changes, which is a best practice. It will help you debug issues and understand the behavior over time.

**Hex Conversion**: You convert the fan speed to hex before running the ipmitool command. This is probably a requirement from the IPMI's raw command.

