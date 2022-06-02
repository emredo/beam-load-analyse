from libs import Load, Beam
import os
import time

print("Hello, please look the user guide to understand program working logic.\n")
while True:
    try:
        beam_length = int(float(input("Please enter the beam length in milimeter: ")))
        break
    except:
        print("\nPlease enter a number.\n")
assert beam_length > 0, "Wrong beam length data, exiting!!!"

while True:
    beam_section_type = input("\nPlease enter the beam section type etc. [rectangular, circular, i_section, h_section, t_section]: ")
    if beam_section_type in ["rectangular", "circular", "i_section", "h_section", "t_section"]:
        break
    else:
        print("\nPlease enter a valid beam section type.\n")

loads = []
while True:
    print(50*"*")
    operation = input("Please press any key to continue entering loading properties:\nIf you finished entering load data, plese tpye 'done':\t")
    if operation == "done":
        break
    load_start = int(float(input("Please enter the load start point: ")))
    load_end = int(float(input("Please enter the load end point: ")))
    if load_end < load_start or load_start > beam_length or load_end > beam_length:
        print("\nPlease enter a valid load end point.\n")
        continue
    #note: if user enters non float value, program raises error.
    load_function_a = float(input("Please enter the coefficient of x^2 which is load function: "))
    load_function_b = float(input("Please enter the coefficient of x which is load function: "))
    load_function_c = float(input("Please enter the constant which is load function: "))
    loads.append(Load(load_start,load_end,-1*load_function_a,-1*load_function_b,-1*load_function_c))

assert loads != [], "No correct load data, exiting!!!"
beam = Beam(loads,beam_length,beam_section_type)

print("\nBEAM PROPERTIES\nMoment of Inertia: {}\nArea: {}\nLength: {}\nSection type: {}\n".format(beam.moi,beam.section_area,beam.length,beam.section_type))
print("\nREACTION VALUES\nReaction X:\t{}\nReaction Y:\t{}\nReaction Moment:\t{}\nMaximum normal stress:\t{}\nMaximum shear stress:\t".format(beam.reaction_x,
                                                                            beam.reaction_y,
                                                                            beam.reaction_moment,beam.max_normal_stress,0))

path = os.getcwd()
path = os.path.join(path,"save_{}".format(int(time.time())))
os.mkdir(path)

beam.visualize_loading(path)
beam.visualize_shear_force(path)
beam.visualize_bending_moment(path)
beam.visualize_tensile_strength(path)
beam.visualize_shear_strength(path)