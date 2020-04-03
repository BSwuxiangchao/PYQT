import win32print
import win32ui
from PIL import Image,ImageWin



class printer_helper:
    HORZSIZE    =  4     # Horizontal size in millimeters   
    VERTSIZE    =  6     # Vertical size in millimeters     
    HORZRES     =  8     # Horizontal width in pixels       
    VERTRES     =  10    # Vertical height in pixels        

    LOGPIXELSX  =  88    # Logical pixels/inch in X         
    LOGPIXELSY  =  90    # Logical pixels/inch in Y         


    PHYSICALWIDTH   = 110 # Physical Width in device units  
    PHYSICALHEIGHT  = 111 # Physical Height in device units 
    PHYSICALOFFSETX = 112 # Physical Printable Area x margin
    PHYSICALOFFSETY = 113 # Physical Printable Area y margin
    printable_area = 0,0
    total_area     = 0,0
    ppi            = 0,0
    
    def __init__(self):
        self.hDC=win32ui.CreateDC ()
        print("Pritner Helper")
        
    def get_printers(self):
        return win32print.EnumPrinters(2)
    
    def get_default_printer(self):
        return win32print.GetDefaultPrinter()
      
    def get_printable_area(self):
        self.printable_area = self.hDC.GetDeviceCaps(self.HORZRES), self.hDC.GetDeviceCaps(self.VERTRES)
        return self.printable_area
        
        
    def get_total_area(self):
        self.total_area=self.hDC.GetDeviceCaps(self.PHYSICALWIDTH),self.hDC.GetDeviceCaps(self.PHYSICALHEIGHT) 
        return self.total_area
    
    def get_ppi(self):
        self.ppi=self.hDC.GetDeviceCaps(self.LOGPIXELSX),self.hDC.GetDeviceCaps(self.LOGPIXELSY)
        return self.ppi

    def get_margin(self):
        self.margin=self.hDC.GetDeviceCaps(self.PHYSICALOFFSETX),self.hDC.GetDeviceCaps(self.PHYSICALOFFSETY)
        return self.margin
        
    def open_printer(self,name):
        self.hDC.CreatePrinterDC(name)
        self.get_printable_area()
        self.get_total_area()
        self.get_ppi()
                
    def mm_to_pixel(self,size_mm,ind):
        return int(size_mm*self.ppi[ind]/25.4)            
    
    def pixel_to_mm(self,size_pix,ind):
        return size_pix*25.4/self.ppi[ind]      

    def do_printer(self,filepath,print_x_mm,print_y_mm,print_w_mm,print_h_mm):
        """
        if (self.mm_to_pixel(print_w_mm,0)>self.printable_area[0])|(self.mm_to_pixel(print_h_mm,1)>self.printable_area[1]):
            print(self.mm_to_pixel(print_w_mm,0),self.printable_area[0])
            print(self.mm_to_pixel(print_h_mm,1),self.printable_area[1])
            print("Error print size")        
            return False
        """
    
        bmp = Image.open (filepath)
        bmp_width  = bmp.size[0]
        bmp_height = bmp.size[1]
        print("Image size(mm): ",self.pixel_to_mm(bmp_width,0),'*',self.pixel_to_mm(bmp_height,1))
    
        ratios = [1.0 * self.mm_to_pixel(print_w_mm,0) / bmp_width, 1.0 * self.mm_to_pixel(print_h_mm,1)/ bmp_height]
        scale = min(ratios)
        #print(m_HORZRES-printer_margins[0] ,bmp.size[0],m_VERTRES ,bmp.size[1])
        print("ratios",ratios,"scale",scale)

        self.hDC.StartDoc (filepath)
        self.hDC.StartPage ()
        dib = ImageWin.Dib (bmp)
        scaled_width = int (scale * bmp_width)
        scaled_height = int (scale * bmp_height)
        print("scaled_width(mm)",self.pixel_to_mm(scaled_width,0),"scaled_height(mm)", self.pixel_to_mm(scaled_height,1))
    
        offset_x =self.mm_to_pixel(print_x_mm,0)
        offset_y =self.mm_to_pixel(print_y_mm,1)
        
        x1 = int ((self.mm_to_pixel(print_w_mm,0) - scaled_width) / 2)+offset_x
        y1 = int ((self.mm_to_pixel(print_h_mm,0) - scaled_height) / 2)+offset_y
        x2 = x1 + scaled_width+offset_x
        y2 = y1 + scaled_height+offset_y
        print('x1(mm):',self.pixel_to_mm(x1,0),'y1(mm):',self.pixel_to_mm(y1,1))
        print('x2(mm):',self.pixel_to_mm(x2,0),'y2(mm):',self.pixel_to_mm(y2,1))
        
        #return 0
        dib.draw (self.hDC.GetHandleOutput (), (x1, y1, x2, y2))

        self.hDC.EndPage ()
        self.hDC.EndDoc ()     
        print("Print Finish")
    
    
#printer=printer_helper()
#print(printer.get_printers())



