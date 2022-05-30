from libs import Load, Beam
import matplotlib.pyplot as plt

load1 = Load(0, 10, 0, -10, -5)
print("\nArea1:\t",load1.area)
print("Centroid1:\t",load1.centroid)

# load2 = Load(7,10,0,0,-10)
# print("\nArea2:\t",load2.area)
# print("Centroid2:\t",load2.centroid)

beam = Beam([load1],10,"rectangular")
print("\nReaction X:\t",beam.reaction_x)
print("Reaction Y:\t",beam.reaction_y)
print("Reaction Moment:\t",beam.reaction_moment)
beam.visualize_loading()
beam.visualize_shear_force()
beam.visualize_bending_moment()