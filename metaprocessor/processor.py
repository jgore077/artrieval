import json
import os
from PIL import Image,UnidentifiedImageError

class Processor():
  def __init__(self,metadata_path):
    self.metadata_path=metadata_path
    with open(metadata_path,'r',encoding='utf-8') as file:
      self.metadata=json.loads(file.read())

  def mutate(self,mutate_function,output_path,*args,**kwargs):
    mutate_function(self.metadata,*args,**kwargs)
    if output_path==self.metadata_path:
      raise FileExistsError("Cannot overwrite initial metadata file")
    with open(output_path,'w',encoding='utf-8') as outputfile:
      outputfile.write(json.dumps(self.metadata,indent=4,ensure_ascii=False))
      
  def iterate(self,iterate_function,*args,**kwargs):
    return iterate_function(self.metadata,*args,**kwargs)

  def validate_image(self, entry:dict, ignore_exception:bool)->bool:
    image_path = entry['file_path']
    absolute_path = os.path.abspath("../"+image_path)
    if os.path.exists(absolute_path):
      try:
        image = Image.open(absolute_path)
        image.verify()
      except Exception:
        print(f"Image {absolute_path} is corrupted")
        if not ignore_exception:
          raise UnidentifiedImageError()
        return False
    else:
      if not ignore_exception:
        raise FileNotFoundError(f"Image path {absolute_path} does not exist")
      return False
    return True
    
  def validate_metadata(self, entry:dict, ignore_exception:bool)->bool:
      return True
  
  def integrity(self,ignore_exception=False)->bool:
    """
    Verifys the integrity of the metadata file and the images, ensuring that images exist and the images are not corrupted
    
    If ignore_exception=False upon an integrity violation an exception will be thrown. If true the function will return false if the file fails the integrity check or true if passing.
    """
    ret=True
    for entry in self.metadata.values():
      if not self.validate_image(entry, ignore_exception):
        ret = False
      if not self.validate_metadata(entry, ignore_exception):
        ret = False
    return True
