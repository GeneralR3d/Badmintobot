Steps that have been taken to build the test dataset using Vision Data
*The first 2 trajectories, 'Trajectory 1' have been purposely left untouched to be used as test data set. They were not used to build the training dataset in any form whatsoever

### Steps
1. Extract out X,Y,Z coordinates from each sheet in the vision data sheet, except those mentioned above
2. For those w 2 parabolas, ie one which also includes the coach throwing the shuttlecock in the air before hitting, filter those out too by using plotting out one by one and taking out the frames, using visualize.py, using MAGIC FRAME NUMBER
3. Swap X and Y columns since X is supposed to be length of badminton court and Y is supposed to be width
4. Scale all 3 by 10 since they are in cm, ML model is trained in mm
5. put in labels for the shots and fill in the time, in increments of 1/30, using excel formulas and auto fill, remembering to remove the formulas using paste values 
6. use python script to transform each trajectory in X Y and Z axes, each in increments of 0.1m which is 100mm, the range is as follows:
    - X: from 0m to 4m which is 0mm to 4000mm( by right half court short service line is until 4.66m)
    - Y: from +2.59m to -2.59m which is +2590mm to -2590mm
    - Z: from 0.1m to 3m which is 100mm to 3000mm
    Then append all transformed trajectories as new trajectories into the dataset
7. Use python script to extract out LaunchX,LaunchY,LaunchZ and calculate LaunchAngle,LaunchDirection,InitialV