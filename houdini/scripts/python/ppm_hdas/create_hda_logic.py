import os

class PPM_HDA:
    def __init__(self, name, hda_file_name, description, version):
        self.name = name
        self.hda_file_name = hda_file_name # has to be the full path to where the file will be saved
        self.description = description
        self.version = version
        
    
    def convert_to_hda(self, node):
        node.createDigitalAsset(name=self.name, 
                                hda_file_name=self.hda_file_name, 
                                description=self.description, 
                                min_num_inputs=0, 
                                max_num_inputs=0, 
                                compress_contents=False, 
                                comment=None, 
                                version=self.version = version, 
                                save_as_embedded=False, 
                                ignore_external_references=False, 
                                change_node_type=True, 
                                create_backup=True, 
                                install_path=None)
        
        
        