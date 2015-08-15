from numpy import linspace, interp, sqrt, loadtxt
import sys
import operator


def data_sort(x, y):
    data = []
    x_new = []
    y_new = []
    for i in range (0, len(x)):
        data.append([x[i], y[i]])

    sort = sorted(data, key=lambda l:l[0])
    for i in range (0, len(sort)):
        x_new.append(sort[i][0])
        y_new.append(sort[i][1])

    print len(y)

    return list(x_new), list(y_new)

def get_cell_param(filename, cell_area = 0.25):
    
    try:
        x = loadtxt(filename, usecols=(0,))
        y = loadtxt(filename, usecols=(1,))
        x, y = data_sort(x, y)
        cell = DataRip(x, y, cell_area)
    except ValueError:
        return None

    return cell

class DataRip:

    def __init__(self, x, y, area):
        area = float(area/1000)
        self.x = x
        self.y = [l / area for l in y]
        self.n = 1000

    def extract_jsc(self):
        x = self.x
        y = self.y
        xvals = linspace(min(x), max(x), self.n)
        yinterp = interp(xvals, x, y)
        minx = min(list(xvals), key=lambda x:abs(x))
        jsc = yinterp[list(xvals).index(minx)]
        return sqrt(jsc**2) 

    def extract_voc(self):
        x = self.x
        y = self.y
        yvals = linspace(min(y), max(y), self.n)
        xinterp = interp(yvals, y, x)
        miny= min(list(yvals), key=lambda x:abs(sqrt(x**2)))
        voc = xinterp[list(yvals).index(miny)]
        return voc 

    def max_power(self):
        x = self.x
        y = self.y
        xvals = linspace(min(x), max(x), self.n)
        yinterp = interp(xvals, x, y)
        power = sqrt((xvals*yinterp)**2)
        lst1 = list(power[:int(len(power)/2)])
        lst2 = list(power[int(len(power)/2)+100:])
        p1 = lst1.index(min(lst1))
        p2 = lst2.index(min(lst2))+p1
        if p1 == p2:
            jmp = 0
            vmp = 0
            return jmp, vmp
        else:
            index=list(power).index(max(power[p1:p2]))
            jmp = yinterp[index]
            vmp = xvals[index]
            return jmp, vmp

    def extract_ff(self):
        jmp, vmp = self.max_power()
        jsc = self.extract_jsc()
        voc = self.extract_voc()
        ff = (jmp*vmp)/(jsc*voc)*100
        return sqrt(ff**2)

    def extract_eff(self):
        jsc = self.extract_jsc()
        voc = self.extract_voc()
        ff = self.extract_ff()
        eff = sqrt(((jsc*1e-3*voc*ff)/100e-3)**2)
        return eff

if __name__ == "__main__":
    cell = get_cell_param(sys.argv[1], float(sys.argv[2]))
    print 'Jsc = %s maA/cm^2' % (cell.extract_jsc())
    print 'Voc = %s V' % (cell.extract_voc())
    print 'FF = %s pc' % (cell.extract_ff())
    print 'Eff = %s pc' % (cell.extract_eff())
