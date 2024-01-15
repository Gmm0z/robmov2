#!/bin/bash

# Source ROS setup
source /opt/ros/noetic/setup.bash  # Replace <your_ros_version> with your ROS version like melodic, noetic etc.
# Alternatively, if you need to source 'devel' from a specific workspace:
# source /path/to/your/catkin/workspace/devel/setup.bash

# Activate conda environment
source /home/palko/anaconda3/etc/profile.d/conda.sh activate percepcion
#conda activate percepcion

# You can even add more commands here if needed

export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/palko/gaz/models
export GAZEBO_RESOURCE_PATH=$GAZEBO_RESOURCE_PATH:/home/palko/gaz/worlds
source /usr/share/gazebo-11/setup.bash

#!/bin/bash

# Source ROS devel setup if it exists
if [ -f "devel/setup.bash" ]; then
    source devel/setup.bash
else
    echo "Could not find ROS devel setup. Skipping."
fi

# Source Conda
if [ -f "/home/palko/anaconda3/etc/profile.d/conda.sh" ]; then
    source /home/palko/anaconda3/etc/profile.d/conda.sh
    conda activate percepcion
else
    echo "Could not find Conda setup. Skipping."
fi

# Any other setup you need
