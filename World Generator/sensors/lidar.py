import math
import numpy as np
import pybullet as p

_EPS = np.finfo(float).eps * 4.0

class LidarSensor:

    def __init__(self, robot_id, link_idx, pos, orn, ray_min=0.02, ray_max=0.4, ray_num_ver=6, ray_num_hor=12) -> None:
        self.ray_min = ray_min
        self.ray_max = ray_max
        self.ray_num_ver = ray_num_ver
        self.ray_num_hor = ray_num_hor
        self.robot_id = robot_id
        self.link_idx = link_idx
        self.pos = pos
        self.orn = orn
        # How to use this stuff???
        # #p.setCollisionFilterGroupMask(robot_id, link_idx, 0b001)

    def update(self):
        link_state = p.getLinkState(self.robot_id, self.link_idx)
        new_transform = p.multiplyTransforms(link_state[0], link_state[1], self.pos, self.orn)
        self.current_pos = new_transform[0]
        self.current_orn = new_transform[1]
        self._set_lidar_cylinder(render=True)

    def quaternion_matrix(self, quaternion):
        """Return homogeneous rotation matrix from quaternion.
        >>> R = quaternion_matrix([0.06146124, 0, 0, 0.99810947])
        >>> numpy.allclose(R, rotation_matrix(0.123, (1, 0, 0)))
        True
        """
        q = np.array(quaternion[:4], dtype=np.float64, copy=True)
        nq = np.dot(q, q)
        if nq < _EPS:
            return np.identity(4)
        q *= math.sqrt(2.0 / nq)
        q = np.outer(q, q)
        return np.array((
            (1.0-q[1, 1]-q[2, 2],     q[0, 1]-q[2, 3],     q[0, 2]+q[1, 3], 0.0),
            (    q[0, 1]+q[2, 3], 1.0-q[0, 0]-q[2, 2],     q[1, 2]-q[0, 3], 0.0),
            (    q[0, 2]-q[1, 3],     q[1, 2]+q[0, 3], 1.0-q[0, 0]-q[1, 1], 0.0),
            (                0.0,                 0.0,                 0.0, 1.0)
            ), dtype=np.float64)
    
    def _set_lidar_cylinder(self, render=False):
        ray_froms = []
        ray_tops = []
        frame = self.quaternion_matrix(self.current_orn)
        frame[0:3,3] = self.current_pos
        ray_froms.append(np.matmul(np.asarray(frame),np.array([0.0,0.0,0.01,1]).T)[0:3].tolist())
        ray_tops.append(np.matmul(np.asarray(frame),np.array([0.0,0.0,self.ray_max,1]).T)[0:3].tolist())


        for angle in range(230, 270, 20):
            for i in range(self.ray_num_hor):
                z = -self.ray_max * math.sin(angle*np.pi/180)
                l = self.ray_max * math.cos(angle*np.pi/180)
                x_end = l*math.cos(2*math.pi*float(i)/self.ray_num_hor)
                y_end = l*math.sin(2*math.pi*float(i)/self.ray_num_hor)
                start = np.matmul(np.asarray(frame),np.array([0.0,0.0,0.01,1]).T)[0:3].tolist()
                end = np.matmul(np.asarray(frame),np.array([x_end,y_end,z,1]).T)[0:3].tolist()
                ray_froms.append(start)
                ray_tops.append(end)
        
        # set the angle of rays
        interval = -0.005
        
        for i in range(8):
            ai = i*np.pi/4
            for angle in range(self.ray_num_ver):    
                z_start = (angle)*interval-0.1
                x_start = self.ray_min*math.cos(ai)
                y_start = self.ray_min*math.sin(ai)
                start = np.matmul(np.asarray(frame),np.array([x_start,y_start,z_start,1]).T)[0:3].tolist()
                z_end = (angle)*interval-0.1
                x_end = self.ray_max*math.cos(ai)
                y_end = self.ray_max*math.sin(ai)
                end = np.matmul(np.asarray(frame),np.array([x_end,y_end,z_end,1]).T)[0:3].tolist()
                ray_froms.append(start)
                ray_tops.append(end)
        
        for angle in range(250, 270, 20):
            for i in range(self.ray_num_hor):
                z = -0.2+self.ray_max * math.sin(angle*np.pi/180)
                l = self.ray_max * math.cos(angle*np.pi/180)
                x_end = l*math.cos(math.pi*float(i)/self.ray_num_hor-np.pi/2)
                y_end = l*math.sin(math.pi*float(i)/self.ray_num_hor-np.pi/2)
                
                start = np.matmul(np.asarray(frame),np.array([x_start,y_start,z_start-0.1,1]).T)[0:3].tolist()
                end = np.matmul(np.asarray(frame),np.array([x_end,y_end,z,1]).T)[0:3].tolist()
                ray_froms.append(start)
                ray_tops.append(end)
        results = p.rayTestBatch(ray_froms, ray_tops)
        
        if render:
            hitRayColor = [0, 1, 0]
            missRayColor = [1, 0, 0]

            for index, result in enumerate(results):
                if result[0] == -1:
                    p.addUserDebugLine(ray_froms[index], ray_tops[index], missRayColor)
                else:
                    p.addUserDebugLine(ray_froms[index], ray_tops[index], hitRayColor)
        return results