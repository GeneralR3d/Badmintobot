Steps that have been taken to build the test dataset using Vision Data
*The first trajectories, 'Trajectory 1' have been purposely left untouched to be used as test data set. They were not used to build the training dataset in any form whatsoever

### Steps
1. Extract out X,Y,Z coordinates from each sheet in the vision data sheet, except those mentioned above
2. For those w 2 parabolas, ie one which also includes the coach throwing the shuttlecock in the air before hitting, filter those not by eye, but through a script to calculate the displacement in 3d, over each timestep. This
3. Swap X and Y columns since X is supposed to be length of badminton court and Y is supposed to be width
4. Scale all 3 by 10 since they are in cm, ML model is trained in mm
5. put in labels for the shots and fill in the time, in increments of 1/30, using excel formulas and auto fill, remembering to remove the formulas using paste values 
6. use python script to transform each trajectory in X Y and Z axes, each in increments of 0.25m which is 250mm, the range is as follows:
    - X: from 0m to 4m which is 0mm to 4000mm( by right half court short service line is until 4.66m)
    - Y: from +2.59m to -2.59m which is +2590mm to -2590mm
    - Z: from 0.1m to 3m which is 100mm to 3000mm
    Transform not individually in each direction, but build a 3d space. For eachx, transform full range of Y, for each Y transform full range of Z.
    Then append all transformed trajectories as new trajectories into the dataset, truncating all those z values that are negative.
7. Use python script to extract out LaunchX,LaunchY,LaunchZ and calculate LaunchAngle,LaunchDirection,InitialV

# Usage Workflow for modifications
0) run findStart.py to identify the true start point of shuttlecock trajectory
1) run trajectoryTransform3d.py to generate cube of transformations
2) run fillfeatures.py to fill in the rest of features in training dataset
3) run trainingcode.py to train the 3 models
4) run predictcode.py to predict trajectory of test trajectory
5) run visualize.py to visualize results in 3d plot
