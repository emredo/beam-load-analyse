import math

class CalculateMoi(object):
    def __init__(self, section_type):
        self.type = section_type
        if self.type == 'rectangular':
            self.moi, self.max_y, self.qx, self.section_thickness, self.section_area = self.calculate_rectangular()
        elif self.type == 'circular':
            self.moi, self.max_y, self.qx, self.section_thickness, self.section_area = self.calculate_circular()
        elif self.type == 'i_section':
            self.moi, self.max_y, self.qx, self.section_thickness, self.section_area = self.calculate_i_profile()
        elif self.type == 'h_section':
            self.moi, self.max_y, self.qx, self.section_thickness, self.section_area = self.calculate_h_profile()
        elif self.type == 't_section':
            self.moi, self.max_y, self.qx, self.section_thickness, self.section_area = self.calculate_t_profile()
        else:
            print("Invalid beam type")

    @staticmethod
    def calculate_rectangular():
        a = int(float(input("Enter the 'a' dimension of the beam (long dim) in mm: ")))
        b = int(float(input("Enter the 'b' dimension of the beam (short dim) in mm: ")))
        yx = b/2
        moi = a*(b**3)/12
        max_y = b-yx
        qx = a*(b-yx)*b*0.25
        section_thickness = a
        area = a*b
        return moi, max_y, qx, section_thickness, area

    @staticmethod
    def calculate_circular():
        D = int(float(input("Enter the 'D' diameter of the beam in mm: ")))
        moi = ((D**4)*math.pi)/64
        max_y = D/2
        yx = (2*D)/(3*math.pi)
        area = math.pi*(D**2)/4
        qx = yx*area
        section_thickness = D
        return moi, max_y, qx, section_thickness, area

    @staticmethod
    def calculate_i_profile():
        a = int(float(input("Enter the 'a' dimension of the section in mm:\t")))
        b = int(float(input("Enter the 'b' dimension of the section in mm:\t")))
        c = int(float(input("Enter the 'c' dimension of the section in mm:\t")))
        d = int(float(input("Enter the 'd' dimension of the section in mm:\t")))
        e = int(float(input("Enter the 'e' dimension of the section in mm:\t")))
        f = int(float(input("Enter the 'f' dimension of the section in mm:\t")))
        m = a-c-d
        n = b-e-f
        area = b*c + b*d * m*n
        yg = (b*c*(m+d+c*0.5)+m*n*(d+m*0.5)+d*b*d*0.5)/area
        moi = b*(c**3)/12 + b*c*((a-c*0.5-yg)**2) + n*m**3/12 + m*n*(d+m*0.5-yg)**2 + b*(d**3)/12 + b*d*(d*0.5-yg)**2
        if b - yg > yg:
            max_y = b - yg
        else:
            max_y = yg

        if yg>m+d:
            qx = b*(a-yg)*(a-yg)*0.5
        elif d<yg<m+d:
            qx = b*c*(a-yg-c*0.5)+n*(a-c-yg)*(a-c-yg)*0.5
        elif yg < d:
            qx = b*c*(a-yg-c*0.5) + m*n*(m*0.5+d-yg) + b*(d-yg)*(d-yg)*0.5
        section_thickness = a
        return moi, max_y, qx, section_thickness, area

    @staticmethod
    def calculate_h_profile():
        a= int(float(input("Enter the 'a' dimension of the section in mm:\t")))
        b= int(float(input("Enter the 'b' dimension of the section in mm:\t")))
        c= int(float(input("Enter the 'c' dimension of the section in mm:\t")))
        d= int(float(input("Enter the 'd' dimension of the section in mm:\t")))
        e= int(float(input("Enter the 'e' dimension of the section in mm:\t")))
        f= int(float(input("Enter the 'f' dimension of the section in mm:\t")))
        m = a-c-d
        n = b-e-f

        area = b*(c+d)+(b-e-f)*(a-c-d)
        yg = ((b**2)*(c+d)/2 + (b-e-f)*(a-c-d)*(f+(b-e-f)/2))/area
        ix = (c+d)*(b**3)/12 + b*(c+d)*(b*0.5-yg)**2 + (((b-e-f)**3)*(a-c-d))/12 + (a-c-d)*(b-f-e)*(b*0.5+(b-e-f)*0.5-yg)**2
        xg = ((a**2)*b*0.5 - (a-c-d)*(e+f)*(c+(a-c-d)*0.5))/area
        if b-yg > yg:
            max_y = b-yg
        else:
            max_y = yg

        if yg > n+f:
            qx = (c+d)*(b-yg)*(b-yg)*0.5
        elif f < yg < f+n:
            qx = (c+d)*e*(b-yg) + a*(b-yg-e)*(b-yg-e)*0.5
        elif yg < f:
            qx = (c+d)*e*(b-yg-e*0.5) + a*n*(n*0.5 - yg + f) + (c+d)*(f-yg)*(f-yg)*0.5
        section_thickness = a
        return ix, max_y, qx, section_thickness, area

    @staticmethod
    def calculate_t_profile():
        b = int(float(input("Enter the 'b' dimension of the section in mm:\t")))
        c = int(float(input("Enter the 'c' dimension of the section in mm:\t")))
        d = int(float(input("Enter the 'd' dimension of the section in mm:\t")))
        a = int(float(input("Enter the 'a' dimension of the section in mm:\t")))
        e = int(float(input("Enter the 'e' dimension of the section in mm:\t")))

        area = a*(b-c) + c*e
        yg = (a*(b-c)*(c+(b-c)/2)+c**2*e/2)/area
        moi = (a*(b-c)**3)/12 + a*(b-c)*(c+(b-c)/2-yg)**2 + (e*c**3)/12 + (e*c)*(yg-c*0.5)**2
        if b - yg > yg:
            max_y = b - yg
        else:
            max_y = yg
        if yg >= c:
            qx = a*(b-yg)*(b-yg)*0.5
        else:
            qx = a*(b-c)*(b-yg-(b-c)*0.5) + e*(c-yg)*(c-yg)*0.5
        section_thickness = e
        return moi, max_y, qx, section_thickness, area