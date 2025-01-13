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
    
    def rec_fn(dir, copy_dir):
        for x in os.scandir(dir):
            if x.is_dir():
                new_dir = os.path.join(copy_dir, x.name)
                os.mkdir(new_dir)

                next_s_dir = os.path.join(dir, x.name)
                next_c_dir = new_dir
    
                rec_fn(next_s_dir, next_c_dir)

            elif x.is_file():
                old_file_path = os.path.join(dir, x.name)
                new_file_path = os.path.join(copy_dir, x.name)
                
                shutil.copy(old_file_path, new_file_path)

    rec_fn("static", "public")


    




main()
