import numpy as np
import os
import datetime
"""
Read and Write data from various XRD data formats
"""

def read_ras_file(filename):

    # Reads a data file from the .ras format

    input_file = open(filename, 'r')

    data_lines = input_file.readlines()

    x_data = []
    y_data = []

    recording = False
    for line in data_lines:

        if "RAS_INT_END" in line:
            recording = False

        # RAS Data format is a 3 column space separated data file with 2theta in first column
        # and intensity in second column
        if recording:


            data_elements = line.split()
            x_data.append(float(data_elements[0]))
            y_data.append(float(data_elements[1]))

        if "RAS_INT_START" in line:
            recording = True

    x_data =  np.array(x_data)

    y_data = np.array(y_data)

    return x_data, y_data





def read_mdi_file(filename):

    input_file = open(filename, 'r')

    data_lines = list(input_file.readlines())

    metadata_line = data_lines[1].split()

    start_angle = float(metadata_line[0])
    end_angle = float(metadata_line[5])
    data_points = int(metadata_line[6])

    # Generate the 2-theta values
    x_data = np.linspace(start_angle, end_angle, data_points)

    y_data = []

    # Load the intensity values
    for line in data_lines[2:]:
        for element in line.split():
           y_data.append(float(element))

    # Cast to numpy array
    y_data = np.array(y_data)

    return x_data, y_data

def write_mdi_file(filename, x_data, y_data, wavelength = 1.54056):

    output_file = open(filename, 'w')

    today = datetime.datetime.now()

    date_string = today.strftime("%m-%d-%y @%H:%M")

    header_string = date_string + " DIF CARBONXS EXPORT"

    starting_2theta = x_data[0]
    delta_2theta = x_data[1]-x_data[0]
    scanrate = 1.0

    # Dummy settings - Export a dummy diffraction
    anode = "CU"
    wavelength_str = "%6.5f"%wavelength

    ending_2theta = x_data[-1]
    total_data_points = len(x_data)


    output_file.write(header_string+"\n")
    output_file.write("%3.1f %3.1f %3.1f %s %s %4.1f %d \n"%(starting_2theta,
                                                          delta_2theta,
                                                          scanrate,
                                                          anode,
                                                          wavelength_str,
                                                          ending_2theta,
                                                          total_data_points
                                                          ))

    counter = 0
    data_line = ""

    # MDI Data format is eight columns of sequential data
    for data_point in y_data:

        data_line += "%8.1f "%data_point
        counter += 1

        if counter == 8:
            output_file.write(data_line + '\n')
            counter = 0
            data_line = ""

    # Write last output
    output_file.write(data_line + '\n')




if __name__ == '__main__':


    # generate synthetic data

    x_data = np.linspace(20, 120, 2000)
    y_data = 100*np.sin(x_data)+100
    write_mdi_file(os.path.join('export_test', 'test_export.mdi'), x_data, y_data)

    read_mdi_file(os.path.join('export_test', 'test_export.mdi'))


