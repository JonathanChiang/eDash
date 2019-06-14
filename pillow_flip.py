from PIL import Image
import glob
import os

def rotate(image_path, degrees_to_rotate, saved_location):
    """
    Rotate the given photo the amount of given degrees, show it and save it

    @param image_path: The path to the image to edit
    @param degrees_to_rotate: The number of degrees to rotate the image
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    rotated_image = image_obj.rotate(degrees_to_rotate)
    name_directory =  saved_location + "test" + ".png"
    rotated_image.save(name_directory)


def directory_flip(directory, out):
    list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(directory))]
    for filename in list_of_images:
        im=Image.open(directory + filename)
        im_rotate=im.rotate(180)
        im_rotate.save(out + 'rotated_' + filename)


if __name__ == '__main__':
    #image = '/Users/jonc101/Desktop/input/brain.png'
    #rotate(image, 180, '/Users/jonc101/Desktop/')
    #rotate(image, 180, '/Users/jonc101/Desktop/out')
    directory_flip('/Users/jonc101/Desktop/input/', '/Users/jonc101/Desktop/out/')
