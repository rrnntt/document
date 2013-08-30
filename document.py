import rect
from rect import Rect, Point

default_styles = {'body': 
                                {'font-family': 'times', 
                                 'font-style': '', 
                                 'font-size': 12},
                  
                  'title':       {'font-style': 'B', 
                                  'font-size': 16},
                  
                  'symbol':      {'font-family': 'math-symbol'},
                  
                  'math-var':    {'font-family': 'math-var'},
                  
                  'math-symbol': {'font-family': 'math-symbol'},
                  'math-fun':    {'font-family': 'math-symbol'},
                  }

textAlignments = {'j': rect.justifyX,
                  'l': rect.alignLeft,
                  'r': rect.alignRight,
                  'c': rect.center,
                 }

""""Empirically found fraction of font's height from the top which defines
character's baseline"""
pdf_baseline = 0.81

#---------------------------------------------------------------------------------
class DocItem(object):
    """An item of a document."""
    def __init__(self):
        self.text = ''
    
    def scaleFont(self,factor):
        """Scale font size by a factor"""
        if hasattr(self,'style'): # not all of them may have style
            if isinstance(self.style,tuple):
                self.style = self.style[0],factor
            else:
                self.style = (self.style,factor)
                
    def showRect(self,pdf):
        pdf.rect(self.rect.x0(), self.rect.y0(), self.rect.width(), self.rect.height(), 'B')

#---------------------------------------------------------------------------------
class MultiItem(DocItem):
    """A complex item containing other items."""
    def __init__(self):
        DocItem.__init__(self)
        self.items = []
        # pointer to the local styles dict
        self.styles = default_styles
        self.style = ('body',1)
        # left and top inner margins
        self.margins = Point(0,0)
        
    def appendItem(self, item):
        """Append a child document item."""
        self.items.append(item)
        
    def refit(self):
        """Refit all the children items so that they are all inside (if possible) of this MultiItem's rect.
        
        This method is supposed to be called after rect of this item has been moved by an outside object
        (a parent of this item for example). Other objects mustn't (shouldn't?) resize this rect however.
        Although I don't know how to enforce it in python.
        
        This method moves children's rects and refits them. 
        """
        old_rect = self.getUnionRect()
        dp = self.rect.p0() - old_rect.p0() + self.margins
        for item in self.items:
            if item:
                item.rect.translate(dp)
                item.refit()
                
    def moveTo(self,x,y):
        """Moves this multi-item to point with coordinates x,y."""
        self.rect.moveTo(Point(x,y))
        self.refit()
                
    def getUnionRect(self):
        """Create a union of all children's rects."""
        rect = Rect()
        for item in self.items:
            if item:
                rect.unite(item.rect)
        return rect
    
    def cellPDF(self, pdf, r = None):
        """Output the item to PDF"""
        style = self.style
        for item in self.items:
            if item:
                if item.style != style:
                    style = item.style
                    self.setFontPDF(pdf, item)
                item.cellPDF(pdf, r)
                
    def scaleFont(self,factor):
        """Scale font size by a factor"""
        self.style = self.style[0],factor
        for item in self.items:
            if item:
                item.scaleFont(factor)
                
    def setFontPDF(self,pdf,item):
        setFontPDF(pdf,item.style, self.styles)

    def resizeItemsPDF(self,pdf, x, y):
        """Resize all items with origin at x,y"""
        for item in self.items:
            if item:
                self.setFontPDF(pdf, item)
                item.resizePDF(pdf, x, y)
                
    def getLineHeight(self, pdf):
        return pdf.font_size_pt / pdf.k
    
    def addItems(self, *items):
        for item in items:
            self.appendItem(item)
