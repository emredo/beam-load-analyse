import os.path
import numpy as np
import matplotlib.pyplot as plt
from moi import CalculateMoi

class Load(object):
    def __init__(self, x_start, x_end, a, b, c):
        self.x_start = x_start
        self.x_end = x_end
        self.a = a
        self.b = b
        self.c = c
        self.dx = 0.1
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
            # distribution.append(self.function(x+self.dx))
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

class Beam(object):
    def __init__(self, loading_list, length, section_type):
        self.loading_list = loading_list
        self.dx = loading_list[0].dx
        self.length = length
        self.section_type = section_type
        self.moi_calculations = CalculateMoi(self.section_type)
        self.moi = self.moi_calculations.moi
        self.max_y = self.moi_calculations.max_y
        self.section_area = self.moi_calculations.section_area
        self.qx = self.moi_calculations.qx
        self.reaction_x, self.reaction_y, self.reaction_moment = self.calculate_reactions()
        self.load_distribution_list = self.load_distribution()
        self.shear_force_list = self.shear_force_distribution()
        self.bending_moment_list = self.bending_moment_distribution()
        self.tensile_strength_list = self.tensile_strength_distribution()
        self.shear_strength_list = self.shear_strength_distribution()
        self.max_normal_stress = max(self.bending_moment_list)*self.max_y/self.moi

    def calculate_reactions(self):
        reaction_x = 0
        reaction_y = 0
        moment = 0
        for loading_obj in self.loading_list:
            reaction_y -= loading_obj.area
            moment -= loading_obj.centroid * loading_obj.area
        return reaction_x, reaction_y, moment

    def load_distribution(self):
        load_list = (self.length * int(1 / self.dx) + 1) * [0]
        for loading_obj in self.loading_list:
            x = loading_obj.x_start * int(1 / self.dx)
            for diff_load in loading_obj.distribution:
                load_list[x] = diff_load
                x += 1
        return load_list

    def shear_force_distribution(self):
        shear_force_list = []
        shear_force = self.reaction_y
        for force in self.load_distribution_list:
            shear_force_list.append(shear_force)
            shear_force += (force*self.dx)
        return shear_force_list

    def bending_moment_distribution(self):
        bending_moment_list = []
        bending_moment = self.reaction_moment
        for shear_force in self.shear_force_list:
            bending_moment_list.append(bending_moment)
            bending_moment -= (shear_force*self.dx)
        return bending_moment_list

    def shear_strength_distribution(self):
        shear_strength_list = []
        for shear_force in self.shear_force_list:
            shear_strength_list.append((shear_force*self.qx)/(self.moi*self.max_y))
        return shear_strength_list

    def tensile_strength_distribution(self):
        tensile_strength_list = []
        for moment in self.bending_moment_list:
            tensile_strength_list.append(moment*self.max_y/self.moi)
        return tensile_strength_list

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
        plt.plot(np.array(range(len(self.shear_force_list)))/100, np.array(self.shear_force_list))
        plt.savefig(os.path.join(path, 'shear_force.png'))
        plt.show()

    def visualize_bending_moment(self, path):
        plt.grid()
        plt.title('Bending Moment Distribution', fontsize=20)
        plt.xlabel('Distance (mm)',fontsize=14)
        plt.ylabel('Moment (N.mm)',fontsize=14)
        plt.plot(np.array(range(len(self.bending_moment_list)))/100, -1*np.array(self.bending_moment_list))
        plt.savefig(os.path.join(path, 'bending_moment.png'))
        plt.show()

    def visualize_tensile_strength(self,path):
        plt.grid()
        plt.title('Tensile Strength Distribution', fontsize=20)
        plt.xlabel('Distance (mm)',fontsize=14)
        plt.ylabel('Strength (MPa)',fontsize=14)
        plt.plot(np.array(range(len(self.tensile_strength_list))), np.array(self.tensile_strength_list))
        plt.savefig(os.path.join(path,'tensile_strength.png'))
        plt.show()

    def visualize_shear_strength(self,path):
        plt.grid()
        plt.title('Max Shear Strength Distribution', fontsize=20)
        plt.xlabel('Distance (mm)',fontsize=14)
        plt.ylabel('Strength (MPa)',fontsize=14)
        plt.plot(np.array(range(len(self.shear_strength_list))), np.array(self.shear_strength_list))
        plt.savefig(os.path.join(path,'shear_strength.png'))
        plt.show()