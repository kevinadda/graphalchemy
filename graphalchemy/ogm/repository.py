


class Repository(object):
    
    def __init__(self, client, model, class_, logger=None):
        self.client = client
        self.model = model
        self.class_ = class_
        self.logger = logger
        
        
    def get(self, id):
        # Retrieve from DB
        response = self.client.get_vertex(id)
        results = response.content['results']
        
        # Verify type
        type = results.pop('type')
        if type != 'vertex' and model.is_node() == False:
            raise Exception('Expected vertex, got '+str(type))
        elif type != 'edge' and model.is_relationship() == False:
            raise Exception('Expected edge, got '+str(type))
        else:
            raise Exception('Unknown type '+str(type))
        
        # Verify id
        _id = results.pop('_id')
        if _id != id:
            raise Exception('Expected '+str(id)+', got '+str(_id))
        
        # Build object
        obj = self.class_()
        for property_db, value_db in results.iteritems():
            found = False
            for property in self.model.properties:
                if property.name_db != property_db:
                    continue
                found = True
                break
            if not found:
                raise Exception('Property retrieved but not found : '+property_db)
            value_py = property.coerce_to_py(value_db)
            setattr(obj, property.name_py, value_py)
            
        
        # Add to the entity map
        id = response.content['results']['_id']
        self.identity_map[obj] = InstanceState(obj)
        self.identity_map[obj].update_id(id)
        self.identity_map[obj].update_attributes(data)
        
        return initialize_element(self.client, resp.results)