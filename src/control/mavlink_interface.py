# Dev 3 - MAVLink Interface + PID Controller
# Yeh file drone ko move karti hai

import time
import numpy as np

class PIDController:
    def __init__(self):
        # Tuned parameters for physical UAV response
        self.Kp_yaw = 0.003
        self.Kd_yaw = 0.001
        
        self.Kp_z = 0.005
        self.Kd_z = 0.002
        
        self.Kp_x = 0.00005 # scaling box area
        
        self.prev_error_yaw = 0
        self.prev_error_z = 0
        self.last_time = time.time()
        
        self.target_area = 40000.0  # Desired bounding box area (maintains distance)

    def calculate(self, target_cx, target_cy, box_area, frame_w=1280, frame_h=720):
        current_time = time.time()
        dt = current_time - self.last_time
        if dt <= 0.0:
            dt = 0.05
        self.last_time = current_time

        # 1. YAW RATE (Horizontal Error)
        error_yaw = target_cx - (frame_w / 2.0)
        d_yaw = (error_yaw - self.prev_error_yaw) / dt
        yaw_rate = (self.Kp_yaw * error_yaw) + (self.Kd_yaw * d_yaw)
        self.prev_error_yaw = error_yaw

        # 2. ALTITUDE Vz (Vertical Error) - Down is positive in NED
        # Target above center means negative error -> we want Vz negative (go up)
        error_z = target_cy - (frame_h / 2.0)
        d_z = (error_z - self.prev_error_z) / dt
        vz = (self.Kp_z * error_z) + (self.Kd_z * d_z)
        self.prev_error_z = error_z

        # 3. FORWARD VELOCITY Vx (Bounding Box Area)
        error_area = self.target_area - box_area
        vx = self.Kp_x * error_area

        # Smoothing and clamping
        yaw_rate = np.clip(yaw_rate, -1.0, 1.0)
        vz = np.clip(vz, -2.0, 2.0)
        vx = np.clip(vx, -2.0, 3.0)

        # Apply deadzones to avoid jitter
        if abs(error_yaw) < 30: yaw_rate = 0.0
        if abs(error_z) < 30: vz = 0.0
        if abs(error_area) < 5000: vx = 0.0

        return vx, 0.0, vz, yaw_rate


# TEST - Yeh chalao dekho kaam karta hai ya nahi
if __name__ == "__main__":
    pid = PIDController()
    
    # Target daayein hai (800, 360), center hai (640, 360)
    vx, vy = pid.calculate(800, 360)
    print(f"Target daayein hai → Drone daayein jayega: vx={vx:.4f}")
    
    # Target neeche hai (640, 500)
    vx, vy = pid.calculate(640, 500)
    print(f"Target neeche hai → Drone neeche jayega: vy={vy:.4f}")
    
    # Target center mein hai (640, 360)
    vx, vy = pid.calculate(640, 360)
    print(f"Target center mein hai → Drone ruke: vx={vx:.4f}, vy={vy:.4f}")