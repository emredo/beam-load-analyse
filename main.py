from libs import Load, Beam
import os
import time

print("Hello, please look the user guide to understand program working logic.")
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
    operation = input("\nPlease press any key to continue entering loading properties. Don't forget, the loading must be in N/mm. \nIf you finished entering load data, plese tpye 'done':\t")
    if operation == "done":
        break
    load_start = int(float(input("\nPlease enter the load start point: ")))
    load_end = int(float(input("Please enter the load end point: ")))
    if load_end < load_start or load_start > beam_length or load_end > beam_length:
        print("\nPlease enter a valid load end point.\n")
        continue

    try:
        load_function_a = float(input("Please enter the coefficient of x^2 : "))
        load_function_b = float(input("Please enter the coefficient of x : "))
        load_function_c = float(input("Please enter the constant C : "))
        loads.append(Load(load_start, load_end, -1 * load_function_a, -1 * load_function_b, -1 * load_function_c))
    except:
        print("Wrong load function data, please be carefull about a, b and c coeffs of load function.")

assert loads != [], "No correct load data, exiting!!!"
beam = Beam(loads,beam_length,beam_section_type)

beam_safety_shear_stress = int(float(input("\nPlease enter the safety shear stress in MPa: ")))
beam_safety_tensile_stress = int(float(input("Please enter the safety tensile stress in MPa: ")))
beam_safety_coef = int(float(input("Please enter the safety coefficient: ")))

print("\nBEAM PROPERTIES\nMoment of Inertia (mm^4): {}\nArea (mm^2): {}\nBeam length (mm): {}\nSection type: {}\n".format(beam.moi,beam.section_area,beam.length,beam.section_type))
print("\nREACTION VALUES\nReaction X in (N):\t{}\nReaction Y in (N):\t{}\nReaction Moment (N.mm):\t{}\nMaximum normal stress (N/mm^2):\t{}\nMaximum shear stress (N/mm^2):\t".format(beam.reaction_x,
                                                                            beam.reaction_y,
                                                                            beam.reaction_moment,beam.max_normal_stress,beam.max_shear_stress))
if beam_safety_shear_stress < beam_safety_coef * beam.max_shear_stress:
    print("\nWARNING: Maximum shear stress is higher than safety shear stress.\n")
else:
    print("\nMaximum shear stress is lower than safety shear stress.\n")

if beam_safety_tensile_stress < beam_safety_coef * beam.max_normal_stress:
    print("\nWARNING: Maximum normal stress is higher than safety tensile stress.\n")
else:
    print("\nMaximum normal stress is lower than safety tensile stress.\n")

path = os.getcwd()
path = os.path.join(path,"save_{}".format(int(time.time())))
os.mkdir(path)

beam.visualize_loading(path)
beam.visualize_shear_force(path)
beam.visualize_bending_moment(path)
beam.visualize_tensile_strength(path)
beam.visualize_shear_strength(path)