from os.path import dirname, abspath, join
import json
import base64
import bson
from mongoengine import connect
from schema import Micrograph
import matplotlib.pyplot as plt
import io
import PIL

class ImageBrowser(object):
    
    def __init__(self, **kwargs):
        #
        # Connect to db
        plt.gray()
        connect('micrograph_db')
        self.set_current_view(**kwargs)
        return
        
    def show_micrograph(self, open_window=True):
        """Displays the face in the row of 'index'
        
        Parameters
        ---------
        face_index: Integer
            Index of the row in self.data_frame which contains the image to be shown
        """
        current_image_entry = Micrograph.objects.get(
            micrograph_id=self.current_view_indices[self.current_micrograph_index]
        )
        current_image_binary = io.BytesIO(base64.b64decode(current_image_entry['image']))
        current_image = PIL.Image.open(current_image_binary)
        plt.imshow(current_image)
        #
        if open_window:
            plt.show()
        #
        return
        
    def open_image_viewer(self):
        """Create initiates ability to key left and right through the images starting at the first one"""
        #
        def on_keyboard(event):
            #
            if event.key == 'right':
                self.current_micrograph_index = (self.current_micrograph_index + 1)%self.current_view_size
            elif event.key == 'left':
                self.current_micrograph_index = (self.current_micrograph_index - 1)%self.current_view_size
            #
            plt.clf()
            self.show_micrograph(open_window=False)
            plt.draw()
        
        plt.gcf().canvas.mpl_connect('key_press_event', on_keyboard)
        #
        self.show_micrograph(open_window=False)
        plt.show()
        #
        return
        
    def set_current_view(self, **kwargs):
        """Returns a dataframe containing only the rows for which 'criterion' returns True
        
        Parameters
        ----------
        criterion: Function
            A function that accepts an index and row of the dataframe as a named tuple and returns False if the row is filtered out
        
        Returns
        -------
        self.data_frame.iloc[rows_that_pass]: Data Frame
            A data frame object with the same columns, but only those rows for which criterion returns True
        """
        self.current_view_indices = [o['micrograph_id'] for o in Micrograph.objects(**kwargs)]
        self.current_view_size = len(self.current_view_indices)
        self.current_micrograph_index = self.current_view_indices[0]
        return
#


b = ImageBrowser(primary_microconstituent='pearlite')
b.open_image_viewer()