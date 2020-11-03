# Sliced2Solid
A method to reconstruct solid geometry from sliced STL files (Gcode files), mainly for analysis purposes.

After creating a CAD model and slicing it to create a gcode file, do the following:
1. Run the GcodeProcess python script. It extracts the toolpaths from the gcode and saves them into a new txt file with the same name and "python_edited" sufffix.
2. Run the SOLIDWORKS macro "standalone macro" to generate these toolpaths in SOLIDWORKS.
3. Wait. It takes a while.
