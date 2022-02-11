import os

class PPM_HDA:
    def __init__(self, name, hda_file_name, min_inputs, description, version):        
        self.name = name
        self.hda_file_name = hda_file_name # has to be the full path to where the file will be saved
        self.description = description
        self.min_inputs = min_inputs
        self.version = version
        
    
    def convert_to_hda(self, node):
        print("Saving OTL with name: {}, on path: {}".format(self.name, self.hda_file_name))
        
        node.createDigitalAsset(name=None, 
                                hda_file_name=self.hda_file_name, 
                                description=self.description, 
                                min_num_inputs=self.min_inputs, 
                                max_num_inputs=0, 
                                compress_contents=False, 
                                comment=None, 
                                version=self.version, 
                                save_as_embedded=False, 
                                ignore_external_references=False, 
                                change_node_type=True, 
                                create_backup=True, 
                                install_path=None
                                )
        
        """node.createDigitalAsset( 
                                hda_file_name=path, 
                                description=description, 
                                min_num_inputs=inputs,    
                                version=version
                                )
        """
        
        
        