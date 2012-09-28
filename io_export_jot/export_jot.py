#!BPY

import bpy

class BuildJot():
    # Build a jot file.
    
    
    def __init__(self,context, filepath, anim, start, end):
        # Export Jot files(s) to disk.
        self.anim = anim
        self.start = start
        self.end = end
        self.filepath = filepath
        # Open file for writing.
        self.file = open(self.filepath, 'w')
        self.file.write('#jot\n')
        # Loop through the scene and find all meshes
        bpy.ops.object.mode_set(mode='OBJECT');
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                self.texbody(obj)
        # Close the file and finish.
        self.file.close()


    def vertices(self, obj, file=False):
        # Write vertices to file.
        if not file:
            file = self.file
        file.write('      vertices {{ ')
        for vert in obj.data.vertices:
            file.write('{ %s %s %s }' % ( vert.co.x, vert.co.y, vert.co.z ) )
        file.write('  }}\n')


    def faces(self, obj, file=False):
        # Triangulate faces and write to file.
        if not file:
            file = self.file
        file.write('      faces {{ ')
        obj.data.update(calc_tessface=True)
        for tface in obj.data.tessfaces:
            vert_index = tface.vertices
            if len(vert_index) == 3:
                file.write('{ %s %s %s }' % ( vert_index[0], vert_index[1], vert_index[2] ) )
            else:
                file.write('{ %s %s %s }' % ( vert_index[0], vert_index[1], vert_index[2] ) )
                file.write('{ %s %s %s }' % ( vert_index[0], vert_index[2], vert_index[3] ) )
        file.write('  }}\n')


    def creases(self, obj, file=False):
        # Write creased edges to file.
        if not file:
            file = self.file
        file.write('       creases {{ ')
        for edge in obj.data.edges:
            if edge.crease > 0.0:
                file.write('{ %s %s }' % ( edge.vertices[0], edge.vertices[1] ) )
        file.write('  }}\n')


    def uvs(self, obj, file=False):
        # Write UV's to file.
        if not file:
            file = self.file
        try:
            file.write('       texcoords2 {{ ')
            m = obj.to_mesh(bpy.context.scene, True, 'PREVIEW')
            face_count = 0
            # This fails if object has no UV's.
            for tex_face in m.tessface_uv_textures.active.data:
                uvs = tex_face.uv
                if len(uvs) == 3:
                    file.write('{ %s { %s %s }{ %s %s }{ %s %s } }' % ( face_count, uvs[0][0], uvs[0][1], uvs[1][0], uvs[1][1], uvs[2][0], uvs[2][1] ) )
                    face_count += 1
                else:
                    file.write('{ %s { %s %s }{ %s %s }{ %s %s } }' % ( face_count, uvs[0][0], uvs[0][1], uvs[1][0], uvs[1][1], uvs[2][0], uvs[2][1] ) )
                    face_count += 1
                    file.write('{ %s { %s %s }{ %s %s }{ %s %s } }' % ( face_count, uvs[0][0], uvs[0][1], uvs[2][0], uvs[2][1], uvs[3][0], uvs[3][1] ) )
                    face_count += 1
            file.write(' }}\n')
        except:
            file.write(' }}\n')


    def texbody(self, obj):
        # Write the TEXBODY for obj to file.
        self.file.write('\nTEXBODY {\n')
        self.file.write('  name  %s\n' % obj.name)
        self.file.write('  xform {{1 0 0 0}{0 1 0 0}{0 0 1 0}{0 0 0 1}}\n')
        self.file.write('  xfdef  { DEFINER\n')
        self.file.write('    DEFINER {\n')
        self.file.write('      out_mask  1\n')
        self.file.write('      inputs    { }\n')
        self.file.write('    }\n')
        self.file.write('  }\n')
        self.file.write('  color {1 1 1}\n')
        self.file.write('  mesh_data {\n')
        self.file.write('    LMESH {\n')
        # Vertices
        self.vertices(obj)
        # Faces
        self.faces(obj)
        # Creases
        self.creases(obj)
        # UV's
        self.uvs(obj)
        # Closing LMESH, mesh_data and TEXBODY and creating it.
        self.file.write('    }\n')
        self.file.write('  }\n')
        self.file.write('}\n')
        self.file.write('CREATE { %s }\n\n' % obj.name)

    def camera(self):
        # Write the camera to file. TODO! Does not work correctly.
        cam = bpy.data.scenes[0].camera
        self.file.write('\nCHNG_CAM {\n')
        self.file.write('{ %s %s %s }' % ( cam.location[0], cam.location[1], cam.location[2] ) )
        self.file.write('{ 0.0 0.0 0.0 }')
        self.file.write('{ %s %s %s }' % ( cam.location[0], cam.location[1], (cam.location[2] + 1) ) )
        self.file.write('{ 0.0 0.0 0.0 }')
        self.file.write(' 0.2 1 2.25 }\n')
        
                


    def unused(self):
        pass
        # CAMERA & VIEW
        # Export Camera
        # TODO! Aim at location, up vector and field of view.
        # TODO! Camera is seemingly pointing in the right direction, but model is facing differently. Find out what axis jot is using for up.
        # Set Windows size TODO! Don't know if this is needed.
        #self.file.write('CHNG_WIN { 30 34 480 580 }\n')
        # Set the View TODO! Don't know if this is needed, and insert correct data.
        #self.file.write('CHNG_VIEW {\n')
        #self.file.write('  VIEW {\n')
        #self.file.write('    view_animator {\n')
        #self.file.write('      Animator {\n')
        #self.file.write('        fps            -1\n')
        #self.file.write('        start_frame    -1\n')
        #self.file.write('        end_frame      -1\n')
        #self.file.write('        name { NULL_STR } \n')
        #self.file.write('      }\n')
        #self.file.write('    }\n')
        #self.file.write('    view_data_file { NULL_STR }\n')
        #self.file.write('  }\n')
        #self.file.write('}\n')
                
