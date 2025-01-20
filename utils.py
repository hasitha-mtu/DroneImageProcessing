import glob

def get_image_list(dir_path):
    image_paths = glob.glob(f"{dir_path}/*.JPG")
    print(f'get_image_list|image_paths : {image_paths}')
    image_files = []
    for image_path in image_paths:
        image = ('images', (image_path, open(image_path, 'rb'), 'image/jpg'))
        image_files.append(image)
    return image_files

if __name__ == "__main__":
    pass
