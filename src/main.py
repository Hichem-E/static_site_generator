from textnode import TextNode, TextType
from htmlnode import HTMLNODE
from leafnode import LeafNode
from parentnode import ParentNode
import shutil
import os

# print("Hello world")

def main():  
    
    if os.path.exists("public/"):
        shutil.rmtree("public")
    os.makedirs("public/", exist_ok=True)

    def file_copy(directory):
        walk = os.walk(directory)
        for root, dirs, files in walk:
            print("root is", root, "here are dirs", dirs, "here are files", files)
            break


    # for x in os.scandir('static'):
    #     if x.is_dir():
    #         print(x.name, "is a directory!")
    #         new_dir = os.path.join('public/', x.name)
    #         os.mkdir(new_dir)
    #     if x.is_file():
    #         print(x.name, "is a file!")
            
    #         shutil.copy('static/'+x.name, 'public/'+x.name)

        

            
            
    
    
    def rec_fn(dir, copy_dir):
        for x in os.scandir(dir):
            if x.is_dir():
                new_dir = os.path.join(copy_dir, x.name)
                os.mkdir(new_dir)

                next_s_dir = os.path.join(dir, x.name)
                next_c_dir = new_dir
    
                rec_fn(next_s_dir, next_c_dir)

            elif x.is_file():
                new_file_path = os.path.join(copy_dir, x.name)
                shutil.copy(dir+x.name, copy_dir+x.name)

    rec_fn("static", "public")


    




main()
