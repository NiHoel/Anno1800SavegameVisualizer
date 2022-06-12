from . import *
    
def scale(im, nR, nC):
    nR0 = len(im)     # source number of self.rows 
    nC0 = len(im[0])  # source number of columns 
    return [[ im[int(nR0 * r / nR)][int(nC0 * c / nC)]  
             for c in range(nC)] for r in range(nR)]

def draw(area, scaling_factor = 2) :
    a = np.uint8(np.clip(scale(np.transpose(area),scaling_factor*len(area),scaling_factor*len(area[0])) , 0, 255))
    image_data = io.BytesIO()
    PIL.Image.fromarray(a).save(image_data, "png")
    IPython.display.display(IPython.display.Image(data=image_data.getvalue()))

#print("Setup completed")