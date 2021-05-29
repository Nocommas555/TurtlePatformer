import os

#           Header
#     # Signature (0-1)
#     # FileSize (2-5)
#     # reserved (6-9)
#     # DataOffset (10-13)

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


''' Define some functions '''
def read_int_from_bytes(pos, num_of_bytes, file):
    file.seek(pos, 0)
    return int.from_bytes(file.read(num_of_bytes), byteorder='little')

class HeaderBmp:
    def __init__(self, my_file):
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

    def print_info(self):
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
        print("Compression\t", self.compression )
        print("ImageSize\t", self.image_size)
        print("XpixelsPerM\t", self.x_pixels_per_m)
        print("YpixelsPerM\t", self.y_pixels_per_m)
        print("Colors Used\t", self.colors_used)
        print("Impotant Colors\t", self.important_colors)

    def print_color_table(self):
        print("\n\tColorTable")
        my_file.seek(54)
        for i in range(int((self.offset-54)/4)):
            print(my_file.read(4))

    def print_image(self):
        print("\n\tImage")
        my_file.seek(self.offset)
        for i in range(4):
            print(i+1,"row")
            for j in range(self.width):
                print(my_file.read(3))


def write_bytes_from_int(pos, num_of_bytes, int_data, destination):
    destination.seek(pos, 0)
    destination.write(
        int(int_data).to_bytes(num_of_bytes, byteorder='little')
    )

def write_header(source, destination, new_width, new_height):
    sample = HeaderBmp(source)

    # Signature (0-1)
    destination.seek(0, 0)
    destination.write(sample.signature)
    # FileSize (2-5)
    destination.write(
        int(
            sample.file_size
            - 3*(sample.width*sample.height-new_height*new_width)
        ).to_bytes(4, byteorder='little')
    )
    '''write_bytes_from_int(
        pos=2,
        num_of_bytes=4,
        int_data=sample.file_size
        - 3*(sample.width*sample.height-new_height*new_width),
        destination=destination
    )'''
    # reserved (6-9)
    write_bytes_from_int(6, 4, sample.reserved, destination)
    # DataOffset (10-13)
    write_bytes_from_int(10, 4, sample.offset, destination)
    # Size (of info header) (14-17), defaults to 40
    write_bytes_from_int(14, 4, 40, destination)
    # Width (18-21)
    write_bytes_from_int(18, 4, new_width, destination)
    # Height (22-25)
    write_bytes_from_int(22, 4, new_height, destination)
    # Planes (26-27)
    write_bytes_from_int(26, 2, sample.planes, destination)
    # Bits Per Pixel (28-29)
    write_bytes_from_int(28, 2, sample.bits_per_pixel, destination)
    # Compression (30-33)
    write_bytes_from_int(30, 4, sample.compression, destination)
    # (compressed) ImageSize (34-37), defaults to 0
    write_bytes_from_int(34, 4, 0, destination)
    # XpixelsPerM (38-41)
    write_bytes_from_int(38, 4, sample.x_pixels_per_m, destination)
    # YpixelsPerM (42-45)
    write_bytes_from_int(42, 4, sample.y_pixels_per_m, destination)
    # Colors Used (46-49)
    write_bytes_from_int(46, 4, sample.colors_used, destination)
    # Important Colors (50-53)
    write_bytes_from_int(50, 4, sample.important_colors, destination)
    # Color Map (54-end_of_offset)
    source.seek(54, 0)
    destination.seek(54, 0)
    destination.write(bytearray(source.read(sample.offset - 54)))

def write_picture_data(pic_matrix, destination):
    offset = read_int_from_bytes(10, 4, destination)

    destination.seek(offset, 0)
    for row in pic_matrix:
        for pixel in row:
            destination.write(bytearray(pixel))


def form_pixel_matrix(picture_bmp):
    offset = read_int_from_bytes(10, 4, my_file)
    org_width = read_int_from_bytes(18, 4, my_file)
    org_height = read_int_from_bytes(22, 4, my_file)

    picture_bmp.seek(offset, 0)
    result = []
    for i in range(org_height):
        result.append([])
        for j in range(org_width):
            result[i].append(bytearray(picture_bmp.read(3)))

    return result


def size_up_matrix_pixelized(source_matrix, coef):
    resized_result = []
    
    for i in range(len(source_matrix)):
        # additional row number
        for rn in range(coef):
            resized_result.append([])
            for j in range(len(source_matrix[-1])):
                # additional column number
                for cn in range(coef):
                    resized_result[-1].append(source_matrix[i][j])
            for k in range(int(len(resized_result[-1])) % 4):
                resized_result[-1][-1].append(0)
    
    return resized_result

def size_up_matrix_bilinear(source_matrix, coef):
    resized_result = []
    
    for i in range(len(source_matrix)):
        # additional row number
        for rn in range(coef):
            resized_result.append([])
            for j in range(len(source_matrix[-1])):
                # additional column number
                for cn in range(coef):
                    resized_result[-1].append([])
                    for rgb in range(3):
                        if i != (len(source_matrix) - 1)\
                        and j != (len(source_matrix[-1]) - 1):
                            value = int(
                                source_matrix[i+1][j+1][rgb]
                                * (rn/coef)*(cn/coef)
                                + source_matrix[i][j+1][rgb]
                                * (1-rn/coef)*(cn/coef)
                                + source_matrix[i+1][j][rgb]
                                * (rn/coef)*(1-cn/coef)
                                + source_matrix[i][j][rgb]
                                * (1-rn/coef)*(1-cn/coef)
                            )
                        elif i != (len(source_matrix) - 1):
                            value = int(
                                source_matrix[i+1][j][rgb]*(rn/coef)
                                + source_matrix[i][j][rgb]*(1-rn/coef)
                            )
                        elif j != (len(source_matrix[-1]) - 1):
                            value = int(
                                source_matrix[i][j+1][rgb]*(cn/coef)
                                + source_matrix[i][j][rgb]*(1-cn/coef)
                            )
                        else:
                            value = source_matrix[i][j][rgb]
                        resized_result[-1][-1].append(
                            value
                        )
            for k in range(int(len(resized_result[-1])) % 4):
                resized_result[-1][-1].append(0)
    
    return resized_result

def size_down_matrix_pixelized(source_matrix, coef):
    org_height = len(source_matrix)
    org_width = len(source_matrix[-1])
    resized_result = []

    for i in range(org_height):
        if i % coef == 0:
            resized_result.append([])
            for j in range(org_width):
                if j % coef == 0:
                    resized_result[-1].append(source_matrix[i][j])
            for k in range(int(len(resized_result[-1])) % 4):
                resized_result[-1][-1].append(0)
    
    return resized_result


def resize_image(
    file_bmp=open("./test.bmp", "rb+"),
    coef=1,
    method="pixel"
):
    resulting_file = open("./newimage.bmp", "wb+")

    head = HeaderBmp(file_bmp)

    # print("\nPrevious image:")
    # head.print_info()

    if coef >= 1:
        if method == "bilinear":
            resized_result = size_up_matrix_bilinear(
                form_pixel_matrix(file_bmp),
                coef
            )
        else:
            resized_result = size_up_matrix_pixelized(
                form_pixel_matrix(file_bmp),
                coef
            )
    elif coef > 0:
        resized_result = size_down_matrix_pixelized(
            form_pixel_matrix(file_bmp),
            round(1/coef)
        )
    else:
        return

    write_header(
        source=file_bmp,
        destination=resulting_file,
        new_width=len(resized_result[0]),
        new_height=len(resized_result)
    )
    write_picture_data(
        pic_matrix=resized_result,
        destination=resulting_file
    )

    print("\nResulting image:")
    res_head = HeaderBmp(resulting_file)
    res_head.print_info()


''' Execution '''
my_file = open("./sample.bmp", "rb+")

resize_image(my_file, 10, "bilinear")