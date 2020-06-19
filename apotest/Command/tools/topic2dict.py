import sys
import rosbag
import os
import numpy as np
import math
import datetime
import argparse

def topic2dict(bag):
    out_file = {}
    global clbale
    time_offset = bag.get_start_time()
    scale = [411101.0, 3363248.0, 0]

    world_x = 0.
    world_y = 0.
    world_theta = 0.
    clbale = False
    out_file['/cmd_vel'] = []
    out_file['/chassis/speed_limit'] = []
    out_file['/platform/platform_guardian'] = []
    for topic, msg_pb, t in bag.read_messages():
        if topic == '/apollo/localization/pose':
            out_file['/localization']=(','.join([str(msg_pb.header.timestamp_sec - time_offset),
                                                          str(msg_pb.measurement_time),
                                                          str(msg_pb.pose.position.x - scale[0]),
                                                          str(msg_pb.pose.position.y - scale[1]),
                                                          str(msg_pb.pose.heading), str(msg_pb.pose.angular_velocity.z),
                                                          str(msg_pb.pose.linear_velocity.x),
                                                          str(msg_pb.pose.linear_velocity.y),
                                                          str(msg_pb.pose.linear_velocity_vrf.x)]) + '\n')
            world_x = msg_pb.pose.position.x - scale[0]
            world_y = msg_pb.pose.position.y - scale[1]
            world_theta = msg_pb.pose.heading
        elif topic == '/apollo/perception/obstacles':
            obstacle_x = ""
            obstacle_y = ""
            position_x = ""
            if world_x:
                rotation = np.matrix([[np.cos(world_theta), -np.sin(world_theta), world_x],
                                      [np.sin(world_theta), np.cos(world_theta), world_y], [0, 0, 1]])
                # print(rotation)
                for perception_obstacle in msg_pb.perception_obstacle:
                    # print(np.matrix([[trajectory_point.path_point.x,trajectory_point.path_point.y,1]]))
                    pose = rotation * np.matrix(
                        [[perception_obstacle.position.x], [perception_obstacle.position.y], [1]])
                    # print(pose[0,0])
                    obstacle_x += "_" + str(pose[0, 0])
                    obstacle_y += "_" + str(pose[1, 0])
                    position_x += "_" + str(perception_obstacle.position.x)

                if obstacle_x:
                    out_file['/perception']=(','.join([str(msg_pb.header.timestamp_sec - time_offset),
                                                                obstacle_x, obstacle_y, str(world_x), str(world_y),
                                                                str(world_theta), position_x
                                                                ]) + '\n')
        elif topic == '/apollo/planning':
            trajectory_x = ""
            trajectory_y = ""
            trajectory_theta = ""
            if world_x:
                rotation = np.matrix([[np.cos(world_theta), -np.sin(world_theta), world_x],
                                      [np.sin(world_theta), np.cos(world_theta), world_y], [0, 0, 1]])
                # print(rotation)
                for trajectory_point in msg_pb.trajectory_point:
                    # print(np.matrix([[trajectory_point.path_point.x,trajectory_point.path_point.y,1]]))
                    pose = rotation * np.matrix([[trajectory_point.path_point.x], [trajectory_point.path_point.y], [1]])
                    # print(pose[0,0])
                    trajectory_x += "_" + str(pose[0, 0])
                    trajectory_y += "_" + str(pose[1, 0])
                    trajectory_theta += "_" + str(trajectory_point.path_point.theta)

                if trajectory_x:
                    out_file['/planning']=(','.join([str(msg_pb.header.timestamp_sec - time_offset),
                                                              trajectory_x, trajectory_y, trajectory_theta,
                                                              str(world_x), str(world_y), str(world_theta)
                                                              ]) + '\n')
        elif topic == '/apollo/control':
            # print("control_time:" + str(msg_pb.header.timestamp_sec - time_offset))
            out_file['/control']=(','.join([str(msg_pb.header.timestamp_sec - time_offset),
                                                     str(msg_pb.linear_velocity), str(msg_pb.angular_velocity),
                                                     str(t.secs + float(t.nsecs) / 1000000000 - time_offset)
                                                     ]) + '\n')
        elif topic == '/platform/earth_gps':
            out_file['/earth_gps']=(','.join([str(msg_pb.x), str(msg_pb.y), str(msg_pb.theta)]) + '\n')
        elif topic == '/cmd_vel':
            # print("cmd_vel_time:" + str(t.secs + t.nsecs/1000000000 - time_offset))
            out_file['/cmd_vel'].append((','.join([str(t.secs + float(t.nsecs) / 1000000000 - time_offset),
                                                     str(msg_pb.linear.x), str(msg_pb.angular.z)
                                                     ]) + '\n'))
        elif topic == '/chassis/speed_limit':
            out_file['/chassis/speed_limit'].append(msg_pb)
            out_file['/chassis/speed_limit'].append(t)
        elif topic == '/platform/platform_guardian':
            out_file['/platform/platform_guardian'].append(msg_pb)
            out_file['/platform/platform_guardian'].append(t)
        elif topic == '/apollo/guardian':
            out_file['/guardian']=(','.join([str(msg_pb.header.timestamp_sec - time_offset),
                                                      str(msg_pb.max_linear_velocity), str(msg_pb.min_linear_velocity),
                                                      str(msg_pb.max_angular_velocity), str(msg_pb.min_angular_velocity)
                                                      ]) + '\n')
        elif topic == '/fence_vel':
            out_file['/fence_vel']=(','.join([str(msg_pb.header.timestamp_sec - time_offset),
                                                       str(msg_pb.max_linear_x), str(msg_pb.min_linear_x),
                                                       str(msg_pb.max_angular_z), str(msg_pb.min_angular_z)
                                                       ]) + '\n')
        elif topic == '/apollo/ultanalyse':
            obst_distances = {}
            obst_xs = {}
            obst_ys = {}
            # print(msg_pb.obstinfo)
            for obst_obj in msg_pb.obstinfo:
                obst_distances[obst_obj.detec_sonar] = obst_obj.obst_distance
                obst_xs[obst_obj.detec_sonar] = obst_obj.location_x
                obst_ys[obst_obj.detec_sonar] = obst_obj.location_y
            if obst_xs != {}:
                distances = ""
                obst_x = 0
                obst_y = 0
                for i in range(1, 13):
                    sensor_distance = 500
                    obst_x = 0
                    obst_y = 0
                    if i in obst_distances:
                        sensor_distance = obst_distances[i]
                        if world_x:
                            # print(obst_xs[i],obst_ys[i])
                            rotation = np.matrix([[np.cos(world_theta), -np.sin(world_theta), world_x],
                                                  [np.sin(world_theta), np.cos(world_theta), world_y], [0, 0, 1]])
                            pose = rotation * np.matrix([[obst_xs[i] / 100], [obst_ys[i] / 100], [1]])
                            # print(pose[0,0])
                            obst_x = pose[0, 0]
                            obst_y = pose[1, 0]
                    if distances:
                        distances = ','.join([distances, str(sensor_distance), str(obst_x), str(obst_y)])
                    else:
                        distances = ','.join([str(sensor_distance), str(obst_x), str(obst_y)])
                # print(distances)
                out_file['/ultanalyse']=(','.join([str(msg_pb.header.timestamp_sec - time_offset),
                                                            distances, str(world_x), str(world_y)
                                                            ]) + '\n')
    return out_file

def writetopic(bag,topic,path):
    with open(path+'bag_read.txt','w') as f:
        Bag = rosbag.Bag(bag)
        output = topic2dict(Bag)
        print(output.keys())
        f.write(str(output[topic]))
        f.close()


