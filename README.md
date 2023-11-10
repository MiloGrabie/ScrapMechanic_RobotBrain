# ScrapMechanic_RobotBrain
 
This is a robot brain mod for the ScrapMechanic game.

It contains within the scripts directory the lua loop to extract data from the game.
It also execute the command contained in the ./Scripts/JSON/interface_in.json

All the data extracted by the lua loop is contained in the ./Scripts/JSON/interface_out.json

The directory AiRobot contains the brain intelligence.
The main.py file is the main loop that interact with interface_XXX.json files by interacting with the context.py file.
Within the multi_legged file is the code to implement a plateform with X legs.
Within the dog_motion directory is the code specific for the motion of a dog.
In the drone directory is the code specific to a drone motion

There is within the mainPlot.py, the main3D_ray.py, and the raycasts.py file the code to plot the data extracted by the lua loop.
Like the visualization of the robot, and the visualization of the raycasts points that the robot can casts, like a LIDAR.

