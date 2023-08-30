**(FAST) Fan_Adjustment_for_System_Temperature**

A script that would monitor Dell R730 PowerEdge temperature sensors and manage the fan speeds in real-time.

<img width="1029" alt="Screenshot 2023-08-28 at 1 59 09 PM" src="https://github.com/cemdede/Fan_Adjustment_for_System_Temperature/assets/14031604/5cb2de7a-537e-48e9-9202-72fb6beb8d31">

Dell PowerEdge R730 has a habit of being angry and reflects its anger with fan noise if you add any GPU or any other parts that are not from Dell.
Even though Bios is updated, these problems make it annoying if you use the server for home-labs or as a low-budget, old, powerful, but reliable analysis server.

In my case, my R730 was so calm that I added the Tesla P100 16GB GPU for image segmentation-based analysis. The fans started to full throttle from ~2200RPM to 14000RPM. However, by completing IDRAC Bios tests I managed to lower it down to ~8000RPM, which is still noisy. I found a couple of Hex scripts that can be run on bash, but these were not responsive to the changes in the temperatures.

Here are the bash codes if you would like to manually control the fans:

sudo ipmitool raw 0x30 0x30 0x01 0x00

For example, to set the fan speed to 20%:
sudo ipmitool raw 0x30 0x30 0x02 0xff 0x14

For example, to set the fan speed to 22%:
sudo ipmitool raw 0x30 0x30 0x02 0xff 0x16


ipmitool raw - send raw IPMI command
0x30 0x30 - IPMI class for fan control
0x02 - target fan 2
0xff - apply to all fans
0x16 - hex value for 22% speed
The hex values from 0x00 to 0x64 (0 to 100 decimal) map to the percentage range for fan speeds.

So 0x16 hex converts to 22 decimal, setting a 22% fan speed.

To quickly summarize the key points:

Use ipmitool raw for raw IPMI commands
0x30 0x30 class is for fan control
Last hex byte sets the percentage (0x16 -> 22%)


Monitor fan speed:
sudo ipmitool sdr type fan

Monitor temperature:
sudo ipmitool sdr type temperature


By using these bash codes, I generated the following script that informs the user in real-time regarding the temperature changes and controls the fan speeds.
I used a sigmoid model for this script, and the simulated outputs are plotted below.

* This is my taste for the fan speed after all, but you can change the script to your own taste.

Here's the simulated plot representing the expected values of temperature and fan speeds if you use this script:

![image](https://github.com/cemdede/Fan_Adjustment_for_System_Temperature/assets/14031604/68d8f0c0-b6c9-47e2-89aa-2cc54f2689c7)

Interpretation of Plots
Temperature Zones Plot (Left Side):
Green Zone (34-38°C): Everything is fine; no need to worry.
Yellow Zone (38-50°C): Keep an eye out; might need some attention soon.
Orange Zone (50-70°C): Warning; consider taking action.
Red Zone (70+°C): Critical; immediate action required.

Fan Speed based on Temperature Plot (Right Side):
The blue curve shows how the fan speed changes as a function of the temperature. The fan speed is represented as a percentage, calculated using the sigmoid function. It's a smooth curve that starts to steeply rise after 60°C, which means the fan will speed up more quickly as the temperature increases beyond that point.

And here is what happens if you'd like to play a bit with the parameters:

![image](https://github.com/cemdede/Fan_Adjustment_for_System_Temperature/assets/14031604/06f406ed-1d11-4dfc-a5d2-0f9c87b5f152)


**Concepts and Explanations**
**Curses**: The curses library allows you to create text-based user interfaces. It handles keyboard input and display formatting, allowing you to make dynamic, terminal-based applications. You initialize it with curses.wrapper(main), which takes care of setup and teardown.

**IPMItool**: You're using the Intelligent Platform Management Interface tool (ipmitool) to interact with the hardware. It's a powerful utility for managing and monitoring devices that support IPMI.

**Sigmoid Function**: You use a sigmoid function to map temperature values to fan speeds in a smooth way. This is a really interesting approach! The sigmoid function is often used in machine learning, specifically in logistic regression and neural networks, to map any input into a value between 0 and 1.

**Regular Expressions**: You're using regex (re.search) to extract numeric values from the shell output. This is very efficient for text parsing.

**Logging**: You're logging the status and changes, which is a best practice. It will help you debug issues and understand the behavior over time.

**Hex Conversion**: You convert the fan speed to hex before running the ipmitool command. This is probably a requirement from the IPMI's raw command.

**How To Run the program**: Just download,

**Run**: chmod +x FAST_Fan_Adjustment_for_System_Temperature.py

**Then Run**: sudo python3 FAST_Fan_Adjustment_for_System_Temperature.py

**To quit**: just hit "q"

IMPORTANT: 
1)This works for me pretty well (on Ubuntu 22.04.3 LTS Server), but it shouldn't have to work for you.

2)I tested it on a Cuda job (I added the jupyter notebook as CUDA_test), and it throttles the fans when Cuda pressures but pushes the breaks when not.

3)This is a quick fix, not a permanent fix. To make it permanent, first try it to see if it works for you as intended, then add it to the startup as a service.

Cheers!

###################################################

###**Fan_Adjustment_for_System_TemperatureV2**: Has cosmetic changes. 

<img width="1047" alt="Screenshot 2023-08-29 at 7 59 55 PM" src="https://github.com/cemdede/Fan_Adjustment_for_System_Temperature/assets/14031604/cedac283-ceab-49a5-ad98-4b8f22b07383">

- Fans and Temperatures can be stable when you don't use too much computing power or GPU, so I had to add a spinner to remind the user that it is running.




