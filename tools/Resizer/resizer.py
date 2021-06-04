'''
    Program used to resize bmp images
'''

#     BMP headers strcucture
#
#           Header
#     # Signature (0-1)
#     # FileSize (2-5)
#     # reserved (6-9)
#     # DataOffset (10-13)
#
#           InfoHeader
#     # Size (14-17)
#     # Width (18-21)
#     # Height (22-25)
#     # Planes (26-27)
#     # Bits Per Pixel (28-29)
#     # Compression (30-33)
#     # ImageSize (34-37)
#     # XpixelsPerM (38-41)
#     # YpixelsPerM (42-45)
#     # Colors Used (46-49)
#     # Important Colors (50-53)


def read_int_from_bytes(pos, num_of_bytes, file):
    ''' Reads given number of bytes at a given position,
        and returns corresponding integer '''
    file.seek(pos, 0)
    return int.from_bytes(file.read(num_of_bytes), byteorder='little')

def write_bytes_from_int(pos, num_of_bytes, int_data, destination):
    ''' Writes given number of bytes from an integer
        to a given position of desired file '''
    destination.seek(pos, 0)
    destination.write(
        int(int_data).to_bytes(num_of_bytes, byteorder='little')
    )


def calculate_pixel_colors_bilinear(
        org_row, org_column, delta_row, delta_column, pixel_matrix
    ):
    ''' Function used to calculate pixel`s
        color values based on it`s position
        in the resulting matrix '''

    resulting_pixel = []

    for rgb in range(3):
        # calculate every color value accordingly
        # to original pixel`s neighbors

        last_row_cond = org_row == (len(pixel_matrix) - 1)
        last_column_cond = org_column == (len(pixel_matrix[-1]) - 1)

        if not last_row_cond and not last_column_cond:
            value = int(
                pixel_matrix[org_row+1][org_column+1][rgb]
                * (delta_row)*(delta_column)
                + pixel_matrix[org_row][org_column+1][rgb]
                * (1-delta_row)*(delta_column)
                + pixel_matrix[org_row+1][org_column][rgb]
                * (delta_row)*(1-delta_column)
                + pixel_matrix[org_row][org_column][rgb]
                * (1-delta_row)*(1-delta_column)
            )
        # we have no sample pixels to the right
        elif not last_row_cond:
            value = int(
                pixel_matrix[org_row+1][org_column][rgb]*(delta_row)
                + pixel_matrix[org_row][org_column][rgb]*(1-delta_row)
            )
        # we have no sample pixels above
        elif not last_column_cond:
            value = int(
                pixel_matrix[org_row][org_column+1][rgb]*(delta_column)
                + pixel_matrix[org_row][org_column][rgb]*(1-delta_column)
            )
        # we have no sample pixels literally anywhere
        else:
            value = pixel_matrix[org_row][org_column][rgb]

        resulting_pixel.append(value)

    return resulting_pixel


class Bmp:
    ''' Class with main info about given bmp picture
        and functional to modify it '''
    def __init__(self, my_file):
        ''' Gets info from sample header '''
        my_file.seek(0, 0)
        self.signature          = my_file.read(2)
        self.file_size          = read_int_from_bytes(2, 4, my_file)
        self.reserved           = read_int_from_bytes(6, 4, my_file)
        self.offset             = read_int_from_bytes(10, 4, my_file)
        self.size               = read_int_from_bytes(14, 4, my_file)
        self.width              = read_int_from_bytes(18, 4, my_file)
        self.height             = read_int_from_bytes(22, 4, my_file)
        self.planes             = read_int_from_bytes(26, 2, my_file)
        self.bits_per_pixel     = read_int_from_bytes(28, 2, my_file)
        self.compression        = read_int_from_bytes(30, 4, my_file)
        self.image_size         = read_int_from_bytes(34, 4, my_file)
        self.x_pixels_per_m     = read_int_from_bytes(38, 4, my_file)
        self.y_pixels_per_m     = read_int_from_bytes(42, 4, my_file)
        self.colors_used        = read_int_from_bytes(46, 4, my_file)
        self.important_colors   = read_int_from_bytes(50, 4, my_file)
        self.color_table        = my_file.read(self.offset - 54)
        self.matrix             = self.form_pixel_matrix(my_file)

    def form_pixel_matrix(self, my_file):
        ''' Forms matrix of bytearrays,
            every bytearray is a pixel in BGR format '''
        my_file.seek(self.offset, 0)
        result = []

        for i in range(self.height):
            result.append([])
            for j in range(self.width):
                result[i].append(bytearray(my_file.read(3)))

        return result

    def update_header(self, new_width, new_height, new_pixel_matrix):
        ''' Updates some Bmp object`s fields
            to actual values '''

        self.file_size = self.file_size\
            + 3*(new_width*new_height-self.width*self.height)
        self.width = new_width
        self.height = new_height
        self.matrix = new_pixel_matrix

    def size_down_matrix_simple(self, coef):
        ''' Sizes down pixel matrix,
            by leaving every coeficiental row,
            and every coeficiental element,
            everything else just ignores.
            It gives good enough result
            in a relatively simple algorithm '''

        resized_result = []
        for i in range(self.height):
            if i % coef == 0:
                resized_result.append([])
                for j in range(self.width):
                    if j % coef == 0:
                        resized_result[-1].append(self.matrix[i][j])

        self.update_header(
            new_width=len(resized_result[-1]),
            new_height=len(resized_result),
            new_pixel_matrix=resized_result
        )

    def size_up_matrix_simple(self, coef):
        ''' Sizing up pixel matrix
            by sizing up every single pixel in it
            (nearest neighbor method) '''

        resized_result = []
        for i in range(self.height):
            # for every additional pixel row
            for _ in range(coef):
                resized_result.append([])
                for j in range(self.width):
                    # for every additional pixel
                    for _ in range(coef):
                        # copy pixel from original image
                        resized_result[-1].append(self.matrix[i][j])

        self.update_header(
            new_width=self.width*coef,
            new_height=self.height*coef,
            new_pixel_matrix=resized_result
        )

    def size_up_matrix_bilinear(self, coef):
        ''' Sizing up pixel matrix by
            assuming missing pixels` BGR values,
            based on current pixel`s neighbors
            (bilinear method) '''

        resized_result = []
        for i in range(self.height):
            # arn stands for Additional Row Number
            for arn in range(coef):
                resized_result.append([])
                for j in range(self.width):
                    # acn stands for Additional Column Number
                    for acn in range(coef):
                        resized_result[-1].append(
                            calculate_pixel_colors_bilinear(
                                org_row=i,
                                org_column=j,
                                delta_row=arn/coef,
                                delta_column=acn/coef,
                                pixel_matrix=self.matrix
                            )
                        )

        self.update_header(
            new_width=self.width*coef,
            new_height=self.height*coef,
            new_pixel_matrix=resized_result
        )

    def print_info(self):
        ''' Prints headers into console '''
        print("\n\tHeader")
        print("Signature\t", self.signature)
        print("FileSize\t", self.file_size, "bits")
        print("reserved\t", self.reserved)
        print("DataOffset\t", self.offset)

        print("\n\tInfoHeader")
        print("Size\t\t", self.size)
        print("Width\t\t", self.width)
        print("Height\t\t", self.height)
        print("Bits Per Pixel\t", self.bits_per_pixel)
        print("Compression\t", self.compression)
        print("ImageSize\t", self.image_size)
        print("XpixelsPerM\t", self.x_pixels_per_m)
        print("YpixelsPerM\t", self.y_pixels_per_m)
        print("Colors Used\t", self.colors_used)
        print("Impotant Colors\t", self.important_colors)

    def print_color_table(self):
        ''' Prints colortable into console '''
        print("\n\tColorTable")
        for i in range(int((self.offset-54)/4)):
            print(self.color_table.read(4))

    def print_image(self):
        ''' Prints every pixel`s bytes into console '''
        print("\n\tImage")
        print(self.matrix)

    def write_to_file(self, destination):
        ''' Writes updated image to a new file '''
        # Signature (0-1)
        destination.seek(0, 0)
        destination.write(self.signature)
        # FileSize (2-5)
        write_bytes_from_int(2, 4, self.file_size, destination)
        # reserved (6-9)
        write_bytes_from_int(6, 4, self.reserved, destination)
        # DataOffset (10-13)
        write_bytes_from_int(10, 4, self.offset, destination)
        # Size (of info header) (14-17), defaults to 40
        write_bytes_from_int(14, 4, 40, destination)
        # Width (18-21)
        write_bytes_from_int(18, 4, self.width, destination)
        # Height (22-25)
        write_bytes_from_int(22, 4, self.height, destination)
        # Planes (26-27)
        write_bytes_from_int(26, 2, self.planes, destination)
        # Bits Per Pixel (28-29)
        write_bytes_from_int(28, 2, self.bits_per_pixel, destination)
        # Compression (30-33), as we don`t compress our images it`s 0
        write_bytes_from_int(30, 4, 0, destination)
        # (compressed) ImageSize (34-37), defaults to 0
        write_bytes_from_int(34, 4, 0, destination)
        # XpixelsPerM (38-41)
        write_bytes_from_int(38, 4, self.x_pixels_per_m, destination)
        # YpixelsPerM (42-45)
        write_bytes_from_int(42, 4, self.y_pixels_per_m, destination)
        # Colors Used (46-49)
        write_bytes_from_int(46, 4, self.colors_used, destination)
        # Important Colors (50-53)
        write_bytes_from_int(50, 4, self.important_colors, destination)
        # Color Map (54-end_of_offset)
        destination.seek(54, 0)
        destination.write(self.color_table)

        destination.seek(self.offset, 0)
        for row in self.matrix:
            for pixel in row:
                destination.write(bytearray(pixel))
            # compensate bmp pixels shift
            for _ in range(len(row) % 4):
                destination.write(int(0).to_bytes(1, byteorder='little'))


# main resizing function
def resize_image(
    file_bmp=open("./test.bmp", "rb+"), coef=1, method="pixel"
):
    ''' Resizes image based on given
        image, coefficient, and method '''

    picture = Bmp(file_bmp)

    if coef >= 1:
        if method == "bilinear":
            picture.size_up_matrix_bilinear(coef)
        else:
            picture.size_up_matrix_simple(coef)
    elif coef > 0:
        picture.size_down_matrix_simple(round(1/coef))
    else:
        print("Invalid scale factor")
        return


    with open("./newimage.bmp", "wb+") as resulting_file:
        picture.write_to_file(
            resulting_file
        )

        print("\nResulting image:")
        Bmp(resulting_file).print_info()


# execution
if __name__ == '__main__':
    with open("./test.bmp", "rb+") as input_image_file:
        resize_image(input_image_file, 2, "bilinear")
