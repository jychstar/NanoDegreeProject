#!/usr/bin/env python

# Import modules
from pcl_helper import *

import pcl

#rospy.init_node('clustering', anonymous=True)
get_color_list.color_list =[]

# Load Point Cloud file
cloud = pcl.load_XYZRGB('tabletop.pcd')  # <type 'pcl._pcl.PointCloud_PointXYZRGB'>
#print cloud.size  # 202627,  each row is a 4-element tuple

# TODO: Voxel Grid Downsampling
vox = cloud.make_voxel_grid_filter()
LEAF_SIZE = 0.01   
vox.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)
cloud_filtered = vox.filter()

# TODO: PassThrough Filter
passthrough = cloud_filtered.make_passthrough_filter()
filter_axis = 'z'
passthrough.set_filter_field_name(filter_axis)
axis_min = 0.5
axis_max = 1.1
passthrough.set_filter_limits(axis_min, axis_max)
cloud_filtered = passthrough.filter()

# TODO: RANSAC Plane Segmentation
seg = cloud_filtered.make_segmenter()
seg.set_model_type(pcl.SACMODEL_PLANE)
seg.set_method_type(pcl.SAC_RANSAC)
max_distance = 0.01
seg.set_distance_threshold(max_distance)
inliers, coefficients = seg.segment()
extracted_inliers = cloud_filtered.extract(inliers, negative=False)
extracted_outliers = cloud_filtered.extract(inliers, negative=True)

###### Euclidean Clustering

white_cloud = XYZRGB_to_XYZ(extracted_outliers) # <type 'pcl._pcl.PointCloud'>
print "cloud size:",white_cloud.size
# print white_cloud.to_array()    # array of [x,y,z]
tree = white_cloud.make_kdtree()   # <type 'pcl._pcl.KdTree'>

# Create a cluster extraction object
ec = white_cloud.make_EuclideanClusterExtraction()
# Set tolerances for distance threshold 
# as well as minimum and maximum cluster size (in points)
# NOTE: These are poor choices of clustering parameters
# Your task is to experiment and find values that work for segmenting objects.
ec.set_ClusterTolerance(0.05)
ec.set_MinClusterSize(50)
ec.set_MaxClusterSize(1000)
# Search the k-d tree for clusters
ec.set_SearchMethod(tree)
# Extract indices for each of the discovered clusters
cluster_indices = ec.Extract()
print "number of clusters:", len(cluster_indices)
#print cluster_indices

#Assign a color corresponding to each segmented object in scene
cluster_color = get_color_list(len(cluster_indices))

color_cluster_point_list = []

for j, indices in enumerate(cluster_indices):
    print j, len(indices)
    for i, indice in enumerate(indices):
        color_cluster_point_list.append([white_cloud[indice][0],
                                        white_cloud[indice][1],
                                        white_cloud[indice][2],
                                         rgb_to_float(cluster_color[j])])

#Create new cloud containing all clusters, each with unique color
cluster_cloud = pcl.PointCloud_PointXYZRGB()
cluster_cloud.from_list(color_cluster_point_list)

pcl.save(cluster_cloud,'b.pcd')
#pcl.save(extracted_outliers,'b.pcd')


for index, pts_list in enumerate(cluster_indices):
    # Grab the points for the cluster from the extracted outliers (cloud_objects)
    pcl_cluster = extracted_outliers.extract(pts_list) # <type 'pcl._pcl.PointCloud_PointXYZRGB'>

    #print type(pcl_cluster)