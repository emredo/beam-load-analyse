import os.path
import numpy as np
import matplotlib.pyplot as plt
from moi import CalculateMoi

#Load class for manipulating load data. Object attributes can be used for plotting or other calculations.
class Load(object):
    def __init__(self, x_start, x_end, a, b, c):
        self.x_start = x_start
        self.x_end = x_end
        self.a = a
        self.b = b
        self.c = c
        self.dx = 0.001
        self.load_length = self.x_end - self.x_start
        self.distribution = self.load_distribution_func()
        self.area = self.calculate_area()
        self.centroid = self.calculate_centroid()

    def function(self,x):
        return self.a*x**2 + self.b*x + self.c

    def integrated_func(self,x):
        return self.a*(x**3)/3 + self.b*(x**2)/2 + self.c*x

    def second_integrated_func(self,x):
        return self.a*(x**4)/12 + self.b*(x**3)/6 + self.c*(x**2)/2

    def load_distribution_func(self):
        x = 0
        distribution = []
        if self.load_length != 0:
            while x < self.load_length:
                distribution.append(self.function(x))
                x += self.dx
        else:
            distribution.append(self.function(x))
        return distribution

    def integrate(self):
        summary_bottom = 0
        summary_top = 0
        if self.x_end - self.x_start != 0:
            x = 0
            while x < (self.x_end - self.x_start):
                summary_bottom += self.function(x)*self.dx
                x += self.dx
            x = self.x_end - self.x_start
            while x > self.x_start:
                summary_top += self.function(x)*self.dx
                x -= self.dx
            return (summary_top + summary_bottom)/2
        else:
            summary_bottom = self.function(self.x_start)
            return summary_bottom

    def calculate_area(self):
        if self.load_length != 0:
            area = self.integrated_func(self.load_length) - self.integrated_func(0)
        else:
            area = self.function(0)
        return area

    def calculate_centroid(self):
        x = 0
        area_moment = 0
        if self.load_length != 0:
            while x < self.load_length:
                area_moment += self.function(x)*self.dx*x
                x += self.dx
            centroid_x = area_moment/self.area
            return self.x_start + centroid_x
        else:
            return self.x_start

#Beam class includes all the attributes and methods for a single beam.
class Beam(object):
    def __init__(self, loading_list, length, section_type):
        self.loading_list = loading_list
        self.dx = loading_list[0].dx
        self.length = length
        self.section_type = section_type
        try:
            self.moi_calculations = CalculateMoi(self.section_type)
        except:
            assert True, "Wrong section shapes, exiting program. Try again."
        self.moi = self.moi_calculations.moi
        self.max_y = self.moi_calculations.max_y
        self.section_area = self.moi_calculations.section_area
        self.qx = self.moi_calculations.qx
        self.section_thickness = self.moi_calculations.section_thickness
        self.reaction_x, self.reaction_y, self.reaction_moment = self.calculate_reactions()
        self.load_distribution_list = self.load_distribution()
        self.shear_force_list = self.shear_force_distribution()
        self.bending_moment_list = self.bending_moment_distribution()
        self.tensile_stress_list = self.tensile_stress_distribution()
        self.shear_stress_list = self.shear_stress_distribution()
        self.max_normal_stress = max(self.bending_moment_list)*self.max_y/self.moi
        if self.qx == 0:  # if section type is circular.
            self.max_shear_stress = max(self.shear_force_list)/self.section_area * 3 / 2
        else: #other section types
            self.max_shear_stress = (max(self.shear_force_list)*self.qx)/(self.moi*self.section_thickness)

    def calculate_reactions(self):
        reaction_x = 0
        reaction_y = 0
        moment = 0
        for loading_obj in self.loading_list:
            reaction_y -= loading_obj.area
            moment -= loading_obj.centroid * loading_obj.area
        return reaction_x, reaction_y, moment

    ######################      Load and cutting reactions distributions    ###################
    def load_distribution(self):
        load_list = (self.length * int(1 / self.dx) + 1) * [0]
        for loading_obj in self.loading_list:
            x = loading_obj.x_start * int(1 / self.dx)
            for diff_load in loading_obj.distribution:
                load_list[x] += diff_load
                x += 1
        return load_list

    def shear_force_distribution(self):
        shear_force_list = []
        shear_force = self.reaction_y
        for force in self.load_distribution_list:
            shear_force_list.append(shear_force)
            index = self.load_distribution_list.index(force)
            if index != 0:
                if self.load_distribution_list[index] != 0 and self.load_distribution_list[index+1] == 0 and self.load_distribution_list[index-1] == 0:
                    shear_force += force
                else:
                    shear_force += (force*self.dx)
            else:
                shear_force += (force * self.dx)
        return shear_force_list

    def bending_moment_distribution(self):
        bending_moment_list = []
        bending_moment = -1*self.reaction_moment
        for shear_force in self.shear_force_list:
            bending_moment_list.append(bending_moment)
            bending_moment += (shear_force*self.dx)
        return bending_moment_list

    ######################      Stress distributions    ###################
    def shear_stress_distribution(self):
        shear_strength_list = []
        for shear_force in self.shear_force_list:
            shear_strength_list.append((shear_force*self.qx)/(self.moi*self.section_thickness))
        return shear_strength_list

    def tensile_stress_distribution(self):
        tensile_strength_list = []
        for moment in self.bending_moment_list:
            tensile_strength_list.append(moment*self.max_y/self.moi)
        return tensile_strength_list

######################      Visualization section    ###################
    def visualize_loading(self, path):
        plt.grid()
        plt.title('Loading Distribution',fontsize=20)
        plt.xlabel('Distance (mm)',fontsize=14)
        plt.ylabel('Load (N)',fontsize=14)
        plt.plot(np.array(range(len(self.load_distribution_list)))*self.dx, -1*np.array(self.load_distribution_list))
        plt.savefig(os.path.join(path, 'loading_distribution.png'))
        plt.show()

    def visualize_shear_force(self, path):
        plt.grid()
        plt.title('Shear Force Distribution', fontsize=20)
        plt.xlabel('Distance (mm)',fontsize=14)
        plt.ylabel('Force (N)',fontsize=14)
        plt.plot(np.array(range(len(self.shear_force_list)))*self.dx, np.array(self.shear_force_list))
        plt.savefig(os.path.join(path, 'shear_force.png'))
        plt.show()

    def visualize_bending_moment(self, path):
        plt.grid()
        plt.title('Bending Moment Distribution', fontsize=20)
        plt.xlabel('Distance (mm)',fontsize=14)
        plt.ylabel('Moment (N.mm)',fontsize=14)
        plt.plot(np.array(range(len(self.bending_moment_list)))*self.dx, np.array(self.bending_moment_list))
        plt.savefig(os.path.join(path, 'bending_moment.png'))
        plt.show()

    def visualize_tensile_stress(self,path):
        plt.grid()
        plt.title('Tensile stress Distribution', fontsize=20)
        plt.xlabel('Distance (mm)',fontsize=14)
        plt.ylabel('stress (MPa)',fontsize=14)
        plt.plot(np.array(range(len(self.tensile_stress_list)))*self.dx, np.array(self.tensile_stress_list))
        plt.savefig(os.path.join(path,'tensile_stress.png'))
        plt.show()

    def visualize_shear_stress(self,path):
        plt.grid()
        plt.title('Max Shear stress Distribution', fontsize=20)
        plt.xlabel('Distance (mm)',fontsize=14)
        plt.ylabel('stress (MPa)',fontsize=14)
        plt.plot(np.array(range(len(self.shear_stress_list)))*self.dx, np.array(self.shear_stress_list))
        plt.savefig(os.path.join(path,'shear_stress.png'))
        plt.show()