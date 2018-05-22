import os
from collections import OrderedDict


class ParserBMP():
    def __init__(self, file):
        self.file = file
        self.data = OrderedDict({})

    def get_data_about_bmp(self):
        self.data.update(self.get_path_bmp_file())
        self.data.update(self.get_filename())
        self.data.update(self.__get_file_header_data())
        self.data.update(self.__get_bitmap_header_data())

        return self.data

    def get_path_bmp_file(self):
        return OrderedDict({'Path': os.path.dirname(os.path.realpath(self.file))})

    def get_filename(self):
        return OrderedDict({'Filename': os.path.splitext(os.path.basename(self.file))[0]})

    def __get_file_header_data(self):
        result = OrderedDict({})

        with open(self.file, 'rb') as f:
            file_header = f.read(14)

            if os.path.splitext(os.path.basename(self.file))[1] == '.rle':
                return result
            else:
                try:
                    signature = file_header[0:2].decode('ascii')

                except UnicodeDecodeError:
                    print('File is not bmp! Please, check the input data')

                else:
                    result.update({'Signature': signature,
                                   'File size': int.from_bytes(file_header[2:6], byteorder='little'),
                                   'Reserved bytes': int.from_bytes(file_header[6:10], byteorder='little'),
                                   'Offset': int.from_bytes(file_header[10:14], byteorder='little')})
                    return result

    def __get_bitmap_header_data(self):
        result = OrderedDict({})

        with open(self.file, 'rb') as f:
            header = f.read()
            length_header = int.from_bytes(header[14:18], byteorder='little')
            result.update({'Header length': length_header})

            if length_header == 12:
                result.update({'File version': 'CORE'})
                result.update(self.__get_data_core(header))
            elif length_header == 40:
                result.update({'File version': 'Windows V3'})
                result.update(self.__get_data_windows_v3(header))
            elif length_header == 108:
                result.update({'File version': 'Windows V4'})
                result.update(self.__get_data_windows_v4(header))
            elif length_header == 124:
                result.update({'File version': 'Windows V5'})
                result.update(self.__get_data_windows_v5(header))

        return result

    def __get_data_core(self, header):
        return OrderedDict({
            'Width': int.from_bytes(header[18:20], byteorder='little'),
            'Height': int.from_bytes(header[20:22], byteorder='little'),
            'Planes': int.from_bytes(header[22:24], byteorder='little'),
            'Count bits': int.from_bytes(header[24:26], byteorder='little')
        })

    def __get_data_windows_v3(self, header):
        return OrderedDict({
            'Width': int.from_bytes(header[18:22], byteorder='little'),
            'Height': int.from_bytes(header[22:26], byteorder='little'),
            'Planes': int.from_bytes(header[26:28], byteorder='little'),
            'Count bits': int.from_bytes(header[28:30], byteorder='little'),
            'Compression': int.from_bytes(header[30:34], byteorder='little'),
            'Size image': int.from_bytes(header[34:38], byteorder='little'),
            'Horizontal pixels per meter': int.from_bytes(header[38:42], byteorder='little'),
            'Vertical pixels per meter': int.from_bytes(header[42:46], byteorder='little'),
            'Count colors': int.from_bytes(header[46:50], byteorder='little'),
            'Count important colors': int.from_bytes(header[50:54], byteorder='little')
        })

    def __get_data_windows_v4(self, header):
        data_v4 = self.__get_data_windows_v3(header)
        data_v4.update({
            'Red mask': int.from_bytes(header[54:58], byteorder='little'),
            'Green mask': int.from_bytes(header[58:62], byteorder='little'),
            'Blue mask': int.from_bytes(header[62:66], byteorder='little'),
            'Alpha mask': int.from_bytes(header[66:70], byteorder='little'),
            'Color space type': header[70:74].decode('utf-8')[::-1]
        })
        if data_v4['Color space type'] == 0:
            data_v4.update({
                'End points': int.from_bytes(header[74:110], byteorder='little'),
                'Gamma Red': int.from_bytes(header[110:114], byteorder='little'),
                'Gamma Green': int.from_bytes(header[114:118], byteorder='little'),
                'Gamma Blue': int.from_bytes(header[118:122], byteorder='little')
            })
        return data_v4

    def __get_data_windows_v5(self, header):
        data_v5 = self.__get_data_windows_v4(header)
        data_v5.update({
            'Intent': int.from_bytes(header[122:126], byteorder='little'),
            'Profile data': int.from_bytes(header[126:130], byteorder='little'),
            'Profile size': int.from_bytes(header[130:134], byteorder='little'),
            'Reserved': int.from_bytes(header[134:138], byteorder='little'),
        })
        return data_v5

    @staticmethod
    def get_bytes_image(file):
        with open(file, "rb") as f:
            f.seek(138)  # 138 is the offset!
            info_image = f.read()
        return info_image



