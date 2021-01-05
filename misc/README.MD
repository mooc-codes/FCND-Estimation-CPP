
### Step 1: Sensor Noise

Here we collect and process the sensor data from a hovering drone to obtain the 
standard deviation for the GPS and Accelerometer.

Here I load the text data using a python script and use numpy to get std dev

```python
import numpy as np

def get_std_dev(data):
    return np.std(data, axis=0)

def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines.pop(0) # removing the titles
        lines = [float(item.split(',')[1]) for item in lines]
        lines = np.array(lines)
    return lines

gps_data = load_data('Graph1.txt')
print(get_std_dev(gps_data))

accel_data = load_data('Graph2.txt')
print(get_std_dev(accel_data))
```

### Step 3: Attitude Estimation

Here we implement a better sensor data integration for gyro and accelerometer.
For convinience we use the provided `Quaternion<float>` class. which has the methods to
convert to and from frames and also to integrate the values.

```c++
  // current estimates rollEst, pitchEst, ekfState(6) <- this is yaw estimate
  float T_s = dtIMU;
  float yawEst = ekfState(6);

  //we use the state to define a quaternion, qt, for the euler angles for φ, θ and ψ.
  Quaternion<float> q_t;
  q_t = Quaternion<float>::FromEuler123_RPY(rollEst, pitchEst, yawEst);

  V3D dq(gyro.x, gyro.y, gyro.z); // rates in body frame
  //  predicted quaternion q_bar_t = dq ∗ qt 
  Quaternion<float> q_bar_t = q_t.IntegrateBodyRate(dq, T_s); 
 
  // Predicted Estimates
  float phi_bar_t = q_bar_t.Roll(); // returns angles in world frame
  float theta_bar_t = q_bar_t.Pitch();
  float psi_bar_t = q_bar_t.Yaw();
  ekfState(6) = psi_bar_t;

  // normalize yaw to -pi .. pi
  if (ekfState(6) > F_PI) ekfState(6) -= 2.f*F_PI;
  if (ekfState(6) < -F_PI) ekfState(6) += 2.f*F_PI;


```


### Step 3: 