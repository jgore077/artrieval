import json
import os
from PIL import Image,UnidentifiedImageError

class Processor():
  def __init__(self,metadata_path,delete:bool=False,ignore_exception:bool=False):
    self.metadata_path=metadata_path
    with open(metadata_path,'r',encoding='utf-8') as file:
      self.metadata=json.loads(file.read())
    self.integrity(ignore_exception, delete)

  def mutate(self,mutate_function,output_path=None,*args,**kwargs):
    mutate_function(self.metadata,*args,**kwargs)
    if output_path==self.metadata_path:
      raise FileExistsError("Cannot overwrite initial metadata file")
    if output_path:
      with open(output_path,'w',encoding='utf-8') as outputfile:
        outputfile.write(json.dumps(self.metadata,indent=4,ensure_ascii=False))
      
  def iterate(self,iterate_function,*args,**kwargs):
    return iterate_function(self.metadata,*args,**kwargs)

  def validate_image(self, key:str, ignore_exception:bool, delete:bool=False)->bool:
    image_path = self.metadata[key]["file_path"]
    absolute_path = os.path.abspath(image_path)
    if os.path.exists(absolute_path):
      try:
        image = Image.open(absolute_path)
        image.verify()
      except Exception:
        print(f"Image {absolute_path} is corrupted")
        if delete:
          print(f"Deleting image {absolute_path}")
          os.remove(absolute_path)
          print(f"Deleting metadata id: {key}")
          del self.metadata[key]
        elif not ignore_exception:
          raise UnidentifiedImageError()
        return False
    else:
      print(f"Image {absolute_path} does not exist")
      if delete:
        print(f"Deleting metadata id: {key}")
        del self.metadata[key]
      elif not ignore_exception:
        raise FileNotFoundError()
      return False
    return True
    
  def validate_entry(self, key:str, ignore_exception:bool)->bool:
      return True
  
  def integrity(self, ignore_exception=False, delete=False)->bool:
    """
    Verifys the integrity of the metadata file and the images, ensuring that images exist and the images are not corrupted
    
    If ignore_exception=False upon an integrity violation an exception will be thrown. If true the function will return false if the file fails the integrity check or true if passing.
    """
    ret=True
    for key in list(self.metadata.keys()):
      if not self.validate_image(key, ignore_exception, delete):
        ret = False
      if not self.validate_entry(key, ignore_exception):
        ret = False
    return True
