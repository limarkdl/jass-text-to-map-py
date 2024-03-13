# Assignment JASS 2024 - Task 2

> Ivan Kostin (@limarkdl)

## Start 🚀
### 🛠️ Linux: 
1. Start Docker 
2. Make sure that you are running commands from the ```/task2/``` folder
3. Run ```sudo /bin/bash ./linux_build_and_run.sh```
> Using ```sudo``` because of the Docker permissions


### 🛠️ Windows: 
1. Start Docker
2. Make sure that you are running commands from the ```/task2/``` folder
3. Run script ```windows_build_and_run.bat```

## About ✍️

This application receives a 2D array of symbols and then translate it to a beautiful map in .png

## Using application 🖥️

After it's started, you can see a CLI interface. Follow the instructions and when you are supposed to enter
the data, do it line by line. After you are done, the program will generate a file called ```output.png``` in the ```/task2/``` folder and show it.

## Features 🌟
1. Sticky sidewalks - all sidewalks are following the road and are not separated from it, as close as possible
2. Parking borders - all parking slots have an automatic border to show the parking area
3. Automatic road curves detection - the program detects the road curves and draws it accordingly
4. Prediction of background of a car - the program predicts if the background of the car is a 'Parking' or a 'Road' and draws it accordingly
5. Aligned cars - all cars are aligned to the road. At crossroads angle is random
6. Pattern / Position randomization - the program randomizes the pattern of the buildings, sidewalks, grass, so it looks more interesting
7. Parking connection to the road - the program connects the parking slots to the road (at least it's doing its best)
8. Filling disproportionate maps - the program fills the map with grass if it's not filled

## Examples of usage 👁️

1. City map
    
   ![city.png](examples%2Fcity.png)


2. Map from the assignment

    ![example.png](examples%2Fexample.png)

3. JASS 2024 map

    ![jass.png](examples%2Fjass.png)

5. Something extreme

   ![extreme_crossroad.png](examples%2Fextreme_crossroad.png)
